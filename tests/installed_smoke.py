"""Run with ``python -I tests/installed_smoke.py [installation-directory]``."""

from pathlib import Path
import sys
import urllib.request

import numpy as np


def forbid_network(*args, **kwargs):
    raise AssertionError("Import and calculations must work without network access")


urllib.request.urlopen = forbid_network
if len(sys.argv) > 1:
    sys.path.insert(0, sys.argv[1])

import geopack
from geopack.vectorized import t96_vectorized
from geopack.t89 import t89
from geopack.t96 import t96
from geopack.t01 import t01
from geopack.t04 import t04

# Legacy module imports must leave the documented top-level functions callable.
for model in (t89, t96, t01, t04):
    assert model is getattr(geopack, model.__name__)

if len(sys.argv) > 1:
    assert Path(geopack.__file__).resolve().parent.parent == Path(sys.argv[1]).resolve()
print("Installed package:", geopack.__file__)

# The quick-start example on PyPI, including its original import path.
ps = geopack.recalc(0)
x = np.array([5.0, 6.0, 7.0, 8.0, 9.0])
y = np.zeros(5)
z = np.zeros(5)
parmod = np.array([2.0, -20.0, 0.0, -5.0, 0, 0, 0, 0, 0, 0])
assert np.isfinite(t96_vectorized(parmod, ps, x, y, z)).all()

for timestamp in (100, 1584662400, 1793106000):
    ps = geopack.recalc(timestamp)
    points = np.array([[5., .2, .3], [-6., 1., -.5], [2., -.3, 1.]])
    x, y, z = points.T
    for name in ("t89", "t96", "t01", "t04"):
        parameters = 3 if name == "t89" else parmod
        scalar = getattr(geopack, name)
        vectorized = getattr(geopack, name + "_vectorized")
        expected = np.array([scalar(parameters, ps, *p) for p in points]).T
        result = np.array(vectorized(parameters, ps, x, y, z))
        assert result.shape == (3, 3)
        assert np.isfinite(result).all()
        np.testing.assert_allclose(result, expected, rtol=1e-10, atol=1e-6)
        np.testing.assert_allclose(
            vectorized(parameters, ps, *points[0]), expected[:, 0],
            rtol=1e-10, atol=1e-6,
        )
    expected = np.array([geopack.igrf_gsm(*p) for p in points]).T
    np.testing.assert_allclose(
        geopack.igrf_gsm_vectorized(x, y, z), expected, rtol=1e-10, atol=1e-6,
    )
    transformed = geopack.geogsm_vectorized(x, y, z, j=1)
    np.testing.assert_allclose(
        geopack.geogsm_vectorized(*transformed, j=-1), points.T, atol=1e-12,
    )

for direction in (-1, 1):
    xf, yf, zf, status = geopack.trace_vectorized(
        np.array([3., 5.]), np.zeros(2), np.zeros(2), dir=direction,
        rlim=30, parmod=parmod, exname="t96", inname="dip",
    )
    assert np.isfinite([xf, yf, zf]).all()
    assert (status == 0).all()
    # The tracer preserves the scalar implementation's boundary crossing.
    assert (np.sqrt(xf**2 + yf**2 + zf**2) <= 1.).all()
    expected = np.array([
        geopack.trace(start, 0., 0., direction, rlim=30, parmod=parmod,
                      exname="t96", inname="dipole")[:3]
        for start in (3., 5.)
    ]).T
    np.testing.assert_allclose([xf, yf, zf], expected, atol=1e-5)


def total_field(parmod, ps, x, y, z):
    internal = geopack.dip(x, y, z)
    external = geopack.t96_vectorized(parmod, ps, x, y, z)
    return tuple(a + b for a, b in zip(internal, external))


frame = geopack.field_line_frenet_frame(total_field, parmod, ps, x, y, z, delta=1e-3)
tangent, normal, binormal = np.array(frame[:9]).reshape(3, 3, -1)
for axis in (tangent, normal, binormal):
    np.testing.assert_allclose(np.linalg.norm(axis, axis=0), 1., atol=1e-10)
# Central differences at delta=1e-3 have truncation error of order delta**2.
np.testing.assert_allclose(np.sum(tangent * normal, axis=0), 0., atol=1e-5)
assert np.isfinite(frame).all()
assert (np.asarray(frame[-1]) > 0).all()
derivatives = geopack.field_line_directional_derivatives(
    total_field, parmod, ps, x, y, z, delta=1e-3,
)
assert {
    "dT_dT_n", "dT_dT_b", "dn_dT_b", "dT_dn_n", "dT_dn_b",
    "dn_dn_b", "dn_db_b", "dn_db_T", "db_db_T",
}.issubset(derivatives)
assert all(np.isfinite(value).all() for value in derivatives.values())
np.testing.assert_allclose(derivatives["dT_dT_n"], frame[-1], rtol=1e-6, atol=1e-9)
print("Installed package checks passed")
