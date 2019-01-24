from graphene_django.rest_framework.mutation import SerializerMutation
from graphene import ClientIDMutation, Field, Boolean, NonNull, ID
from graphene_django_actions.default_actions import (
    CreateAction,
    ChangeAction,
    DeleteAction,
)
from graphene_django_actions.mixins import (
    PermissionSerializerMutationMixin,
    PermissionMutationMixin,
)


class CreateMutation(PermissionSerializerMutationMixin, SerializerMutation):
    action = CreateAction

    class Meta:
        abstract = True


class ChangeMutation(PermissionSerializerMutationMixin, SerializerMutation):
    action = ChangeAction

    @classmethod
    def get_parent_object(cls, permission_target, info, **kwargs):
        return None

    @classmethod
    def get_permission_target(cls, info, **kwargs):
        serializer = kwargs["serializer"]
        return serializer.instance

    class Meta:
        abstract = True


class DeleteMutation(PermissionMutationMixin, ClientIDMutation):
    action = DeleteAction
    deleted = Field(Boolean)

    class Argument:
        id = NonNull(ID)

    @classmethod
    def handle_has_permission(cls, permission_target, info, **kwargs):
        permission_target.delete()
        return cls(deleted=True)

    @classmethod
    def get_permission_target(cls, info, **kwargs):
        _id = kwargs["input"]["id"]
        model = cls.get_model()
        return model.objects.get(id=_id)

    @classmethod
    def get_parent_object(cls, permission_target, info, **kwargs):
        return None

    @staticmethod
    def get_model():
        raise NotImplementedError

    class Meta:
        abstract = True
