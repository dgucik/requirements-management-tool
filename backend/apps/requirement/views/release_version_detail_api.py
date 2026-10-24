from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    ReleaseVersionUpdateInputSerializer,
    ReleaseVersionUpdateOutputSerializer,
)
from ..services import release_version_delete, release_version_update


class ReleaseVersionDetailApi(APIView):
    """Update or permanently delete a release version."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ReleaseVersionUpdateInputSerializer,
        responses=ReleaseVersionUpdateOutputSerializer,
        summary="Update a release version",
        tags=["Release versions"],
    )
    def patch(self, request, project_id, release_version_id):
        """Validate the name and delegate the update."""

        input_serializer = ReleaseVersionUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        release_version = release_version_update(
            project_id=str(project_id),
            release_version_id=str(release_version_id),
            user_id=str(request.user.pk),
            name=input_serializer.validated_data["name"],
        )
        output_serializer = ReleaseVersionUpdateOutputSerializer(release_version)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={status.HTTP_204_NO_CONTENT: None},
        summary="Delete a release version",
        tags=["Release versions"],
    )
    def delete(self, request, project_id, release_version_id):
        """Permanently delete the selected release version."""

        release_version_delete(
            project_id=str(project_id),
            release_version_id=str(release_version_id),
            user_id=str(request.user.pk),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
