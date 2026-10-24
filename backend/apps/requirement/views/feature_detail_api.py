from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import FeatureUpdateInputSerializer, FeatureUpdateOutputSerializer
from ..services import feature_delete, feature_update


class FeatureDetailApi(APIView):
    """Update or soft-delete an existing project feature."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=FeatureUpdateInputSerializer,
        responses=FeatureUpdateOutputSerializer,
        summary="Update a project feature",
        tags=["Features"],
    )
    def patch(self, request, project_id, feature_id):
        """Validate the title and delegate the feature update."""

        input_serializer = FeatureUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        feature = feature_update(
            project_id=str(project_id),
            feature_id=str(feature_id),
            user_id=str(request.user.pk),
            title=input_serializer.validated_data["title"],
        )
        output_serializer = FeatureUpdateOutputSerializer(feature)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={status.HTTP_204_NO_CONTENT: None},
        summary="Delete a project feature",
        tags=["Features"],
    )
    def delete(self, request, project_id, feature_id):
        """Soft-delete the selected feature."""

        feature_delete(
            project_id=str(project_id),
            feature_id=str(feature_id),
            user_id=str(request.user.pk),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
