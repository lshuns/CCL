_all__ = ("ConcentrationDuffy08", "ConcentrationDuffy08FreeScaling")

from . import Concentration


class ConcentrationDuffy08(Concentration):
    """Concentration-mass relation by `Duffy et al. 2008
    <https://arxiv.org/abs/0804.2486>`_. This parametrization is only
    valid for S.O. masses with :math:`\\Delta = \\Delta_{\\rm vir}`,
    of :math:`\\Delta=200` times the matter or critical density.
    By default it will be initialized for :math:`M_{200c}`.

    Args:
        mass_def (:class:`~pyccl.halos.massdef.MassDef` or :obj:`str`): a mass
            definition object, or a name string.
    """
    name = 'Duffy08'

    def __init__(self, *, mass_def="200c"):
        super().__init__(mass_def=mass_def)

    def _check_mass_def_strict(self, mass_def):
        return mass_def.name not in ["vir", "200m", "200c"]

    def _setup(self):
        vals = {"vir": (7.85, -0.081, -0.71),
                "200m": (10.14, -0.081, -1.01),
                "200c": (5.71, -0.084, -0.47)}

        self.A, self.B, self.C = vals[self.mass_def.name]

    def _concentration(self, cosmo, M, a):
        M_pivot_inv = cosmo["h"] * 5E-13
        return self.A * (M * M_pivot_inv)**self.B * a**(-self.C)

class ConcentrationDuffy08FreeScaling(ConcentrationDuffy08):
    """Concentration-mass relation by `Duffy et al. 2008
    <https://arxiv.org/abs/0804.2486>`_. This parametrization is only
    valid for S.O. masses with :math:`\\Delta = \\Delta_{\\rm vir}`,
    of :math:`\\Delta=200` times the matter or critical density.
    By default it will be initialized for :math:`M_{200c}`.
    This modification allows a free scaling parameter.

    Args:
        mass_def (:class:`~pyccl.halos.massdef.MassDef` or :obj:`str`): a mass
            definition object, or a name string.
        f_c (:obj:`float`): a scaling factor applied to the relation.
    """
    name = 'Duffy08FreeScaling'

    def __init__(self, *, mass_def="200c", f_c=1):
        super().__init__(mass_def=mass_def)
        self.f_c = f_c

    def _concentration(self, cosmo, M, a):
        M_pivot_inv = cosmo["h"] * 5E-13
        return self.f_c * self.A * (M * M_pivot_inv)**self.B * a**(-self.C)
