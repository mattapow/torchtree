from torch.distributions import Gamma, TransformedDistribution, constraints
from torch.distributions.transforms import PowerTransform


class InverseGamma(TransformedDistribution):
    arg_constraints = {
        'concentration': constraints.positive,
        'rate': constraints.positive,
    }
    support = constraints.positive
    has_rsample = True

    def __init__(self, concentration, rate, validate_args=None):
        base_dist = Gamma(concentration, rate)
        super().__init__(
            base_dist,
            PowerTransform(-base_dist.rate.new_ones(())),
            validate_args=validate_args,
        )

    def expand(self, batch_shape, _instance=None):
        new = self._get_checked_instance(InverseGamma, _instance)
        return super().expand(batch_shape, _instance=new)

    @property
    def concentration(self):
        return self.base_dist.concentration

    @property
    def rate(self):
        return self.base_dist.rate
