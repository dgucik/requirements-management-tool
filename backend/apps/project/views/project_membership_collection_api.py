from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    ProjectMembershipCreateInputSerializer,
    ProjectMembershipCreateOutputSerializer,
    ProjectMembershipListOutputSerializer,
)
from ..selectors import project_membership_list
from ..services import project_membership_create


class ProjectMembershipCollectionApi(APIView):
    """List and create memberships in a project."""

    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        """Return memberships assigned to the project."""

        memberships = project_membership_list(project_id=str(project_id))
        output_serializer = ProjectMembershipListOutputSerializer(
            memberships,
            many=True,
        )
        return Response(output_serializer.data, status=status.HTTP_200_OK)

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
