from inspect import isclass

from .registry import get_action_registry


class Action:
    """Action class serves as a registry for model permissions."""

    def __init__(
        self, name, on_parent=False, register=True, registry_fabric=get_action_registry
    ):
        self.name = name
        self.on_parent = on_parent
        self._permission_registry = {}
        if register:
            action_registry = registry_fabric()
            action_registry.register(self)

    def add_permission(self, model, permission):
        """Add a permission check for a model type."""
        if model not in self._permission_registry:
            self._permission_registry[model] = []
        self._permission_registry[model].append(permission)

    def set_permissions(self, model, permissions):
        """Set permission checks for a model type."""
        self._permission_registry[model] = permissions

    def get_permissions(self, model):
        """Get permission checks for a model type."""
        return self._permission_registry.get(model, [])

    def has_permission(self, user, target, parent_object=None, **kwargs):
        """Check if a user has a permission to perform the action on a target.
        If a parent object is provided, permissions of the target are checked against the parent object.
        """
        model_type = self.get_model_type(target)
        if parent_object is not None:
            target = parent_object
        permissions = self.get_permissions(model_type)
        if not permissions:
            return False
        for permission in permissions:
            if not permission.check(user, target, **kwargs):
                return False
        return True

    @staticmethod
    def get_model_type(target_source):
        if isclass(target_source):
            return target_source
        return target_source._meta.model

    def __eq__(self, o):
        if not isinstance(o, Action):
            return False
        return self.name == o.name

    def __str__(self) -> str:
        return self.name
