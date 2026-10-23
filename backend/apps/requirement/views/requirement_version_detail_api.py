from drf_spectacular.utils import OpenApiRequest, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    RequirementVersionUpdateInputSerializer,
    RequirementVersionUpdateOutputSerializer,
)
from ..services import requirement_version_update


class RequirementVersionDetailApi(APIView):
    """Update an existing requirement version."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=OpenApiRequest(
            request={
                "type": "object",
                "required": [
                    "title",
                    "description",
                    "target_release_version_id",
                    "implemented_release_version_id",
                    "feature_id",
                ],
                "properties": {
                    "title": {"type": "string", "maxLength": 255},
                    "description": {"type": "string"},
                    "target_release_version_id": {
                        "type": "string",
                        "format": "uuid",
                        "nullable": True,
                    },
                    "implemented_release_version_id": {
                        "type": "string",
                        "format": "uuid",
                        "nullable": True,
                    },
                    "feature_id": {"type": "string", "format": "uuid"},
                },
            }
        ),
        responses=RequirementVersionUpdateOutputSerializer,
        summary="Update editable requirement version fields",
        tags=["Requirements"],
    )
    def patch(self, request, project_id, requirement_id, version_id):
        """Validate editable fields and delegate version updates to the service."""

        input_serializer = RequirementVersionUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        version = requirement_version_update(
            project_id=str(project_id),
            requirement_id=str(requirement_id),
            version_id=str(version_id),
            user_id=str(request.user.pk),
            title=data["title"],
            description=data["description"],
            target_release_version_id=(
                str(data["target_release_version_id"])
                if data["target_release_version_id"]
                else None
            ),
            implemented_release_version_id=(
                str(data["implemented_release_version_id"])
                if data["implemented_release_version_id"]
                else None
            ),
            feature_id=str(data["feature_id"]),
        )
        output_serializer = RequirementVersionUpdateOutputSerializer(version)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
