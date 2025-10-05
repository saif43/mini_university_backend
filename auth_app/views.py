from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer,
    ChangePasswordSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    # @swagger_auto_schema(
    #     operation_description="Register a new user",
    #     responses={
    #         201: openapi.Response(
    #             description="User created successfully",
    #             schema=openapi.Schema(
    #                 type=openapi.TYPE_OBJECT,
    #                 properties={
    #                     'message': openapi.Schema(type=openapi.TYPE_STRING),
    #                     'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
    #                 }
    #             )
    #         )
    #     }
    # )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully',
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(TokenObtainPairView):
    """User login endpoint that returns JWT tokens"""
    permission_classes = [permissions.AllowAny]

    # @swagger_auto_schema(
    #     operation_description="Login user and get JWT tokens",
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         required=['username', 'password'],
    #         properties={
    #             'username': openapi.Schema(type=openapi.TYPE_STRING),
    #             'password': openapi.Schema(type=openapi.TYPE_STRING),
    #         }
    #     ),
    #     responses={
    #         200: openapi.Response(
    #             description="Login successful",
    #             schema=openapi.Schema(
    #                 type=openapi.TYPE_OBJECT,
    #                 properties={
    #                     'access': openapi.Schema(type=openapi.TYPE_STRING),
    #                     'refresh': openapi.Schema(type=openapi.TYPE_STRING),
    #                     'user': openapi.Schema(
    #                         type=openapi.TYPE_OBJECT,
    #                         properties={
    #                             'id': openapi.Schema(type=openapi.TYPE_INTEGER),
    #                             'username': openapi.Schema(type=openapi.TYPE_STRING),
    #                             'email': openapi.Schema(type=openapi.TYPE_STRING),
    #                             'first_name': openapi.Schema(type=openapi.TYPE_STRING),
    #                             'last_name': openapi.Schema(type=openapi.TYPE_STRING),
    #                         }
    #                     )
    #                 }
    #             )
    #         )
    #     }
    # )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # Get user data
            username = request.data.get('username')
            user = User.objects.get(username=username)
            user_serializer = UserProfileSerializer(user)
            
            # Add user data to response
            response.data['user'] = user_serializer.data
        
        return response


class UserLogoutView(APIView):
    """User logout endpoint that blacklists refresh token"""
    permission_classes = [permissions.IsAuthenticated]

    # @swagger_auto_schema(
    #     operation_description="Logout user by blacklisting refresh token",
    #     request_body=openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         required=['refresh'],
    #         properties={
    #             'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
    #         }
    #     ),
    #     responses={
    #         200: openapi.Response(description="Logged out successfully"),
    #         400: openapi.Response(description="Invalid token")
    #     }
    # )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile endpoint"""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    # @swagger_auto_schema(operation_description="Get user profile")
    # def get(self, request, *args, **kwargs):
    #     return super().get(request, *args, **kwargs)

    # @swagger_auto_schema(operation_description="Update user profile")
    # def patch(self, request, *args, **kwargs):
    #     return super().patch(request, *args, **kwargs)


class ChangePasswordView(APIView):
    """Change password endpoint"""
    permission_classes = [permissions.IsAuthenticated]

    # @swagger_auto_schema(
    #     operation_description="Change user password",
    #     request_body=ChangePasswordSerializer,
    #     responses={
    #         200: openapi.Response(description="Password changed successfully"),
    #         400: openapi.Response(description="Invalid data")
    #     }
    # )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@swagger_auto_schema(
    operation_description="Check if user is authenticated",
    responses={
        200: openapi.Response(
            description="Authentication status",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'authenticated': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    'user': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'username': openapi.Schema(type=openapi.TYPE_STRING),
                            'email': openapi.Schema(type=openapi.TYPE_STRING),
                        }
                    )
                }
            )
        )
    }
)
def auth_status(request):
    """Check authentication status"""
    user_serializer = UserProfileSerializer(request.user)
    return Response({
        'authenticated': True,
        'user': user_serializer.data
    })
