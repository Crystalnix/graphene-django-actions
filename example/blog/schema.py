from graphene import ObjectType, Schema, Node
from graphene_django import DjangoConnectionField

from blog.models import Post
from .object_types import PostType, UserType
from .mutations import (
    CreatePostMutation,
    ChangePostMutation,
    CreateCommentMutation,
    ChangeCommentMutation,
    DeleteCommentMutation,
    DeletePostMutation,
)


class Query(ObjectType):
    post = Node.Field(PostType)
    posts = DjangoConnectionField(PostType)

    @staticmethod
    def resolve_posts(root, info, **kwargs):
        return Post.objects.filter(is_published=True)


class Mutation(ObjectType):
    create_post = CreatePostMutation.Field()
    change_post = ChangePostMutation.Field()
    delete_post = DeletePostMutation.Field()
    create_comment = CreateCommentMutation.Field()
    change_comment = ChangeCommentMutation.Field()
    delete_comment = DeleteCommentMutation.Field()


schema = Schema(query=Query, mutation=Mutation, types=[UserType])
