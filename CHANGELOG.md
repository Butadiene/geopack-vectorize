# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.2] - 2026-11-04

### Fixed
- Preserve the T01 IMF clock angle for negative By instead of replacing it
  with 2*pi, correcting both scalar and vectorized magnetic fields.
- Accept integer coordinates without truncation in vectorized T01/T96,
  and preserve NumPy broadcasting and multidimensional inputs in T01.
- Broadcast all coordinate/vector components before transforms and determine
  scalar outputs from every input, including spherical transforms and the
  IGRF GSM/GSW wrappers.

## [2.0.1] - 2026-10-28

### Fixed
- Include every `geopack` subpackage in wheels and source distributions, including
  `geopack.vectorized.models`, so a normal pip installation can be imported.
- Load bundled IGRF coefficients on import without network access or writes to
  the installation directory. Updates remain available through `update_igrf()`,
  using HTTPS and a bounded request timeout.
- Restore `t89_vectorized`, `t96_vectorized`, `t01_vectorized`, and `t04_vectorized`
  imports from `geopack.vectorized`, including the quick-start import on PyPI.
- Restore upstream scalar model imports (`from geopack.t89 import t89`, and the
  corresponding T96, T01, and T04 paths) used by consumers such as pySPEDAS.

## [2.0.0] - 2026-02-11

### Breaking
- **Package renamed** from `geopack-vectorized` to `geopack-vectorize` on PyPI
- Reorganized all vectorized modules into `geopack/vectorized/` subpackage
  - Field models moved to `geopack/vectorized/models/` (t89, t96, t01, t04)
  - Coordinates, IGRF, tracing, geometry, derivatives moved under `geopack/vectorized/`
  - Removed `_vectorized` suffix from internal filenames
- Removed legacy tracing modules (`trace_field_lines_vectorized.py`, `trace_field_lines_vectorized_nointerp.py`)
- Removed several test/benchmark files (consolidated into remaining test suite)

### Added
- 14 new public functions exported from top-level `geopack` package
- Subpackage namespace access (`from geopack.vectorized import models, coordinates, igrf, trace`)
- Rewritten vectorized field line tracing (`geopack/vectorized/trace.py`)
- New test file for trace + vectorized model integration
- 5 new Jupyter notebooks (tracing guide, tracing validation, geometry/derivatives, T96 and dipole derivative maps)
- `SHOW_CHRISTOFFEL` notation toggle in derivative map notebooks

### Changed
- Translated all Japanese comments and docstrings to English
- Standardized all docstrings to NumPy format
- Unified code style and markdown formatting across examples and notebooks
- Improved trace test diagnostics

### Removed
- Entire `examples/conjugate_test/` directory
- 12 obsolete Jupyter notebooks
- Legacy example scripts and analysis outputs

## [1.0.13] - 2025-01-07

### Added
- Vectorized IGRF (International Geomagnetic Reference Field) implementation
  - `igrf_geo_vectorized()` for spherical geographic coordinates
  - `igrf_gsm_vectorized()` for GSM coordinates  
  - `igrf_gsw_vectorized()` for GSW coordinates
  - 9-13x performance improvement for arrays of 1000+ points
  - Exact numerical compatibility with scalar implementation
- Vectorized coordinate transformations
  - All major coordinate systems supported (GSM, GSE, GSW, GEO, MAG, SM, GEI)
  - 25-60x speedup for batch processing
  - `coordinates_vectorized.py` and `coordinates_vectorized_complex.py` modules
- Comprehensive Jupyter notebook examples
  - 01_coordinate_transformations_guide.ipynb
  - 02_magnetic_field_models_guide.ipynb  
  - 03_performance_comparison.ipynb
  - 04_accuracy_validation.ipynb
  - 05_igrf_vectorized_guide.ipynb
- Extensive test suites for IGRF and coordinate transformations
- Performance benchmarking scripts
- Documentation for vectorization implementations

### Changed
- Updated all notebooks to use vectorized functions where applicable
- Improved documentation with detailed vectorization guides

### Fixed
- Datetime hour range issue in coordinate transformation examples
- Matplotlib compatibility issues with streamplot alpha parameter
- Memory efficiency calculation division by zero error
- Function signature handling for bspcar/bcarsp transformations
- Undefined variable in satellite orbit example

## [1.0.12] - 2024-01-30

### Added
- Fully vectorized implementations of all magnetospheric models:
  - T89 model with 50x performance improvement
  - T96 model with 30x performance improvement
  - T01 model with complete vectorization
  - T04 model with complete vectorization
- Optimized field line tracing with 265x speedup
- Vectorized coordinate transformations
- Comprehensive test suite for all vectorized models
- Performance benchmarking tools
- Example scripts and notebooks

### Changed
- Reorganized package structure with separate `models/` and `vectorized/` modules
- Updated build configuration to use pyproject.toml
- Removed platform restrictions (now supports all platforms, not just Mac OS)
- Improved documentation and examples

### Fixed
- T01 and T04 models now handle invalid X values gracefully (X < -15 Re)
- Improved numerical stability in vectorized implementations
- Fixed edge cases in coordinate transformations

## [1.0.11] - Previous releases

See git history for changes in previous versions.
