from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..selectors import release_version_list
from ..serializers import (
    ReleaseVersionCreateInputSerializer,
    ReleaseVersionCreateOutputSerializer,
    ReleaseVersionOutputSerializer,
)
from ..services import release_version_create


class ReleaseVersionCollectionApi(APIView):
    """List and create release versions."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=ReleaseVersionOutputSerializer(many=True),
        summary="List release versions",
        tags=["Release versions"],
    )
    def get(self, request, project_id):
        """Return all release versions."""

        release_versions = release_version_list(project_id=str(project_id))
        output_serializer = ReleaseVersionOutputSerializer(
            release_versions,
            many=True,
        )
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=ReleaseVersionCreateInputSerializer,
        responses=ReleaseVersionCreateOutputSerializer,
        summary="Create a release version",
        tags=["Release versions"],
    )
    def post(self, request, project_id):
        """Validate input and delegate release version creation."""

        input_serializer = ReleaseVersionCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        release_version = release_version_create(
            project_id=str(project_id),
            user_id=str(request.user.pk),
            name=input_serializer.validated_data["name"],
        )
        output_serializer = ReleaseVersionCreateOutputSerializer(release_version)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
