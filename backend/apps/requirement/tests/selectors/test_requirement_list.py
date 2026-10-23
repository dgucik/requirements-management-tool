import pytest
from django.contrib.auth import get_user_model

from apps.project.models import Project

from ...models import Feature, Requirement, RequirementVersion
from ...selectors import requirement_list


@pytest.mark.django_db
def test_requirement_list_hides_other_users_drafts_and_includes_requesters_drafts():
    user = get_user_model().objects.create_user(username="list-user")
    other_user = get_user_model().objects.create_user(username="other-list-user")
    project = Project.objects.create(name="Project", code="list-project")
    feature = Feature.objects.create(
        key="list-feature", title="Feature", project=project
    )

    own_draft = Requirement.objects.create(key="own-draft")
    RequirementVersion.objects.create(
        requirement=own_draft,
        created_by=user,
        title="Own draft",
        description="Visible to author",
        status=RequirementVersion.Status.DRAFT,
        version=1,
        feature=feature,
    )

    other_draft = Requirement.objects.create(key="other-draft")
    RequirementVersion.objects.create(
        requirement=other_draft,
        created_by=other_user,
        title="Other draft",
        description="Not visible to requester",
        status=RequirementVersion.Status.DRAFT,
        version=1,
        feature=feature,
    )

    approved = Requirement.objects.create(key="approved")
    RequirementVersion.objects.create(
        requirement=approved,
        created_by=other_user,
        title="Approved",
        description="Visible regardless of author",
        status=RequirementVersion.Status.APPROVED,
        version=1,
        feature=feature,
    )

    results = requirement_list(project_id=str(project.id), user_id=str(user.id))

    assert [result.key for result in results] == ["approved", "own-draft"]


@pytest.mark.django_db
def test_requirement_list_does_not_fall_back_to_older_non_draft_version():
    user = get_user_model().objects.create_user(username="latest-list-user")
    other_user = get_user_model().objects.create_user(username="latest-other-user")
    project = Project.objects.create(name="Project", code="latest-project")
    feature = Feature.objects.create(
        key="latest-feature", title="Feature", project=project
    )
    requirement = Requirement.objects.create(key="latest-draft")
    RequirementVersion.objects.create(
        requirement=requirement,
        created_by=other_user,
        title="Approved older version",
        description="Must not be used as fallback",
        status=RequirementVersion.Status.APPROVED,
        version=1,
        feature=feature,
    )
    RequirementVersion.objects.create(
        requirement=requirement,
        created_by=other_user,
        title="Latest draft",
        description="Hidden draft",
        status=RequirementVersion.Status.DRAFT,
        version=2,
        feature=feature,
    )

    assert requirement_list(project_id=str(project.id), user_id=str(user.id)) == []
