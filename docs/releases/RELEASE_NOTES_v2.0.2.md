# geopack-vectorize v2.0.2

This patch corrects T01 magnetic fields for negative IMF By and fixes several
input-handling defects in the vectorized API.

## Fixes

- **T01 IMF clock angle (scalar and vectorized).** For negative IMF By, the clock
  angle was replaced with 2*pi instead of being shifted by 2*pi, which removed the
  clock-angle-dependent interconnection field. The angle is now preserved, matching
  the original Fortran model. T01 results with By < 0 change in this release.
- **Integer coordinates.** Vectorized T01 and T96 now convert coordinates to
  floating point. Integer inputs previously truncated T96 field components and could
  place T01 points in the wrong magnetopause region.
- **Broadcasting.** Vectorized T01 accepts mixed scalar/array inputs and
  multidimensional grids (e.g. `np.meshgrid`). Coordinate transforms, spherical and
  magnetic-component transforms, and the IGRF GSM/GSW wrappers broadcast every input
  and return scalars only when every input is scalar.

## Validation

New regression tests check the T01 IMF interconnection field against its prescribed
form independently of scalar/vectorized agreement, compare integer and
multidimensional model inputs with pointwise scalar fields, and exercise both
directions of each coordinate transform with every input broadcast. CI runs all
calculation tests on Python 3.12 and 3.14.

## Installation

After the release is available on PyPI:

```bash
python -m pip install --upgrade geopack-vectorize==2.0.2
```

`geopack` and `geopack-vectorize` share installed Python package files. If both
distributions are needed, install `geopack-vectorize` last. If its files have
already been overwritten by reinstalling `geopack`, restore them with:

```bash
python -m pip install --force-reinstall --no-deps geopack-vectorize==2.0.2
```
