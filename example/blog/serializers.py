from rest_framework.serializers import ModelSerializer

from blog.models import Post, Comment


class BaseCreateSerializer(ModelSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context["request"]
        user = request.user
        attrs["author"] = user
        return attrs


class CreatePostSerializer(BaseCreateSerializer):
    class Meta:
        model = Post
        exclude = ["created_at", "author"]


class ChangePostSerializer(ModelSerializer):
    class Meta:
        model = Post
        exclude = ["author"]


class CreateCommentSerializer(BaseCreateSerializer):
    class Meta:
        model = Comment
        exclude = ["author"]


class ChangeCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ["author", "post"]
