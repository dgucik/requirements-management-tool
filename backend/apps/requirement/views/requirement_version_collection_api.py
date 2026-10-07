from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    RequirementVersionCreateInputSerializer,
    RequirementVersionCreateOutputSerializer,
)
from ..services import requirement_version_create


class RequirementVersionCollectionApi(APIView):
    """Create a new draft version from an existing requirement version."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=RequirementVersionCreateInputSerializer,
        responses=RequirementVersionCreateOutputSerializer,
        summary="Create a draft requirement version",
    )
    def post(self, request, project_id, requirement_id):
        """Validate the source version and delegate version creation."""

        input_serializer = RequirementVersionCreateInputSerializer(
            data=request.data
        )
        input_serializer.is_valid(raise_exception=True)

        version = requirement_version_create(
            project_id=str(project_id),
            requirement_id=str(requirement_id),
            based_on_version_id=str(
                input_serializer.validated_data["based_on_version_id"]
            ),
            user_id=str(request.user.pk),
        )
        output_serializer = RequirementVersionCreateOutputSerializer(version)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
