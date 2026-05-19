from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from django.utils import timezone

from .models import CustomUser, TokenBlacklist
from .serializers import (
    CustomerRegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
    UpdateProfileSerializer,
    VendorCreateSerializer,
    CustomTokenObtainPairSerializer,
    UserSerializer,
    LogoutSerializer
)
from .permissions import IsAdmin, IsVendor, IsCustomer
from .utils import get_tokens_for_user, send_verification_email


class CustomerRegisterAPIView(APIView):
    """
    API for customer registration
    POST /api/auth/register/
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Register a new customer"""
        serializer = CustomerRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            
            return Response({
                'message': 'Customer registered successfully!',
                'user': UserSerializer(user).data,
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
    API for user login (any role)
    POST /api/auth/login/
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Login user and return tokens"""
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens_for_user(user)
            
            return Response({
                'message': 'Login successful!',
                'user': UserSerializer(user).data,
                'tokens': tokens
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    """
    API for user logout (adds token to blacklist)
    POST /api/auth/logout/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Logout user by blacklisting token"""
        try:
            refresh_token = request.data.get('refresh')
            
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Decode token to get expiry time
            try:
                token = RefreshToken(refresh_token)
                expires_at = timezone.now() + timedelta(days=7)  # Default 7 days
                
                # Blacklist the token
                TokenBlacklist.objects.create(
                    token=refresh_token,
                    user=request.user,
                    expires_at=expires_at
                )
                
                return Response(
                    {'message': 'Successfully logged out.'},
                    status=status.HTTP_200_OK
                )
            except TokenError as e:
                return Response(
                    {'error': f'Invalid token: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        except Exception as e:
            return Response(
                {'error': f'Logout failed: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    API for obtaining JWT tokens with custom claims
    POST /api/auth/token/
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RefreshTokenAPIView(TokenRefreshView):
    """
    API for refreshing JWT access token
    POST /api/auth/token/refresh/
    """
    permission_classes = [AllowAny]


class ProfileAPIView(APIView):
    """
    API to get current user profile
    GET /api/auth/profile/
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Get user profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        """Update user profile"""
        serializer = UpdateProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Profile updated successfully!',
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    """
    API to change user password
    POST /api/auth/change-password/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Change user password"""
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            return Response({
                'message': 'Password changed successfully!'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminCreateVendorAPIView(APIView):
    """
    API for admin to create vendors
    POST /api/auth/admin/create-vendor/
    Only super admins can access this
    """
    permission_classes = [IsAdmin]
    
    def post(self, request):
        """Create a new vendor (admin only)"""
        serializer = VendorCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            return Response({
                'message': 'Vendor created successfully!',
                'vendor': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(APIView):
    """
    API to list all users (admin only)
    GET /api/auth/admin/users/
    """
    permission_classes = [IsAdmin]
    
    def get(self, request):
        """Get list of all users"""
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        
        return Response({
            'count': users.count(),
            'users': serializer.data
        }, status=status.HTTP_200_OK)


class UserDetailAPIView(APIView):
    """
    API to get user details by ID (admin only)
    GET /api/auth/admin/users/{id}/
    """
    permission_classes = [IsAdmin]
    
    def get(self, request, user_id):
        """Get user details"""
        try:
            user = CustomUser.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class DeleteUserAPIView(APIView):
    """
    API to delete user (admin only)
    DELETE /api/auth/admin/users/{id}/
    """
    permission_classes = [IsAdmin]
    
    def delete(self, request, user_id):
        """Delete a user"""
        try:
            user = CustomUser.objects.get(id=user_id)
            
            # Prevent deleting self
            if user.id == request.user.id:
                return Response(
                    {'error': 'You cannot delete your own account.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.delete()
            return Response(
                {'message': 'User deleted successfully.'},
                status=status.HTTP_200_OK
            )
        
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class VendorListAPIView(APIView):
    """
    API to list all vendors (admin only)
    GET /api/auth/admin/vendors/
    """
    permission_classes = [IsAdmin]
    
    def get(self, request):
        """Get list of all vendors"""
        vendors = CustomUser.objects.filter(role='vendor')
        serializer = UserSerializer(vendors, many=True)
        
        return Response({
            'count': vendors.count(),
            'vendors': serializer.data
        }, status=status.HTTP_200_OK)


class VendorApprovalAPIView(APIView):
    """
    API for admin to approve or reject vendor accounts.
    PATCH /api/auth/admin/vendors/{vendor_id}/approval/
    """
    permission_classes = [IsAdmin]

    def patch(self, request, vendor_id):
        try:
            vendor = CustomUser.objects.get(id=vendor_id, role='vendor')
        except CustomUser.DoesNotExist:
            return Response({'error': 'Vendor not found.'}, status=status.HTTP_404_NOT_FOUND)

        approval = request.data.get('approved')
        if approval is None:
            return Response(
                {'error': 'Please provide approved=true or approved=false.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        approved = str(approval).lower() in ['true', '1', 'yes', 'approved']
        vendor.is_verified = approved
        vendor.save(update_fields=['is_verified'])

        status_text = 'approved' if vendor.is_verified else 'rejected'
        return Response({
            'message': f'Vendor successfully {status_text}.',
            'vendor': UserSerializer(vendor).data
        }, status=status.HTTP_200_OK)


class AdminDashboardStatsAPIView(APIView):
    """
    API for admin dashboard statistics
    GET /api/auth/admin/stats/
    """
    permission_classes = [IsAdmin]
    
    def get(self, request):
        """Get dashboard statistics"""
        total_users = CustomUser.objects.count()
        total_admins = CustomUser.objects.filter(role='admin').count()
        total_vendors = CustomUser.objects.filter(role='vendor').count()
        total_customers = CustomUser.objects.filter(role='customer').count()
        
        return Response({
            'total_users': total_users,
            'total_admins': total_admins,
            'total_vendors': total_vendors,
            'total_customers': total_customers,
            'users_by_role': {
                'admin': total_admins,
                'vendor': total_vendors,
                'customer': total_customers
            }
        }, status=status.HTTP_200_OK)


class VendorProfileAPIView(APIView):
    """
    API for vendors to view their profile
    GET /api/auth/vendor/profile/
    """
    permission_classes = [IsVendor]
    
    def get(self, request):
        """Get vendor profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        """Update vendor profile"""
        serializer = UpdateProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Vendor profile updated successfully!',
                'vendor': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerProfileAPIView(APIView):
    """
    API for customers to view their profile
    GET /api/auth/customer/profile/
    """
    permission_classes = [IsCustomer]
    
    def get(self, request):
        """Get customer profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
