from datetime import timedelta

from django.contrib.auth.models import User
from django.utils.timezone import now

from .utils import BaseGrapheneTestCase, assert_model_count_change
from graphene.relay.node import to_global_id
from model_mommy import mommy
from blog.models import Post, Comment


class BaseCommentTest(BaseGrapheneTestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.published_post = mommy.make(Post, is_published=True)
        self.not_published_post = mommy.make(Post, is_published=False)
        self.comment = mommy.make(Comment, post=self.published_post)

    @staticmethod
    def get_post_id(post):
        return to_global_id("PostType", post.id)

    @staticmethod
    def get_comment_id(comment):
        return to_global_id("CommentType", comment.id)


class CommentQueryTest(BaseCommentTest):
    def test_get_comment(self):
        comment = self.get_comment(self.comment)
        self.assertTrue(comment)

    def test_unauthorized_permission_set(self):
        permission_set = self.get_permission_set(self.comment)
        self.assertEqual(
            permission_set, {"view": True, "change": False, "delete": False}
        )

    def test_authorized_permission_set(self):
        self.client.force_login(self.user)
        permission_set = self.get_permission_set(self.comment)
        self.assertEqual(
            permission_set, {"view": True, "change": False, "delete": False}
        )

    def test_author_permission_set(self):
        comment = self.comment
        author = comment.author
        self.client.force_login(author)
        permission_set = self.get_permission_set(comment)
        self.assertEqual(permission_set, {"view": True, "change": True, "delete": True})

    def test_post_author_permission_set(self):
        comment = self.comment
        post = comment.post
        author = post.author
        self.client.force_login(author)
        permission_set = self.get_permission_set(comment)
        self.assertEqual(
            permission_set, {"view": True, "change": False, "delete": True}
        )

    def get_permission_set(self, comment):
        permission_set = """
            permissionSet {
                view
                change
                delete
            }
        """
        comment_data = self.get_comment(comment, permission_set)
        return comment_data["permissionSet"]

    def get_comment(self, comment, subselection="id"):
        global_id = self.get_comment_id(comment)
        query = (
            """
            query getComment($id: ID!) {
                comment(id: $id) {
                    %s
                }
            }
        """
            % subselection
        )
        variables = {"id": global_id}
        data = self.send_graphql_request(query, variables)
        return data["comment"]


class CommentMutationTest(BaseCommentTest):
    def test_unauthorized_create_comment(self):
        with assert_model_count_change(Comment, 0):
            mutation = self.create_comment(self.published_post)
        self.assertTrue(mutation["permissionError"])

    def test_authorized_create_comment(self):
        self.client.force_login(self.user)
        with assert_model_count_change(Comment, 1):
            mutation = self.create_comment(self.published_post)
        self.assertIsNone(mutation["permissionError"])

    def test_authorized_create_comment_for_not_published_post(self):
        self.client.force_login(self.user)
        with assert_model_count_change(Comment, 0):
            mutation = self.create_comment(self.not_published_post)
        self.assertTrue(mutation["permissionError"])

    def test_unauthorized_change_comment(self):
        mutation = self.change_comment(self.comment)
        self.assertTrue(mutation["permissionError"])

    def test_authorized_change_comment(self):
        self.client.force_login(self.user)
        mutation = self.change_comment(self.comment)
        self.assertTrue(mutation["permissionError"])

    def test_author_change_comment(self):
        comment = self.comment
        self.client.force_login(comment.author)
        mutation = self.change_comment(comment)
        self.assertIsNone(mutation["permissionError"])

    def test_unauthorized_delete_comment(self):
        with assert_model_count_change(Comment, 0):
            mutation = self.delete_comment(self.comment)
        self.assertTrue(mutation["permissionError"])

    def test_authorized_delete_comment(self):
        self.client.force_login(self.user)
        with assert_model_count_change(Comment, 0):
            mutation = self.delete_comment(self.comment)
        self.assertTrue(mutation["permissionError"])

    def test_author_delete_comment(self):
        comment = self.comment
        self.client.force_login(comment.author)
        with assert_model_count_change(Comment, -1):
            mutation = self.delete_comment(comment)
        self.assertIsNone(mutation["permissionError"])

    def create_comment(self, post):
        query = """
            mutation createComment($input: CreateCommentMutationInput!) {
                createComment(input: $input) {
                    id
                    permissionError {
                        message
                    }
                }
            }
        """
        variables = {"input": {"body": "Body", "post": str(post.id)}}
        data = self.send_graphql_request(query, variables)
        return data["createComment"]

    def change_comment(self, comment):
        query = """
            mutation changeComment($input: ChangeCommentMutationInput!) {
                changeComment(input: $input) {
                    id
                    body
                    permissionError {
                        message
                    }
                }
            }
        """
        variables = {"input": {"id": str(comment.id), "body": "Changed body"}}
        data = self.send_graphql_request(query, variables)
        return data["changeComment"]

    def delete_comment(self, comment):
        query = """
            mutation deleteComment($input: DeleteCommentMutationInput!) {
                deleteComment(input: $input) {
                    deleted
                    permissionError {
                        message
                    }
                }
            }
        """
        variables = {"input": {"id": str(comment.id)}}
        data = self.send_graphql_request(query, variables)
        return data["deleteComment"]
