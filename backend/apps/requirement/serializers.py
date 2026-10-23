from rest_framework import serializers


class RequirementCreateInputSerializer(serializers.Serializer):
    """Validate data required to create a requirement and its first version."""

    title = serializers.CharField(
        max_length=255,
        allow_blank=False,
        trim_whitespace=True,
    )
    description = serializers.CharField(allow_blank=False, trim_whitespace=True)
    feature_id = serializers.UUIDField()


class RequirementInitialVersionOutputSerializer(serializers.Serializer):
    """Serialize the first version created with a requirement."""

    id = serializers.UUIDField()
    requirement_id = serializers.UUIDField()
    based_on_version_id = serializers.UUIDField(allow_null=True)
    created_by_id = serializers.CharField(allow_null=True)
    title = serializers.CharField()
    description = serializers.CharField()
    status = serializers.CharField()
    version = serializers.IntegerField()
    feature_id = serializers.UUIDField()
    target_release_version_id = serializers.CharField(allow_null=True)
    implemented_release_version_id = serializers.CharField(allow_null=True)


class RequirementVersionCreateInputSerializer(serializers.Serializer):
    """Validate the source version used to create a new draft version."""

    based_on_version_id = serializers.UUIDField()


class RequirementVersionCreateOutputSerializer(serializers.Serializer):
    """Serialize a new draft version created from an existing version."""

    id = serializers.UUIDField()
    requirement_id = serializers.UUIDField()
    based_on_version_id = serializers.UUIDField()
    created_by_id = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    status = serializers.CharField()
    version = serializers.IntegerField()
    feature_id = serializers.UUIDField()
    target_release_version_id = serializers.CharField(allow_null=True)
    implemented_release_version_id = serializers.CharField(allow_null=True)


class RequirementCreateOutputSerializer(serializers.Serializer):
    """Serialize a newly created requirement and its first version."""

    id = serializers.UUIDField()
    key = serializers.SlugField(max_length=255)
    first_version = RequirementInitialVersionOutputSerializer()


class RequirementListOutputSerializer(serializers.Serializer):
    """Serialize a requirement with its latest non-deleted version flattened."""

    id = serializers.UUIDField()
    key = serializers.SlugField(max_length=255)
    version_id = serializers.UUIDField()
    based_on_version_id = serializers.UUIDField(allow_null=True)
    created_by_id = serializers.CharField(allow_null=True)
    title = serializers.CharField()
    description = serializers.CharField()
    status = serializers.CharField()
    version = serializers.IntegerField()
    feature_id = serializers.UUIDField()
    target_release_version_id = serializers.UUIDField(allow_null=True)
    implemented_release_version_id = serializers.UUIDField(allow_null=True)
