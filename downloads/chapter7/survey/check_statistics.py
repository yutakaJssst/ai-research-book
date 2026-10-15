"""Independent small-sample checks using SciPy exhaustive permutations."""
import math
import numpy as np
from scipy import stats
from analyze import signed_rank, mann_whitney_exact, holm_correction

# Inclusive two-sided tails, including tied absolute ranks and discarded zeros.
for difference in ([1, -1, 2, -2, 0], [-1] * 6 + [-2] * 5,
                   [-1, -1] + [1] * 5 + [3] * 3, [1, 2, -3], [0, 0]):
    d = np.asarray(difference, dtype=float)
    nz = d[d != 0]
    actual = signed_rank(d)
    if len(nz):
        reference = stats.wilcoxon(
            nz, zero_method="wilcox", alternative="two-sided",
            method=stats.PermutationMethod(n_resamples=np.inf)).pvalue
    else:
        reference = 1.0
    assert math.isclose(actual["p"], reference, abs_tol=1e-12), (d, actual, reference)
    if len(nz) >= 10:
        reference_z = stats.wilcoxon(nz, method="approx", correction=False).zstatistic
        assert math.isclose(actual["r"], abs(reference_z) / math.sqrt(len(nz)), abs_tol=1e-12)

# SciPy independent-label permutations; ties are retained in the statistic.
for a, b in [([1, 1], [1, 2, 3]), ([2, 4, 4], [1, 1, 5]), ([1, 1], [2, 2])]:
    def statistic(x, y):
        return stats.mannwhitneyu(x, y, method="asymptotic").statistic
    reference = stats.permutation_test((a, b), statistic, permutation_type="independent",
                                       n_resamples=np.inf, alternative="two-sided").pvalue
    assert math.isclose(mann_whitney_exact(a, b), reference, abs_tol=1e-12)

assert signed_rank([-1] * 6 + [-2] * 5)["p"] == 0.0009765625
assert holm_correction([0.75, 1, 0.25, 1, 1, 0.0009765625])[-1] == 0.005859375
assert signed_rank([-1, -1] + [1] * 5 + [3] * 3)["p"] == 0.056640625
print("Passed: exact tied signed ranks, zero differences, tie-adjusted r, exact rank sums, Holm family.")
