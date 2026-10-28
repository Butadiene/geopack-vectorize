"""Exercise installed artifacts outside the checkout, including an sdist rebuild."""

from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import zipfile

import pytest


ROOT = Path(__file__).resolve().parents[1]


def run(*args, cwd):
    result = subprocess.run(
        [str(arg) for arg in args], cwd=str(cwd),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        universal_newlines=True, timeout=120,
    )
    assert result.returncode == 0, result.stdout
    return result.stdout


@pytest.fixture(scope="module", params=["wheel", "sdist"])
def installed_distribution(request, tmp_path_factory):
    work = tmp_path_factory.mktemp("distribution-" + request.param)
    source = work / "source"
    shutil.copytree(
        str(ROOT), str(source),
        ignore=shutil.ignore_patterns(
            ".git", ".venv", "build", "dist", "*.egg-info",
            "__pycache__", ".pytest_cache",
        ),
    )
    artifacts = work / "artifacts"
    artifacts.mkdir()
    if request.param == "sdist":
        run(sys.executable, "-c",
            "from setuptools.build_meta import build_sdist; "
            "build_sdist('" + artifacts.as_posix() + "')", cwd=source)
        with tarfile.open(str(next(artifacts.glob("*.tar.gz")))) as archive:
            # The archive was just built from this checkout.
            if sys.version_info >= (3, 12):
                archive.extractall(str(work / "unpacked"), filter="data")
            else:
                archive.extractall(str(work / "unpacked"))
        source = next((work / "unpacked").iterdir())

    run(sys.executable, "-c",
        "from setuptools.build_meta import build_wheel; "
        "build_wheel('" + artifacts.as_posix() + "')", cwd=source)
    wheel = next(artifacts.glob("*.whl"))
    with zipfile.ZipFile(str(wheel)) as archive:
        names = set(archive.namelist())
    for path in (ROOT / "geopack").rglob("*.py"):
        assert path.relative_to(ROOT).as_posix() in names
    for path in (ROOT / "geopack" / "igrf_coeffs").glob("*.txt"):
        assert path.relative_to(ROOT).as_posix() in names
    assert not any(name.startswith(("tests/", "examples/")) for name in names)

    target = work / "installed"
    run(sys.executable, "-m", "pip", "install", "--no-index", "--no-deps",
        "--no-cache-dir", "--no-compile", "--target", target, wheel, cwd=work)
    return work, target


def test_installed_distribution(installed_distribution):
    work, target = installed_distribution
    smoke = Path(__file__).with_name("installed_smoke.py")
    output = run(sys.executable, "-I", smoke, target, cwd=work)
    assert "Installed package checks passed" in output
