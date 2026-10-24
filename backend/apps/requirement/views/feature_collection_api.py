from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import (
    FeatureCreateInputSerializer,
    FeatureCreateOutputSerializer,
    FeatureListOutputSerializer,
)
from ..selectors import feature_list
from ..services import feature_create


class FeatureCollectionApi(APIView):
    """List and create features in a project."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=FeatureListOutputSerializer(many=True),
        summary="List project features",
        tags=["Features"],
    )
    def get(self, request, project_id):
        """Return all features assigned to the project."""

        features = feature_list(project_id=str(project_id))
        output_serializer = FeatureListOutputSerializer(features, many=True)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=FeatureCreateInputSerializer,
        responses=FeatureCreateOutputSerializer,
        summary="Create a project feature",
        tags=["Features"],
    )
    def post(self, request, project_id):
        """Validate the feature title and delegate creation to the service."""

        input_serializer = FeatureCreateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        feature = feature_create(
            project_id=str(project_id),
            user_id=str(request.user.pk),
            title=input_serializer.validated_data["title"],
        )
        output_serializer = FeatureCreateOutputSerializer(feature)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
