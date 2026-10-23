from itertools import chain

from .models import BusinessRule, Feature, Requirement


def key_existing_list() -> list[str]:
    """Return keys used by requirements, business rules, and features.

    Returns:
        A sorted list of unique keys used by supported requirement items.
    """

    key_querysets = (
        Requirement.objects.values_list("key", flat=True),
        BusinessRule.objects.values_list("key", flat=True),
        Feature.objects.values_list("key", flat=True),
    )
    return sorted(set(chain.from_iterable(key_querysets)))
