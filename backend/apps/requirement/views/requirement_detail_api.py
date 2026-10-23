from drf_spectacular.utils import OpenApiRequest, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import RequirementUpdateInputSerializer, RequirementUpdateOutputSerializer
from ..services import requirement_update


class RequirementDetailApi(APIView):
    """Update an existing requirement."""

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
                },
            }
        ),
        responses=RequirementUpdateOutputSerializer,
        summary="Update a requirement",
        tags=["Requirements"],
    )
    def patch(self, request, project_id, requirement_id):
        """Validate editable fields and delegate requirement updates to the service."""

        input_serializer = RequirementUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data

        requirement = requirement_update(
            project_id=str(project_id),
            requirement_id=str(requirement_id),
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
        )
        output_serializer = RequirementUpdateOutputSerializer(requirement)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
