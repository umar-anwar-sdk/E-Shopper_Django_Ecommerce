from rest_framework import permissions

from .constants import ROLES


def has_user_role(user, role_name):
    """Return whether the user has the requested role."""
    if not user or not user.is_authenticated:
        return False

    role_accessor = getattr(user, f'is_{role_name}', None)
    if not callable(role_accessor):
        return False

    return bool(role_accessor())


def has_any_role(user, role_names):
    """Return whether the user has any of the requested roles."""
    return any(has_user_role(user, role_name) for role_name in role_names)


def is_vendor_approved(user):
    """Vendor accounts must be approved before accessing protected resources."""
    return has_user_role(user, ROLES['vendor']) and getattr(user, 'is_verified', False)


class IsAdminUserRole(permissions.BasePermission):
    """Permission for admin users only."""
    message = 'Admin access required.'

    def has_permission(self, request, view):
        return has_user_role(request.user, ROLES['admin'])


class IsVendorUserRole(permissions.BasePermission):
    """Permission for approved vendor users only."""
    message = 'Vendor access required.'

    def has_permission(self, request, view):
        return is_vendor_approved(request.user)


class IsCustomerUserRole(permissions.BasePermission):
    """Permission for customer users only."""
    message = 'Customer access required.'

    def has_permission(self, request, view):
        return has_user_role(request.user, ROLES['customer'])


class IsAdminOrVendor(permissions.BasePermission):
    """Permission for admin or approved vendor users."""
    message = 'Vendor or Admin access required.'

    def has_permission(self, request, view):
        if has_user_role(request.user, ROLES['admin']):
            return True
        return is_vendor_approved(request.user)


class IsOwnerOrAdmin(permissions.BasePermission):
    """Object-level permission allowing resource owners or admins full access."""
    message = 'You do not have permission to access this resource.'

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if has_user_role(request.user, ROLES['admin']):
            return True

        owner = getattr(obj, 'vendor', None) or getattr(obj, 'user', None)
        return owner == request.user


class IsVendorProductOwner(permissions.BasePermission):
    """Permission for admins or approved vendors managing their own products."""
    message = 'You can only manage your own products.'

    def has_permission(self, request, view):
        return has_any_role(request.user, [ROLES['admin'], ROLES['vendor']])

    def has_object_permission(self, request, view, obj):
        if has_user_role(request.user, ROLES['admin']):
            return True
        return is_vendor_approved(request.user) and getattr(obj, 'vendor', None) == request.user


class IsAdmin(IsAdminUserRole):
    """Compatibility alias for existing admin permission names."""
    pass


class IsVendor(IsVendorUserRole):
    """Compatibility alias for existing vendor permission names."""
    pass


class IsCustomer(IsCustomerUserRole):
    """Compatibility alias for existing customer permission names."""
    pass


class IsVendorOrAdmin(IsAdminOrVendor):
    """Compatibility alias for vendor-or-admin permission name."""
    pass
