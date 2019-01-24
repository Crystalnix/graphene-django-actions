from functools import partial

from graphene import ObjectType, Boolean, Field, NonNull, String
from graphene.types.objecttype import ObjectTypeOptions
from graphene_django.registry import get_global_registry

from graphene_django_actions import get_user
from .registry import get_action_registry


def get_model_from_type(_type):
    registry = get_global_registry()._registry
    for model, graphql_type in registry.items():
        if graphql_type._meta.name == _type:
            return model

    raise KeyError(f"There is no type {_type}")


class PermissionErrorType(ObjectType):
    message = NonNull(String)


class ObjectPermissionSetOptions(ObjectTypeOptions):
    actions = []


class AbstractObjectPermissionSet(ObjectType):
    """Base class for object permission sets.
    To generate permission fields, specify actions in the inner Meta class.

    >>>from graphene_django_actions.default_actions import ChangeAction, DeleteAction
    >>>class MyPermissionSet(AbstractObjectPermissionSet):
    >>>     class Meta:
    >>>         actions = [ChangeAction, DeleteAction]
    """

    def __init__(self, obj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.obj = obj

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        interfaces=(),
        possible_types=(),
        default_resolver=None,
        _meta=None,
        actions=None,
        **options,
    ):
        if _meta is None:
            _meta = ObjectPermissionSetOptions(cls)
        fields = _meta.fields
        if fields is None:
            fields = {}
        action_fields = cls.get_action_fields(actions)
        fields.update(action_fields)
        _meta.fields = fields
        super().__init_subclass_with_meta__(
            interfaces, possible_types, default_resolver, _meta, **options
        )

    @classmethod
    def get_action_fields(cls, actions):
        if not actions:
            action_registry = cls.get_registry()
            actions = action_registry.get_actions()
        action_fields = {}
        for action in actions:
            name = action.name.lower()
            field_args = {}
            if action.on_parent:
                field_args["args"] = {"type": cls.get_type_argument_definition()}
            field_args["resolver"] = partial(cls.resolve_permission, action)
            action_fields[name] = Field(NonNull(Boolean), **field_args)
        return action_fields

    @classmethod
    def get_type_argument_definition(cls):
        return NonNull(String)

    @classmethod
    def get_registry(cls):
        return get_action_registry()

    @classmethod
    def resolve_permission(cls, action, root, info, **kwargs):
        type_ = kwargs.get("type", None)
        obj = root.obj
        user = get_user(info)
        if type_ is not None:
            model = cls.get_model_from_type(type_)
            return action.has_permission(user, model, obj)
        return action.has_permission(user, obj)

    @classmethod
    def get_model_from_type(cls, type_):
        return get_model_from_type(type_)

    class Meta:
        abstract = True


class ObjectPermissionSet(AbstractObjectPermissionSet):
    """
    Object permission set containing permission checks for all registered actions.
    """

    pass
