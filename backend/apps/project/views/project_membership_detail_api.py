from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from ..serializers import (
    ProjectMembershipUpdateInputSerializer,
    ProjectMembershipUpdateOutputSerializer,
)
from ..services import project_membership_delete, project_membership_update


class ProjectMembershipDetailApi(APIView):
    """Update or delete a project membership."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ProjectMembershipUpdateInputSerializer,
        responses=ProjectMembershipUpdateOutputSerializer,
        summary="Update a project membership",
        tags=["Project memberships"],
    )
    def patch(self, request, project_id, membership_id):
        """Validate membership changes and delegate them to the service."""

        input_serializer = ProjectMembershipUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        membership = project_membership_update(
            project_id=str(project_id),
            membership_id=str(membership_id),
            requester_user_id=str(request.user.pk),
            role=input_serializer.validated_data["role"],
        )
        output_serializer = ProjectMembershipUpdateOutputSerializer(membership)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={204: None},
        summary="Remove a project member",
        tags=["Project memberships"],
    )
    def delete(self, request, project_id, membership_id):
        """Delegate membership deletion to the service."""

        project_membership_delete(
            project_id=str(project_id),
            membership_id=str(membership_id),
            requester_user_id=str(request.user.pk),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
