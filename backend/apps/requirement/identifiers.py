from collections.abc import Iterable


def requirement_key_generate(
    *, project_code: str, existing_keys: Iterable[str]
) -> str:
    """Generate the next shared item key for a project.

    Args:
        project_code: Slug identifying the project.
        existing_keys: Keys already used by any item in the project namespace.

    Returns:
        A unique slug in the ``<project-code>-<number>`` format.
    """

    used_keys = set(existing_keys)
    sequence = 1
    candidate = f"{project_code}-{sequence}"
    while candidate in used_keys:
        sequence += 1
        candidate = f"{project_code}-{sequence}"

    return candidate
