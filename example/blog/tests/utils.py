from contextlib import contextmanager
import json
from django.test import TestCase


class BaseGrapheneTestCase(TestCase):
    def send_graphql_request(self, query, variables):
        data = {"query": query, "variables": variables}
        response = self.client.post(
            "/graphql/", data=json.dumps(data), content_type="application/json"
        )
        response_json = response.json()
        return response_json["data"]


@contextmanager
def assert_model_count_change(model, count_change):
    count = model.objects.count()
    yield
    change = model.objects.count() - count
    assert count_change == change
