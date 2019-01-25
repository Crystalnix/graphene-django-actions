from django_filters import FilterSet
from blog.models import Comment


class CommentFilterSet(FilterSet):
    class Meta:
        model = Comment
        fields = ["author"]
