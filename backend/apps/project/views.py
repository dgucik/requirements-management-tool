from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.project.serializers import (
    ProjectCreateInputSerializer,
    ProjectCreateOutputSerializer,
    ProjectListOutputSerializer,
    ProjectUpdateInputSerializer,
    ProjectUpdateOutputSerializer,
)
from apps.project.selectors import project_list
from apps.project.services import project_create, project_delete, project_update


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


class ProjectDetailApi(APIView):
    """Update or delete a project when requested by its owner."""

    permission_classes = [IsAuthenticated]

    def delete(self, request, project_id):
        """Delegate project deletion to the project service."""

        project_delete(
            project_id=str(project_id),
            user_id=str(request.user.pk),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, project_id):
        """Validate the request and delegate the project update to the service."""

        input_serializer = ProjectUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        project = project_update(
            project_id=str(project_id),
            user_id=str(request.user.pk),
            name=input_serializer.validated_data["name"],
        )
        output_serializer = ProjectUpdateOutputSerializer(project)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
