from collections.abc import Iterable

from django.utils.text import slugify


def project_code_generate(*, name: str, existing_codes: Iterable[str]) -> str:
    """Generate a unique, readable project code with at most ten characters.

    Args:
        name: Project name used as the source for the generated code.
        existing_codes: Codes that are already used and must be avoided.

    Returns:
        A lowercase slug no longer than ten characters.
    """

    normalized_slug = slugify(name)
    words = [word for word in normalized_slug.split("-") if word]
    initials = "".join(word[0] for word in words)
    base = initials if len(words) > 1 and initials else normalized_slug.replace("-", "")
    base = (base[:10].strip("-") or "project")[:10]

    used_codes = set(existing_codes)
    candidate = base
    suffix_number = 1
    while candidate in used_codes:
        suffix = f"-{suffix_number}"
        stem = base[: 10 - len(suffix)].rstrip("-")
        candidate = f"{stem}{suffix}"
        suffix_number += 1

    return candidate
