from rest_framework import serializers

from .models import ProjectMembership


class ProjectCreateInputSerializer(serializers.Serializer):
    """Validate input required to create a project."""

    name = serializers.CharField(max_length=255, allow_blank=False, trim_whitespace=True)


class ProjectMembershipOutputSerializer(serializers.Serializer):
    """Serialize the membership created for a new project owner."""

    id = serializers.CharField()
    user_id = serializers.CharField()
    project_id = serializers.CharField()
    role = serializers.CharField()


class ProjectCreateOutputSerializer(serializers.Serializer):
    """Serialize the result returned after creating a project."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    owner_membership = ProjectMembershipOutputSerializer()


class ProjectUpdateInputSerializer(serializers.Serializer):
    """Validate input required to update a project."""

    name = serializers.CharField(max_length=255, allow_blank=False, trim_whitespace=True)


class ProjectUpdateOutputSerializer(serializers.Serializer):
    """Serialize the result returned after updating a project."""

    id = serializers.UUIDField()
    name = serializers.CharField()


class ProjectListOutputSerializer(serializers.Serializer):
    """Serialize projects available to the authenticated user."""

    id = serializers.UUIDField()
    name = serializers.CharField()
    role = serializers.CharField()


class ProjectMembershipCreateInputSerializer(serializers.Serializer):
    """Validate input required to add a member to a project."""

    user_id = serializers.CharField()
    role = serializers.ChoiceField(
        choices=[
            ProjectMembership.Role.VIEWER,
            ProjectMembership.Role.EDITOR,
            ProjectMembership.Role.MODERATOR,
        ]
    )


class ProjectMembershipCreateOutputSerializer(serializers.Serializer):
    """Serialize a membership created for a project."""

    id = serializers.UUIDField()
    user_id = serializers.CharField()
    project_id = serializers.UUIDField()
    role = serializers.CharField()


class ProjectMembershipUpdateInputSerializer(serializers.Serializer):
    """Validate input required to update a project membership."""

    role = serializers.ChoiceField(
        choices=[
            ProjectMembership.Role.VIEWER,
            ProjectMembership.Role.EDITOR,
            ProjectMembership.Role.MODERATOR,
        ]
    )


class ProjectMembershipUpdateOutputSerializer(serializers.Serializer):
    """Serialize a membership after it has been updated."""

    id = serializers.UUIDField()
    user_id = serializers.CharField()
    project_id = serializers.UUIDField()
    role = serializers.CharField()


class ProjectMembershipListOutputSerializer(serializers.Serializer):
    """Serialize memberships assigned to a project."""

    id = serializers.UUIDField()
    user_id = serializers.CharField()
    project_id = serializers.UUIDField()
    role = serializers.CharField()
