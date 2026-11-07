# geopack-vectorize v2.0.3

This patch preserves missing-coordinate results in vectorized T01/T96 and aligns
Cartesian-to-spherical longitude with the scalar API.

## Fixes

- **NaN coordinates.** Vectorized T01 and T96 now return NaN magnetic-field
  components when a coordinate is NaN. Previously, these samples matched no
  magnetopause region and incorrectly returned zero fields. Valid points in the
  same batch retain their existing values.
- **Spherical longitude.** Cartesian-to-spherical `sphcar_vectorized` now adds
  2*pi to negative longitude, matching the scalar convention. For example,
  `(1, -1, 0)` returns `7*pi/4` instead of `-pi/4`. Both angles describe the same
  direction. The zero-longitude convention at the poles is preserved.

## Validation

Regression tests cover NaN in each coordinate, scalar return types,
multidimensional batches containing both valid and missing coordinates, all four
longitude quadrants, signed-zero axis cases, poles, the origin, and broadcasting.
The calculation and distribution tests pass, including wheel and source
distribution installation checks. CI covers Python 3.12 and 3.14.

## Installation

```bash
python -m pip install --upgrade geopack-vectorize==2.0.3
```

`geopack` and `geopack-vectorize` share installed Python package files. If both
distributions are needed, install `geopack-vectorize` last. If its files have
already been overwritten by reinstalling `geopack`, restore them with:

```bash
python -m pip install --force-reinstall --no-deps geopack-vectorize==2.0.3
```
