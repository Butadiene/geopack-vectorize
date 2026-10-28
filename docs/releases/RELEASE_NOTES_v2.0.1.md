# geopack-vectorize v2.0.1

This patch fixes installations of v2.0.0 that succeeded in pip but failed at
`import geopack` because the distribution omitted `geopack.vectorized.models`.
Both wheels and source distributions now include all `geopack` subpackages.

## Fixes

- Import and calculate fields using bundled IGRF coefficients without contacting
  NOAA or creating directories in the installation location. Explicit coefficient
  updates remain available through `update_igrf()` with HTTPS and a timeout.
- Restore the `from geopack.vectorized import t96_vectorized` quick-start import
  and the corresponding T89, T01, and T04 aliases.
- Support upstream scalar module imports used by pySPEDAS, including
  `from geopack.t89 import t89`, with matching T96, T01, and T04 paths.

## Validation

Tests cover building and installing a wheel directly and rebuilding a wheel from
the source distribution outside the checkout. Model outputs are compared with
the scalar implementations; coordinate transforms, IGRF, tracing, geometry, and
directional derivatives are exercised. Tests and the runnable README examples
passed on Python 3.14.4 with NumPy 2.5.3 and SciPy 1.18.1. Python 3.12 and a full
pySPEDAS installation were not tested in this environment.

## Installation

After the release is available on PyPI:

```bash
python -m pip install --upgrade geopack-vectorize==2.0.1
```

`geopack` and `geopack-vectorize` share installed Python package files. If both
distributions are needed, install `geopack-vectorize` last. If its files have
already been overwritten by reinstalling `geopack`, restore them with:

```bash
python -m pip install --force-reinstall --no-deps geopack-vectorize==2.0.1
```
