from graphene import Field

from graphene_django_actions import get_user
from .default_actions import ViewAction, ListAction
from django.core.exceptions import ImproperlyConfigured
from .object_types import PermissionErrorType


class BasePermissionMixin:
    """Mixin that adds a functionality of permission checking."""

    action = None

    @classmethod
    def perform_action(cls, info, **kwargs):
        """Try to perform an action with a permission check."""
        permission_target = cls.get_permission_target(info, **kwargs)
        if cls.has_permission(permission_target, info, **kwargs):
            return cls.handle_has_permission(permission_target, info, **kwargs)
        return cls.handle_no_permission(permission_target, info, **kwargs)

    @classmethod
    def has_permission(cls, permission_target, info, **kwargs):
        """Check if the current user has permission to perform action on a target."""
        action = cls.get_action(permission_target, info, **kwargs)
        user = cls.get_user(info)
        parent_object = cls.get_parent_object(permission_target, info, **kwargs)
        return action.has_permission(user, permission_target, parent_object, **kwargs)

    @classmethod
    def get_action(cls, permission_target, info, **kwargs):
        """Get action to check permissions against."""
        action = cls.action
        if action is None:
            raise ImproperlyConfigured("You must provide an action")
        return action

    @classmethod
    def get_user(cls, info):
        """Get user from the context."""
        return get_user(info)

    @classmethod
    def handle_no_permission(cls, permission_target, info, **kwargs):
        """Execute actions if permission has not been granted."""
        raise NotImplementedError

    @classmethod
    def handle_has_permission(cls, permission_target, info, **kwargs):
        """Execute actions if permission has been granted."""
        raise NotImplementedError

    @classmethod
    def get_permission_target(cls, info, **kwargs):
        """Get object to check permissions against."""
        raise NotImplementedError

    @classmethod
    def get_parent_object(cls, permission_target, info, **kwargs):
        """Get parent object.
        Parent object is used mainly with Create and List actions, when a user tries to perform an action for some object.
        For example, the user tries to create comment for a post. In this case, we need to check permissions
        against the post, but retrieve permissions for comments.
        """
        raise NotImplementedError


class PermissionNodeMixin(BasePermissionMixin):
    """
    Permission mixin for retrieving a single node.
    """

    action = ViewAction

    @classmethod
    def get_node(cls, info, _id):
        kwargs = {"id": _id}
        return cls.perform_action(info, **kwargs)

    @classmethod
    def handle_has_permission(cls, permission_target, info, **kwargs):
        return permission_target

    @classmethod
    def handle_no_permission(cls, permission_target, info, **kwargs):
        return None

    @classmethod
    def get_permission_target(cls, info, **kwargs):
        _id = kwargs["id"]
        return super(PermissionNodeMixin, cls).get_node(info, _id)

    @classmethod
    def get_parent_object(cls, permission_target, info, **kwargs):
        return None


class BaseMutationMixin(BasePermissionMixin):
    permission_error = Field(PermissionErrorType)

    @classmethod
    def handle_no_permission(cls, permission_target, info, **kwargs):
        """Return permission error."""
        permission_error = PermissionErrorType(
            message=cls.get_permission_error_message(permission_target, info, **kwargs)
        )
        return cls(permission_error=permission_error)

    @classmethod
    def get_permission_error_message(cls, permission_target, info, **kwargs):
        return "You have no permissions to perform that action"


class PermissionMutationMixin(BaseMutationMixin):
    """
    Permission mixin for ClientIdMutation.
    """

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        kwargs = {"input": input, "root": root}
        return cls.perform_action(info, **kwargs)


class PermissionSerializerMutationMixin(BaseMutationMixin):
    """Permission mixin for serializer mutations."""

    @classmethod
    def perform_mutate(cls, serializer, info):
        kwargs = {"serializer": serializer}
        return cls.perform_action(info, **kwargs)

    @classmethod
    def handle_has_permission(cls, permission_target, info, **kwargs):
        serializer = kwargs["serializer"]
        return super(PermissionSerializerMutationMixin, cls).perform_mutate(
            serializer, info
        )


class PermissionConnectionFieldMixin(BasePermissionMixin):
    """
    Permission mixin for DjangoConnectionField.
    """

    action = ListAction

    @classmethod
    def connection_resolver(
        cls,
        resolver,
        connection,
        default_manager,
        max_limit,
        enforce_first_or_last,
        root,
        info,
        **args
    ):
        kwargs = {
            "resolver": resolver,
            "connection": connection,
            "default_manager": default_manager,
            "max_limit": max_limit,
            "enforce_first_or_last": enforce_first_or_last,
            "root": root,
        }
        kwargs.update(args)
        return cls.perform_action(info, **kwargs)

    @classmethod
    def handle_has_permission(cls, permission_target, info, **kwargs):
        return super(PermissionConnectionFieldMixin, cls).connection_resolver(
            info=info, **kwargs
        )

    @classmethod
    def get_permission_target(cls, info, **kwargs):
        default_manager = kwargs["default_manager"]
        return default_manager.model

    @classmethod
    def handle_no_permission(cls, permission_target, info, **kwargs):
        return None

    @classmethod
    def get_parent_object(cls, permission_target, info, **kwargs):
        return kwargs["root"]


class PermissionFilterConnectionFieldMixin(PermissionConnectionFieldMixin):
    """
    Permission mixin for DjangoFilterConnectionField.
    """

    @classmethod
    def connection_resolver(
        cls,
        resolver,
        connection,
        default_manager,
        max_limit,
        enforce_first_or_last,
        filterset_class,
        filtering_args,
        root,
        info,
        **args
    ):
        kwargs = {
            "resolver": resolver,
            "connection": connection,
            "default_manager": default_manager,
            "max_limit": max_limit,
            "enforce_first_or_last": enforce_first_or_last,
            "filterset_class": filterset_class,
            "filtering_args": filtering_args,
            "root": root,
        }
        kwargs.update(args)
        return cls.perform_action(info, **kwargs)
