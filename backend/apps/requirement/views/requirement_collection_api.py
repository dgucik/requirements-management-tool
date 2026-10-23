from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    RequirementCreateInputSerializer,
    RequirementCreateOutputSerializer,
    RequirementListOutputSerializer,
)
from ..selectors import requirement_list
from ..services import requirement_create


class RequirementCollectionApi(APIView):
    """List and create requirements in a project."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=RequirementListOutputSerializer(many=True),
        summary="List requirements with their latest active versions",
        tags=["Requirements"],
    )
    def get(self, request, project_id):
        """Return requirements and their latest non-deleted versions."""

        requirements = requirement_list(project_id=str(project_id))
        output_serializer = RequirementListOutputSerializer(
            requirements,
            many=True,
        )
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=RequirementCreateInputSerializer,
        responses=RequirementCreateOutputSerializer,
        summary="Create a requirement and its first version",
        tags=["Requirements"],
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
