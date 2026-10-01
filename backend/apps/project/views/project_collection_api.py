from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..selectors import project_list
from ..serializers import (
    ProjectCreateInputSerializer,
    ProjectCreateOutputSerializer,
    ProjectListOutputSerializer,
)
from ..services import project_create


class ProjectCollectionApi(APIView):
    """List and create projects for authenticated users."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return projects where the authenticated user has a membership."""

        projects = project_list(user_id=str(request.user.pk))
        output_serializer = ProjectListOutputSerializer(projects, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Validate the request and delegate project creation to the service."""

        input_serializer = ProjectCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        project = project_create(
            name=input_serializer.validated_data["name"],
            owner_user_id=str(request.user.pk),
        )

        output_serializer = ProjectCreateOutputSerializer(project)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
