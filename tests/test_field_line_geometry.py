"""Regression checks for coordinate dtypes in magnetic field geometry."""

import unittest

import numpy as np

import geopack


def uniform_field(parmod, ps, x, y, z):
    return tuple(np.full_like(x, value, dtype=float) for value in (3, 4, 0))


def helical_field(parmod, ps, x, y, z):
    return -1.0 * y, 1.0 * x, np.full_like(z, 2.0, dtype=float)


def bending_field(parmod, ps, x, y, z):
    return np.ones_like(x, dtype=float), 3.0 * x, 4.0 * x


class TestFieldLineGeometry(unittest.TestCase):
    def test_tangent_normalizes_integer_and_mixed_coordinates(self):
        for coordinates in ((3, 4, 0), (3., 4, 0.), (3., 4., 0.)):
            with self.subTest(coordinates=coordinates):
                tangent = geopack.field_line_tangent(
                    uniform_field, None, 0., *coordinates,
                )
                np.testing.assert_allclose(tangent, (.6, .8, 0.))
                self.assertTrue(all(isinstance(value, float) for value in tangent))

    def test_integer_zero_does_not_truncate_normal_component(self):
        # At x=0 the tangent is exactly (1, 0, 0), so only normal
        # normalization exposes truncation of the integer z component.
        normal = geopack.field_line_normal(bending_field, None, 0., 0., 0., 0)
        np.testing.assert_allclose(normal, (0., .6, .8))

    def test_integer_batches_preserve_shape_and_normalization(self):
        for shape in ((2,), (2, 2)):
            for dtype in (np.int32, np.int64, np.float32, np.float64):
                with self.subTest(shape=shape, dtype=dtype):
                    coordinates = tuple(np.full(shape, value, dtype=dtype)
                                        for value in (3, 4, 0))
                    tangent = geopack.field_line_tangent(
                        uniform_field, None, 0., *coordinates,
                    )
                    for component, expected in zip(tangent, (.6, .8, 0.)):
                        self.assertEqual(component.shape, shape)
                        self.assertTrue(np.issubdtype(component.dtype, np.floating))
                        np.testing.assert_allclose(component, expected)

    def test_helical_geometry_matches_analytic_values(self):
        # B=(-y,x,2) at radius 5 has curvature 5/29 and torsion 2/29.
        expected = np.concatenate((
            np.array([-4., 3., 2.]) / np.sqrt(29.),
            [-.6, -.8, 0.],
            np.array([1.6, -1.2, 5.]) / np.sqrt(29.),
            [5. / 29., 2. / 29.],
        ))
        for coordinates in ((3, 4, 0), (3., 4, 0.), (3., 4., 0.),
                            ([3, 3], [4, 4], [0, 0])):
            with self.subTest(coordinates=coordinates):
                actual = geopack.field_line_geometry_complete(
                    helical_field, None, 0., *coordinates,
                )
                for component, target in zip(actual, expected):
                    np.testing.assert_allclose(component, target, rtol=1e-5, atol=1e-10)
                derivatives = geopack.field_line_directional_derivatives(
                    helical_field, None, 0., *coordinates,
                )
                np.testing.assert_allclose(derivatives['dT_dT_n'], 5. / 29., rtol=1e-5)
                np.testing.assert_allclose(derivatives['dn_dT_b'], 2. / 29., rtol=1e-5)

    def test_zero_field_returns_zero_tangent_and_normal(self):
        def zero_field(parmod, ps, x, y, z):
            return np.zeros_like(x), np.zeros_like(y), np.zeros_like(z)

        for function in (geopack.field_line_tangent, geopack.field_line_normal):
            with self.subTest(function=function.__name__):
                np.testing.assert_array_equal(function(zero_field, None, 0., 1, 2, 0),
                                              (0., 0., 0.))


if __name__ == '__main__':
    unittest.main()
