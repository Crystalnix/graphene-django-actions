from rest_framework.serializers import ModelSerializer

from blog.models import Post, Comment


class BaseCreateSerializer(ModelSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        request = self.context["request"]
        user = request.user
        attrs["author"] = user
        return attrs

    class Meta:
        exclude = ["author"]


class CreatePostSerializer(BaseCreateSerializer):
    class Meta(BaseCreateSerializer.Meta):
        model = Post


class ChangePostSerializer(ModelSerializer):
    class Meta:
        model = Post
        exclude = ["author"]


class CreateCommentSerializer(BaseCreateSerializer):
    class Meta(BaseCreateSerializer.Meta):
        model = Comment


class ChangeCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ["author"]
