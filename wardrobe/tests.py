from rest_framework import status
from rest_framework.test import APITestCase

from .models import FashionRequest, Look


class GenerateLookAPITests(APITestCase):
    def test_generate_looks_endpoint_returns_three_sorted_looks(self):
        payload = {"user_input": "tenue pour un mariage en été, budget moyen"}

        response = self.client.post("/api/generate-look/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()

        self.assertIn("looks", data)
        self.assertEqual(len(data["looks"]), 3)
        self.assertLessEqual(
            data["looks"][0]["budget_rank"], data["looks"][-1]["budget_rank"]
        )

        self.assertEqual(FashionRequest.objects.count(), 1)
        self.assertEqual(Look.objects.count(), 3)
        self.assertTrue(all(look.get("image_url") for look in data["looks"]))

    def test_get_returns_recent_requests(self):
        payload = {"user_input": "tenue pour un mariage en été, budget moyen"}
        self.client.post("/api/generate-look/", payload, format="json")

        response = self.client.get("/api/generate-look/?limit=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(len(data[0]["looks"]), 3)
