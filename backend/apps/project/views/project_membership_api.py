from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    ProjectMembershipCreateInputSerializer,
    ProjectMembershipCreateOutputSerializer,
)
from ..services import project_membership_create, project_membership_delete


class ProjectMembershipApi(APIView):
    """Create or delete a project membership."""

    permission_classes = [IsAuthenticated]

    def post(self, request, project_id):
        """Validate membership data and delegate creation to the service."""

        input_serializer = ProjectMembershipCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        membership = project_membership_create(
            project_id=str(project_id),
            user_id=input_serializer.validated_data["user_id"],
            requester_user_id=str(request.user.pk),
            role=input_serializer.validated_data["role"],
        )
        output_serializer = ProjectMembershipCreateOutputSerializer(membership)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, project_id, membership_id):
        """Delegate membership deletion to the project membership service."""

        project_membership_delete(
            project_id=str(project_id),
            membership_id=str(membership_id),
            requester_user_id=str(request.user.pk),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
