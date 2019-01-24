from django.contrib.auth.models import User
from graphene import Field, Node, NonNull
from graphene_django import DjangoObjectType
from graphene_django_actions.mixins import PermissionNodeMixin
from graphene_django_actions.object_types import (
    ObjectPermissionSet,
    AbstractObjectPermissionSet,
)

from graphene_django_actions.default_actions import (
    ViewAction,
    DeleteAction,
    ChangeAction,
)
from blog.models import Post, Comment
from graphene_django_actions.fields import PermissionConnectionField


class PostType(PermissionNodeMixin, DjangoObjectType):
    permission_set = Field(NonNull(ObjectPermissionSet))
    comments = PermissionConnectionField(lambda: CommentType)

    @staticmethod
    def resolve_permission_set(post, info, **kwargs):
        return ObjectPermissionSet(post)

    class Meta:
        model = Post
        interfaces = (Node,)


class CommentPermissionSet(AbstractObjectPermissionSet):
    class Meta:
        actions = [ViewAction, DeleteAction, ChangeAction]


class CommentType(PermissionNodeMixin, DjangoObjectType):
    permission_set = Field(NonNull(CommentPermissionSet))

    @staticmethod
    def resolve_permission_set(comment, info, **kwargs):
        return CommentPermissionSet(comment)

    class Meta:
        model = Comment
        interfaces = (Node,)


class UserType(DjangoObjectType):
    class Meta:
        model = User
        only_fields = ["username"]
        interfaces = (Node,)
