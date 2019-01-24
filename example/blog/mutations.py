from blog.base_mutations import CreateMutation, ChangeMutation, DeleteMutation
from blog.models import Post, Comment
from blog.serializers import (
    CreatePostSerializer,
    CreateCommentSerializer,
    ChangePostSerializer,
    ChangeCommentSerializer,
)


class CreatePostMutation(CreateMutation):
    @classmethod
    def get_permission_target(cls, info, **kwargs):
        return Post

    @classmethod
    def get_parent_object(cls, permission_target, info, **kwargs):
        return None

    class Meta:
        serializer_class = CreatePostSerializer
        model_operations = ["create"]


class CreateCommentMutation(CreateMutation):
    @classmethod
    def get_parent_object(cls, permission_target, info, **kwargs):
        serializer = kwargs["serializer"]
        return serializer.validated_data["post"]

    @classmethod
    def get_permission_target(cls, info, **kwargs):
        return Comment

    class Meta:
        serializer_class = CreateCommentSerializer
        model_operations = ["create"]


class ChangePostMutation(ChangeMutation):
    class Meta:
        serializer_class = ChangePostSerializer
        model_operations = ["update"]


class ChangeCommentMutation(ChangeMutation):
    class Meta:
        serializer_class = ChangeCommentSerializer
        model_operations = ["update"]


class DeletePostMutation(DeleteMutation):
    @staticmethod
    def get_model():
        return Post


class DeleteCommentMutation(DeleteMutation):
    @staticmethod
    def get_model():
        return Comment
