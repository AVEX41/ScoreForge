from django.test import TestCase
from django.urls import reverse

from .models import User, PerformanceIndicator, DataPoint


class TrackerTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", password="password1"
        )  # user 1
        self.user2 = User.objects.create_user(
            username="user2", password="password2"
        )  # user 2
        self.perf_ind1 = PerformanceIndicator.objects.create(  # perfomance indicator 1
            user=self.user1,
            name="perf_ind1",
            description="Description1",
            user_favourite=True,
        )
        self.perf_ind2 = PerformanceIndicator.objects.create(  # perfomance indicator 2
            user=self.user1,
            name="perf_ind2",
            description="Description2",
            user_favourite=False,
        )
        self.datap1 = DataPoint.objects.create(  # datapoint 1:1
            score_table=self.perf_ind1,
            score=10,
        )
        self.datap2 = DataPoint.objects.create(  # datapoint 1:2
            score_table=self.perf_ind1,
            score=9,
        )
        self.datap3 = DataPoint.objects.create(  # datapoint 1:3
            score_table=self.perf_ind1,
            score=11,
        )
        self.datap4 = DataPoint.objects.create(  # datapoint 2:1
            score_table=self.perf_ind2,
            score=8,
        )


class HTMLresponseTests(TrackerTestCase):  # Tests for HTML responses
    def testUserHasLoggedIn(self):
        self.client.login(username="user1", password="password1")
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def testUserHasNotLoggedIn(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 302)


class DataRespnseTests(
    TrackerTestCase
):  # Tests for the fetch requests that the user can make for different pages
    def testIndexFavourite(self):
        # --- handle fetch and response ---
        self.client.login(username="user1", password="password1")
        response = self.client.get(reverse("indexData"))
        self.assertEqual(response.status_code, 200)

        # --- Data ---
        # get data from response
        data = response.json()

        # Check if it is the correct perfomance indicator
        self.assertEqual(data["perf_indicator_id"], "perf_ind1")

        # Check if score is correct
        dataPoints = data["perf_indicator"]
        self.assertEqual(dataPoints[0]["fields"]["score"], 10)
        self.assertEqual(dataPoints[1]["fields"]["score"], 9)
        self.assertEqual(dataPoints[2]["fields"]["score"], 11)

    def testManage(self):
        # --- handle fetch and response ---
        self.client.login(username="user1", password="password1")
        response = self.client.get(reverse("manage"))
        self.assertEqual(response.status_code, 200)

        # --- Data ---
        # get data from response
        data = response.json()

        # Check if score is correct
        PerformanceIndicators = data["competition_types"]

        # First
        self.assertEqual(PerformanceIndicators[0]["name"], "perf_ind1")
        self.assertEqual(PerformanceIndicators[0]["description"], "Description1")
        self.assertEqual(PerformanceIndicators[0]["user_favourite"], True)

        # Second
        self.assertEqual(PerformanceIndicators[1]["name"], "perf_ind2")
        self.assertEqual(PerformanceIndicators[1]["description"], "Description2")
        self.assertEqual(PerformanceIndicators[1]["user_favourite"], False)

    def testManageSpecific1(self):
        # --- handle fetch and response ---
        self.client.login(username="user1", password="password1")
        response = self.client.get(
            reverse("manageView", kwargs={"view": self.perf_ind1.id})
        )
        self.assertEqual(response.status_code, 200)

        # --- Data ---
        # get data from response
        data = response.json()

        # Check if it is the correct perfomance indicator
        self.assertEqual(data["performance_indicator_name"], self.perf_ind1.name)
        self.assertEqual(data["performance_indicator_id"], self.perf_ind1.id)
        self.assertEqual(
            data["performance_indicator_description"], self.perf_ind1.description
        )

        # Check if score is correct
        dataPoints = data["data_points"]
        stored_datapoints = DataPoint.objects.filter(score_table=self.perf_ind1.id)
        for index, datapoint in enumerate(stored_datapoints):
            self.assertEqual(dataPoints[index]["fields"]["score"], datapoint.score)

    def testManageSpecific2(self):
        # --- handle fetch and response ---
        self.client.login(username="user1", password="password1")
        response = self.client.get(
            reverse("manageView", kwargs={"view": self.perf_ind2.id})
        )
        self.assertEqual(response.status_code, 200)

        # --- Data ---
        # get data from response
        data = response.json()

        # Check if it is the correct perfomance indicator
        self.assertEqual(data["performance_indicator_name"], self.perf_ind2.name)
        self.assertEqual(data["performance_indicator_id"], self.perf_ind2.id)
        self.assertEqual(
            data["performance_indicator_description"], self.perf_ind2.description
        )

        # Check if score is correct
        dataPoints = data["data_points"]
        stored_datapoints = DataPoint.objects.filter(score_table=self.perf_ind2.id)
        for index, datapoint in enumerate(stored_datapoints):
            self.assertEqual(dataPoints[index]["fields"]["score"], datapoint.score)
