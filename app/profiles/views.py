# /home/mint/Desktop/ArtistMgntBack/app/profiles/views.py
from asyncio.log import logger
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status
from rest_framework.response import Response

from app.core.models import User
from app.core.serializers import UserProfileSerializer, ManagerProfileSerializer
from .service import (
    create_raw_manager_profile_queries,
    get_all_raw_user_profiles_queries,
    get_raw_user_profile_list_queries,
    get_raw_user_profile_detail_queries,
    create_raw_user_profile_queries,
    update_raw_user_profile_queries,
    delete_raw_user_profile_queries,
    get_all_raw_manager_profiles_queries,
    get_raw_manager_profile_list_queries,
    get_raw_manager_profile_detail_queries,
    update_raw_manager_profile_queries,
    delete_raw_manager_profile_queries,
    get_manager_profile_by_user_id_direct,
)


class UserProfileCreateView(APIView):
    """View for creating User Profiles."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                success, data = create_raw_user_profile_queries(
                    request.user.id, serializer.validated_data
                )
                if success:
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # Log database errors
                logger.error(f"Error creating user profile: {e}")
                return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Return serializer errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileListView(APIView):
    """View for listing User Profiles."""

    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        # profile=User.objects.all()
        profiles = get_raw_user_profile_list_queries(request.user.id)
        serializer = self.serializer_class(data=profiles, many=True)
        serializer.is_valid()
        return Response(serializer.data)


class UserProfileDetailView(APIView):
    """View for retrieving, updating, or deleting a User Profile."""

    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request, pk):
        profile = get_raw_user_profile_detail_queries(request.user.id, pk)
        if profile:
            serializer = self.serializer_class(data=profile)
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            success, data = update_raw_user_profile_queries(
                request.user.id, pk, serializer.validated_data
            )
            if success:
                return Response(data)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        deleted = delete_raw_user_profile_queries(request.user.id, pk)
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class AllUserProfileListView(APIView):
    """View for listing all User Profiles."""

    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        profiles = get_all_raw_user_profiles_queries()
        serializer = self.serializer_class(data=profiles, many=True)
        serializer.is_valid()
        return Response(serializer.data)


class ManagerProfileCreateView(APIView):
    """View for creating a new Manager Profile."""

    permission_classes = [permissions.AllowAny]
    serializer_class = ManagerProfileSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            success, data = create_raw_manager_profile_queries(
                request.user.id, serializer.validated_data
            )

            if success:
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManagerProfileListView(APIView):
    """View for listing Manager Profiles."""

    permission_classes = [permissions.AllowAny]
    serializer_class = ManagerProfileSerializer

    def get(self, request):
        profiles = get_raw_manager_profile_list_queries(request.user.id)
        serializer = self.serializer_class(data=profiles, many=True)
        serializer.is_valid()
        return Response(serializer.data)


class ManagerProfileDetailView(APIView):
    """View for retrieving, updating, or deleting a Manager Profile."""

    permission_classes = [permissions.AllowAny]
    serializer_class = ManagerProfileSerializer
    def get(self, request, pk):
        profile = get_raw_manager_profile_detail_queries(request.user.id, pk)
        if profile:
            serializer = self.serializer_class(data=profile)
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        print(request.data)
        # print(request.user.id)
        # print(pk)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            success, data = update_raw_manager_profile_queries(
                request.user.id, pk, serializer.validated_data
            )
            if success:
                return Response(data)
            else:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        deleted = delete_raw_manager_profile_queries(request.user.id, pk)
        if deleted:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class AllManagerProfileListView(APIView):
    """View for listing all Manager Profiles."""

    permission_classes = [permissions.AllowAny]
    serializer_class = ManagerProfileSerializer

    def get(self, request):
        profiles = get_all_raw_manager_profiles_queries()
        # Add id to each profile dictionary
        for profile in profiles:
            profile['id'] = str(profile['id'])
        serializer = self.serializer_class(data=profiles, many=True)
        serializer.is_valid()
        return Response(serializer.data)


class ManagerProfileByUserView(APIView):
    """View for retrieving a Manager Profile by User ID."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ManagerProfileSerializer

    def get(self, request, user_id):
        """
        Retrieves the ManagerProfile associated with a given user_id.

        Args:
            request: The HTTP request object.
            user_id: The ID of the User.

        Returns:
            A Response object containing the serialized ManagerProfile data or an error response.
        """
        try:
            manager_profile = get_manager_profile_by_user_id_direct(user_id)
            if manager_profile:
                serializer = self.serializer_class(manager_profile)
                data = serializer.data
                data['manager_id'] = str(manager_profile.id) # Add manager_id to the response
                return Response(data)
            else:
                return Response({"error": f"ManagerProfile not found for user with ID {user_id}."}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": f"User with ID {user_id} not found."}, status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist:
            return Response({"error": f"ManagerProfile not found for user with ID {user_id}."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving manager profile by user ID: {e}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
