from operator import and_, or_


class Permission:
    def __init__(self, name=None) -> None:
        if name is None:
            self.name = self.__class__.__name__
        else:
            self.name = name

    def check(self, user, obj, **kwargs):
        """Check if the given user has a permission for the given object."""
        raise NotImplementedError

    def __or__(self, other):
        return self._combine(other, or_)

    def __and__(self, other):
        return self._combine(other, and_)

    def _combine(self, other, combination):
        def check(user, obj, **kwargs):
            first_check = self.check(user, obj, **kwargs)
            second_check = other.check(user, obj, **kwargs)
            return combination(first_check, second_check)

        combination_name = combination.__name__.strip("_")
        name = f"({self} {combination_name} {other})"
        new_permission = Permission(name=name)
        new_permission.check = check
        return new_permission

    def __str__(self) -> str:
        return self.name


class AllowAny(Permission):
    """
    Allows any user for any action.
    """

    def check(self, user, obj, **kwargs):
        return True


class DenyAny(Permission):
    """
    Deny any user for any action.
    """

    def check(self, user, obj, **kwargs):
        return False


class AllowAuthenticated(Permission):
    """
    Allows performing action only for logged in users.
    """

    def check(self, user, obj, **kwargs):
        """Perform the check."""
        return user.is_authenticated


class AllowStaff(Permission):
    """
    Allow performing action only for staff users.
    """

    def check(self, user, obj, **kwargs):
        """Perform the check."""
        return user.is_staff


class AllowSuperuser(Permission):
    """
    Allow performing action only for superusers.
    """

    def check(self, user, obj, **kwargs):
        """Perform the check."""
        return user.is_superuser
