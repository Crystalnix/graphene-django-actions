from django.utils.timezone import now

from graphene_django_actions.permissions import Permission


class AllowAuthor(Permission):
    def check(self, user, obj, **kwargs):
        return user == self.get_author(obj)

    @staticmethod
    def get_author(obj):
        return obj.author


class AllowCommentPostAuthor(AllowAuthor):
    @staticmethod
    def get_author(comment):
        return comment.post.author


class AllowAge(Permission):
    def __init__(self, age, name=None):
        super().__init__(name)
        self.age = age

    def check(self, user, obj, **kwargs):
        return self.age >= self.get_object_age(obj)

    @staticmethod
    def get_object_age(obj):
        return now() - obj.created_at


class AllowPublished(Permission):
    def check(self, user, obj, **kwargs):
        return obj.is_published
