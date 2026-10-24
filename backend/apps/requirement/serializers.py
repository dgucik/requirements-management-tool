from rest_framework import serializers


class BusinessRuleCreateInputSerializer(serializers.Serializer):
    """Validate data required to create a business rule."""

    rule = serializers.CharField(allow_blank=False, trim_whitespace=True)
    requirement_ids = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False,
    )


class BusinessRuleUpdateInputSerializer(serializers.Serializer):
    """Validate editable fields for a business rule."""

    rule = serializers.CharField(
        allow_blank=False,
        required=False,
        trim_whitespace=True,
    )
    requirement_ids = serializers.ListField(
        child=serializers.UUIDField(),
        allow_empty=False,
        required=False,
    )

    def validate(self, attrs):
        """Reject fields outside the business rule's editable attributes."""

        unsupported_fields = set(self.initial_data) - {"rule", "requirement_ids"}
        if unsupported_fields:
            raise serializers.ValidationError(
                {
                    field: "This field cannot be changed."
                    for field in sorted(unsupported_fields)
                }
            )
        if not attrs:
            raise serializers.ValidationError(
                "At least one editable field is required."
            )
        return attrs


class BusinessRuleOutputSerializer(serializers.Serializer):
    """Serialize a business rule."""

    id = serializers.UUIDField()
    key = serializers.SlugField(max_length=255)
    rule = serializers.CharField()
    requirement_ids = serializers.ListField(child=serializers.UUIDField())


class BusinessRuleCreateOutputSerializer(BusinessRuleOutputSerializer):
    """Serialize a newly created business rule."""


class BusinessRuleUpdateOutputSerializer(BusinessRuleOutputSerializer):
    """Serialize an updated business rule."""


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
