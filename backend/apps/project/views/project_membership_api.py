from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    ProjectMembershipCreateInputSerializer,
    ProjectMembershipCreateOutputSerializer,
)
from ..services import project_membership_create


class ProjectMembershipCreateApi(APIView):
    """Add a non-owner member to a project."""

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
