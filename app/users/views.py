from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from app.core.permission import IsArtistManager, IsSuperAdmin
from app.core.serializers import UserSerializer, RegisterSerializer
from .services import (
    get_raw_user_detail_queries,
    get_raw_user_list_queries,
    update_raw_user_queries,
    delete_raw_user_queries,
)


class UserListView(APIView):
    """View for listing and creating users."""

    permission_classes = [IsSuperAdmin | IsArtistManager]
    serializer_class = UserSerializer

    def get(self, request):
        users = get_raw_user_list_queries()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)


class UserDetailView(APIView):
    """View for retrieving, updating, or deleting a single user."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, pk):
        user = get_raw_user_detail_queries(pk)
        if user:
            serializer = self.serializer_class(data=user)
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            success, data = update_raw_user_queries(pk, serializer.validated_data)
            if success:
                return Response(data)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        deleted = delete_raw_user_queries(pk)
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
