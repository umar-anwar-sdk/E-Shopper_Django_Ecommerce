from django.urls import path
from .views import (
    CustomerRegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    CustomTokenObtainPairView,
    RefreshTokenAPIView,
    ProfileAPIView,
    ChangePasswordAPIView,
    AdminCreateVendorAPIView,
    UserListAPIView,
    UserDetailAPIView,
    DeleteUserAPIView,
    VendorListAPIView,
    VendorApprovalAPIView,
    AdminDashboardStatsAPIView,
    VendorProfileAPIView,
    CustomerProfileAPIView,
)

app_name = 'authentication'

urlpatterns = [
    # Authentication URLs
    path('register/', CustomerRegisterAPIView.as_view(), name='customer-register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', RefreshTokenAPIView.as_view(), name='token-refresh'),
    
    # User Profile URLs
    path('profile/', ProfileAPIView.as_view(), name='profile'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    
    # Customer URLs
    path('customer/profile/', CustomerProfileAPIView.as_view(), name='customer-profile'),
    
    # Vendor URLs
    path('vendor/profile/', VendorProfileAPIView.as_view(), name='vendor-profile'),
    
    # Admin URLs
    path('admin/create-vendor/', AdminCreateVendorAPIView.as_view(), name='admin-create-vendor'),
    path('admin/users/', UserListAPIView.as_view(), name='user-list'),
    path('admin/users/<int:user_id>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('admin/users/<int:user_id>/delete/', DeleteUserAPIView.as_view(), name='delete-user'),
    path('admin/vendors/', VendorListAPIView.as_view(), name='vendor-list'),
    path('admin/vendors/<int:vendor_id>/approval/', VendorApprovalAPIView.as_view(), name='vendor-approval'),
    path('admin/stats/', AdminDashboardStatsAPIView.as_view(), name='admin-stats'),
]
