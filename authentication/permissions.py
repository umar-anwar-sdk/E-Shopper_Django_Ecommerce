from rest_framework import permissions


class IsAdminUserRole(permissions.BasePermission):
    """
    Permission for admin users only.
    """
    message = 'Admin access required.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin())


class IsVendorUserRole(permissions.BasePermission):
    """
    Permission for vendor users only.
    """
    message = 'Vendor access required.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_vendor())


class IsCustomerUserRole(permissions.BasePermission):
    """
    Permission for customer users only.
    """
    message = 'Customer access required.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_customer())


class IsAdminOrVendor(permissions.BasePermission):
    """
    Permission for admin or vendor users.
    """
    message = 'Vendor or Admin access required.'

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_admin() or request.user.is_vendor())
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to allow owners or admins full access.
    """
    message = 'You do not have permission to access this resource.'

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_admin():
            return True

        owner = getattr(obj, 'vendor', None) or getattr(obj, 'user', None)
        return owner == request.user


class IsVendorProductOwner(permissions.BasePermission):
    """
    Object-level permission to allow vendors to manage their own products, or admins to manage any.
    """
    message = 'You can only manage your own products.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_admin() or request.user.is_vendor()))

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin():
            return True
        return bool(request.user.is_vendor() and getattr(obj, 'vendor', None) == request.user)


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
