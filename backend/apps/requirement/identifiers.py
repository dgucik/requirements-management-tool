from collections.abc import Iterable


def requirement_key_generate(
    *, project_code: str, existing_keys: Iterable[str]
) -> str:
    """Generate the next readable requirement key for a project.

    Args:
        project_code: Slug identifying the project.
        existing_keys: Requirement keys already used in the project namespace.

    Returns:
        A unique slug in the ``<project-code>-r-<number>`` format.
    """

    used_keys = set(existing_keys)
    sequence = 1
    candidate = f"{project_code}-r-{sequence}"
    while candidate in used_keys:
        sequence += 1
        candidate = f"{project_code}-r-{sequence}"

    return candidate
