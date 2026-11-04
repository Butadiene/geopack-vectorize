"""Regressions independent of scalar/vectorized implementation agreement."""

import unittest

import numpy as np

from geopack import models
from geopack.vectorized import models as vectorized


PARMOD = [2., -20., 2., -5., 1., 1., 1., 1., 1., 1.]


class TestModelInputRegressions(unittest.TestCase):
    def test_t01_imf_interconnection_preserves_clock_angle(self):
        # With G1/G2 held fixed, the IMF dependence is exactly the prescribed
        # T01 interconnection field, including outside the magnetopause.
        for function in (models.t01, vectorized.t01):
            for point in ((-6., 2., 1.), (15., 3., 1.)):
                base = list(PARMOD)
                base[2:4] = [0., 0.]
                baseline = np.array(function(base, .2, *point))
                for by in (-5., -1e-8, -0., 0., 1e-8, 5.):
                    for bz in (-5., 5.):
                        with self.subTest(api=function.__module__, point=point, by=by, bz=bz):
                            parameters = list(PARMOD)
                            parameters[2:4] = [by, bz]
                            theta = np.arctan2(by, bz)
                            factor = .05887 + .57691 * np.sin(theta / 2.)**2
                            expected = baseline + factor * np.array([0., by, bz])
                            actual = function(parameters, .2, *point)
                            np.testing.assert_allclose(actual, expected, rtol=1e-12, atol=1e-9)

    def test_integer_coordinates_match_scalar_fields_in_all_regions(self):
        points = np.array([[5, 1, 1], [10, 0, -5], [15, 1, 1]])
        for name in ('t01', 't96'):
            scalar, batched = getattr(models, name), getattr(vectorized, name)
            expected = np.array([scalar(PARMOD, .4, *point.astype(float)) for point in points]).T
            with self.subTest(model=name, mode='batch'):
                np.testing.assert_allclose(batched(PARMOD, .4, *points.T), expected,
                                           rtol=1e-10, atol=1e-6)
            for point, field in zip(points, expected.T):
                with self.subTest(model=name, point=point):
                    actual = batched(PARMOD, .4, *(int(c) for c in point))
                    np.testing.assert_allclose(actual, field, rtol=1e-10, atol=1e-6)
                    self.assertTrue(all(isinstance(c, float) for c in actual))

    def test_t01_broadcast_and_mesh_inputs_match_pointwise_fields(self):
        points = (
            (5., np.array([1., 2.]), 1.),
            (np.array([5., 10.])[:, None], np.array([1., 2., 3.]), -5.),
            np.meshgrid([5., 10.], [1., 2.], [-5., 1.], indexing='ij'),
        )
        for coords in points:
            broadcast = np.broadcast_arrays(*coords)
            expected = np.array([models.t01(PARMOD, .4, *point)
                                 for point in zip(*(c.ravel() for c in broadcast))])
            expected = expected.T.reshape((3,) + broadcast[0].shape)
            with self.subTest(shape=broadcast[0].shape):
                actual = vectorized.t01(PARMOD, .4, *coords)
                for component in actual:
                    self.assertEqual(component.shape, broadcast[0].shape)
                np.testing.assert_allclose(actual, expected, rtol=1e-10, atol=1e-6)


if __name__ == '__main__':
    unittest.main()
