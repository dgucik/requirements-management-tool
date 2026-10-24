from rest_framework import serializers


class RequirementCreateInputSerializer(serializers.Serializer):
    """Validate data required to create a requirement."""

    title = serializers.CharField(max_length=255, allow_blank=False, trim_whitespace=True)
    description = serializers.CharField(allow_blank=False, trim_whitespace=True)
    feature_id = serializers.UUIDField()


class RequirementUpdateInputSerializer(serializers.Serializer):
    """Validate editable fields for a requirement."""

    title = serializers.CharField(max_length=255, allow_blank=False, trim_whitespace=True)
    description = serializers.CharField(allow_blank=False, trim_whitespace=True)
    target_release_version_id = serializers.UUIDField(allow_null=True)
    implemented_release_version_id = serializers.UUIDField(allow_null=True)

    def validate(self, attrs):
        """Reject fields outside the requirement's editable attributes."""

        editable_fields = {
            "title",
            "description",
            "target_release_version_id",
            "implemented_release_version_id",
        }
        unsupported_fields = set(self.initial_data) - editable_fields
        if unsupported_fields:
            raise serializers.ValidationError(
                {
                    field: "This field cannot be changed."
                    for field in sorted(unsupported_fields)
                }
            )
        return attrs


class RequirementOutputSerializer(serializers.Serializer):
    """Serialize a requirement."""

    id = serializers.UUIDField()
    key = serializers.SlugField(max_length=255)
    created_by_id = serializers.CharField(allow_null=True)
    title = serializers.CharField()
    description = serializers.CharField()
    feature_id = serializers.UUIDField()
    target_release_version_id = serializers.UUIDField(allow_null=True)
    implemented_release_version_id = serializers.UUIDField(allow_null=True)


class RequirementCreateOutputSerializer(RequirementOutputSerializer):
    """Serialize a newly created requirement."""


class RequirementUpdateOutputSerializer(RequirementOutputSerializer):
    """Serialize an updated requirement."""


class RequirementListOutputSerializer(serializers.Serializer):
    """Serialize requirement fields returned by the list endpoint."""

    id = serializers.UUIDField()
    key = serializers.SlugField(max_length=255)
    created_by_id = serializers.CharField(allow_null=True)
    title = serializers.CharField()
    description = serializers.CharField()
    feature_id = serializers.UUIDField()
    target_release_version_id = serializers.UUIDField(allow_null=True)
    implemented_release_version_id = serializers.UUIDField(allow_null=True)


class FeatureCreateInputSerializer(serializers.Serializer):
    """Validate the title required to create a project feature."""

    title = serializers.CharField(max_length=255, allow_blank=False, trim_whitespace=True)


class FeatureCreateOutputSerializer(serializers.Serializer):
    """Serialize a newly created project feature."""

    id = serializers.UUIDField()
    key = serializers.SlugField(max_length=255)
    title = serializers.CharField()
    project_id = serializers.UUIDField()


class FeatureUpdateInputSerializer(serializers.Serializer):
    """Validate the title required to update a feature."""

    title = serializers.CharField(max_length=255, allow_blank=False, trim_whitespace=True)

    def validate(self, attrs):
        """Reject fields outside the feature's editable attributes."""

        unsupported_fields = set(self.initial_data) - {"title"}
        if unsupported_fields:
            raise serializers.ValidationError(
                {
                    field: "This field cannot be changed."
                    for field in sorted(unsupported_fields)
                }
            )
        return attrs


class FeatureUpdateOutputSerializer(FeatureCreateOutputSerializer):
    """Serialize an updated project feature."""


class FeatureDeleteOutputSerializer(serializers.Serializer):
    """Serialize a soft-deleted project feature."""

    id = serializers.UUIDField()
    is_deleted = serializers.BooleanField()


class FeatureListOutputSerializer(serializers.Serializer):
    """Serialize features returned for a project."""

    id = serializers.UUIDField()
    key = serializers.SlugField(max_length=255)
    title = serializers.CharField()
    project_id = serializers.UUIDField()
