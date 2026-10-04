from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    RequirementCreateInputSerializer,
    RequirementCreateOutputSerializer,
)
from ..services import requirement_create


class RequirementCollectionApi(APIView):
    """Create requirements in a project."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=RequirementCreateInputSerializer,
        responses=RequirementCreateOutputSerializer,
        summary="Create a requirement and its first version",
    )
    def post(self, request, project_id):
        """Validate input and delegate requirement creation to the service."""

        input_serializer = RequirementCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        requirement = requirement_create(
            project_id=str(project_id),
            user_id=str(request.user.pk),
            title=input_serializer.validated_data["title"],
            description=input_serializer.validated_data["description"],
            feature_id=str(input_serializer.validated_data["feature_id"]),
        )
        output_serializer = RequirementCreateOutputSerializer(requirement)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
