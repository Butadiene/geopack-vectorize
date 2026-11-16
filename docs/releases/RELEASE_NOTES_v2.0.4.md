# geopack-vectorize v2.0.4

This patch fixes integer-coordinate truncation in Mageometry and updates the
recommended citation to the Earth, Planets and Space paper.

## Fixes

- Tangent and normal vectors now use floating-point output arrays. With a field
  of `(3, 4, 0)`, integer coordinates now produce the tangent `(0.6, 0.8, 0.0)`.
  Previously, the fractional components were truncated to zero. Mixed coordinate
  types, including an integer zero on just one axis, could also truncate vector
  components and affect curvature, torsion, and directional derivatives.
- `CITATION.cff` now recommends Isono, Yoshikawa, and Katoh (2026),
  *A local-frame approach to three-dimensional analysis of magnetospheric magnetic
  fields*, DOI `10.1186/s40623-026-02528-2`. The original geopack author and DOI
  remain credited in the references. The file conforms to CFF 1.2.0.

## Validation

Regression tests cover integer and mixed coordinates, integer-zero normal
components, array shapes and dtypes, zero fields, and helical-field geometry
and directional derivatives against analytical values. Release checks include
the calculation suite and isolated wheel and source distribution installations.

## Installation

```bash
python -m pip install --upgrade geopack-vectorize==2.0.4
```
