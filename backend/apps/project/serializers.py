from rest_framework import serializers


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
