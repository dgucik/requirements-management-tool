from apps.requirement.identifiers import requirement_key_generate


def test_requirement_key_generate_uses_shared_project_sequence():
    assert requirement_key_generate(
        project_code="project",
        existing_keys=["project-1", "project-3"],
    ) == "project-2"
