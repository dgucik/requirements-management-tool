from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.project.serializers import (
    ProjectCreateInputSerializer,
    ProjectCreateOutputSerializer,
)
from apps.project.services import project_create


class ProjectCreateApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        input_serializer = ProjectCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        project = project_create(
            name=input_serializer.validated_data["name"],
            owner_user_id=str(request.user.pk),
        )

        output_serializer = ProjectCreateOutputSerializer(project)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
