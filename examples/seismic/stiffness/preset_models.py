import numpy as np

from examples.seismic.stiffness.model import ElasticModel

__all__ = ['demo_model']


def demo_model(preset, **kwargs):
    """
    Utility function to create preset `Model` objects for
    demonstration and testing purposes. The particular presets are ::

    * `constant-elastic` : A constant single-layer model in a 2D or 3D domain with
                    velocity 1.5 km/s
    * 'layers-elastic': Simple n-layered model with velocities ranging from 1.5 km/s
                    to 3.5 km/s in the top and bottom layer respectively.
                    Vs is set to .5 vp and 0 in the top layer.
    """
    space_order = kwargs.pop('space_order', 2)
    shape = kwargs.pop('shape', (101, 101))
    spacing = kwargs.pop('spacing', tuple([10. for _ in shape]))
    origin = kwargs.pop('origin', tuple([0. for _ in shape]))
    nbl = kwargs.pop('nbl', 10)
    dtype = kwargs.pop('dtype', np.float32)
    vp = kwargs.pop('vp', 1.5)
    nlayers = kwargs.pop('nlayers', 3)

    if preset.lower() in ['constant-elastic']:
        # A constant single-layer model in a 2D or 3D domain
        # with velocity 1.5 km/s.
        vs = 0.5 * vp
        rho = 1.0

        return ElasticModel(space_order=space_order, vp=vp, vs=vs, rho=rho,
                            origin=origin, shape=shape, dtype=dtype, spacing=spacing,
                            nbl=nbl, **kwargs)

    elif preset.lower() in ['layers-elastic']:
        # A n-layers model in a 2D or 3D domain with two different
        # velocities split across the height dimension:
        # By default, the top part of the domain has 1.5 km/s,
        # and the bottom part of the domain has 2.5 km/s.
        vp_top = kwargs.pop('vp_top', 1.5)
        vp_bottom = kwargs.pop('vp_bottom', 3.5)

        # Define a velocity profile in km/s
        v = np.empty(shape, dtype=dtype)
        v[:] = vp_top  # Top velocity (background)
        vp_i = np.linspace(vp_top, vp_bottom, nlayers)
        for i in range(1, nlayers):
            v[..., i*int(shape[-1] / nlayers):] = vp_i[i]  # Bottom velocity

        vs = 0.5 * v[:]
        rho = (0.31 * (1e3*v)**0.25)
        rho[v < 1.51] = 1.0
        vs[v < 1.51] = 0.0

        return ElasticModel(space_order=space_order, vp=v, vs=vs, rho=rho,
                            origin=origin, shape=shape,
                            dtype=dtype, spacing=spacing, nbl=nbl, **kwargs)

    else:
        raise ValueError("Unknown model preset name")
