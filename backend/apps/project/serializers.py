from rest_framework import serializers


class ProjectCreateInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_blank=False, trim_whitespace=True)


class ProjectMembershipOutputSerializer(serializers.Serializer):
    id = serializers.CharField()
    user_id = serializers.CharField()
    project_id = serializers.CharField()
    role = serializers.CharField()


class ProjectCreateOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    owner_membership = ProjectMembershipOutputSerializer()
