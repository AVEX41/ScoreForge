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
        self.perf_ind3 = PerformanceIndicator.objects.create(  # perfomance indicator 2
            user=self.user2,
            name="perf_ind3",
            description="Description3",
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


class DataResponseTests(
    TrackerTestCase
):  # Tests for the fetch requests that the user can make for different pages
    # ---- Happy path tests ----
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

    # ---- Negative path testing ----
    # -- Index favourite
    def testIndexFavouritePOST(self):
        # --- handle fetch and response ---
        self.client.login(username="user1", password="password1")
        response = self.client.post(reverse("indexData"))
        self.assertEqual(response.status_code, 400)

    def testIndexFavouriteNotAuth(self):
        # --- handle fetch and response ---
        response = self.client.get(reverse("indexData"))
        self.assertEqual(response.status_code, 302)

    def testIndexFavouriteNotFav(self):
        # --- handle fetch and response ---
        self.client.login(username="user2", password="password2")
        response = self.client.get(reverse("indexData"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["error"], "No Performance indicator favourited."
        )

    # -- Manage --
    def testManagePOST(self):
        # --- handle fetch and response ---
        self.client.login(username="user1", password="password1")
        response = self.client.post(reverse("manage"))
        self.assertEqual(response.status_code, 400)

    def testManageNotAuth(self):
        # --- handle fetch and response ---
        response = self.client.get(reverse("manage"))
        self.assertEqual(response.status_code, 302)

    # -- Manage specific
    def testManageViewPOST(self):
        # --- handle fetch and response ---
        self.client.login(username="user1", password="password1")
        response = self.client.post(
            reverse("manageView", kwargs={"view": self.perf_ind2.id})
        )
        self.assertEqual(response.status_code, 400)

    def testManageViewNotAuth(self):
        # --- handle fetch and response ---
        response = self.client.get(
            reverse("manageView", kwargs={"view": self.perf_ind2.id})
        )
        self.assertEqual(response.status_code, 302)

    def testManageViewWrongUser(self):
        # --- handle fetch and response ---
        self.client.login(username="user1", password="password1")
        response = self.client.get(
            reverse("manageView", kwargs={"view": self.perf_ind3.id})
        )
        self.assertEqual(response.status_code, 400)

        # check error:
        data = response.json()
        self.assertEqual(data["error"], "Invalid Performance indicator.")


class FormTests(TrackerTestCase):  # Tests for the form routes
    # ---- Happy path testing ----
    def testNewPerfIndForm(self):
        self.client.login(username="user1", password="password1")
        # Form data
        form_data = {
            "name": "perf_ind4",
            "description": "description4",
        }
        response = self.client.post(reverse("new"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["message"], "Performance indicator created successfully."
        )
        # Check if object got created
        try:
            PerformanceIndicator.objects.get(name="perf_ind4")
        except:
            self.fail("Object was not created")

    def testNewDataPointForm(self):
        self.client.login(username="user1", password="password1")
        # Form data
        form_data = {
            "competition_type": self.perf_ind1.id,
            "score": 20,
        }
        response = self.client.post(reverse("comp_new"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Datapoint created successfully.")

        # Check if object got created
        try:
            DataPoint.objects.get(score_table=self.perf_ind1, score=20)
        except:
            self.fail("Object was not created")

    def testEditPerfIndForm(self):
        current_id = self.perf_ind1.id
        # Old object
        old = PerformanceIndicator.objects.get(id=current_id)

        self.client.login(username="user1", password="password1")
        # Form data
        form_data = {
            "submit-type": current_id,
            "name": "perf_ind5",
            "description": "description5",
        }

        self.assertEqual(1, 1)
        response = self.client.post(reverse("edit"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["message"], "Performance indicator edited successfully."
        )

        new = PerformanceIndicator.objects.get(id=current_id)

        # Assertions: object
        self.assertEqual(new.id, old.id)  # id of object
        self.assertNotEqual(new.name, old.name)  # name of objects
        self.assertNotEqual(new.description, old.description)  # description of objects

    def testEditDataPointForm(self):
        current_id = self.datap3.id
        # Old object
        old = DataPoint.objects.get(id=current_id)

        self.client.login(username="user1", password="password1")
        # Form data
        form_data = {
            "submit_type": current_id,
            "score": 20,
        }
        response = self.client.post(reverse("comp_edit"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Datapoint edited successfully.")

        new = DataPoint.objects.get(id=current_id)

        # Assertions: object
        self.assertEqual(new.id, old.id)  # id of object
        self.assertEqual(new.score_table, old.score_table)  # owner of object
        self.assertNotEqual(new.score, old.score)  # score of objects

    def testDeletePerfIndForm(self):
        test_object = PerformanceIndicator.objects.create(
            user=self.user1,
            name="perf_ind6",
            description="Description6",
            user_favourite=False,
        )
        object_id = test_object.id

        self.client.login(username="user1", password="password1")
        # Form data
        form_data = {
            "item": object_id,
        }
        response = self.client.post(reverse("delete"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["message"], "Performance indicator deleted successfully."
        )

        # Check if object
        try:
            PerformanceIndicator.objects.get(id=object_id)  # Throws error
            self.fail("Object still exist")
        except:
            self.assertTrue(True)

    def testDeleteDataPointForm(self):
        test_object = DataPoint.objects.create(score_table=self.perf_ind1, score=4)
        object_id = test_object.id

        self.client.login(username="user1", password="password1")
        # Form data
        form_data = {
            "item": object_id,
        }
        response = self.client.post(reverse("comp_delete"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "DataPoint deleted successfully.")

        # Check if object
        try:
            DataPoint.objects.get(id=object_id)  # Throws error
            self.fail("Object still exist")
        except:
            self.assertTrue(True)

    def testFormIndexFavourite(self):
        self.client.login(username="user1", password="password1")
        # Form data
        form_data = {"perf_id": self.perf_ind2.id}
        response = self.client.post(reverse("indexFav"), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Favourite edited successfully.")

        # Check if it is the only user favourite
        favourites = PerformanceIndicator.objects.filter(user_favourite=True)
        self.assertEqual(len(favourites), 1)

    # ---- Negative path testing ----
    # New Performance indicator form
    def testNewPerfIndFormNotAuth(self):
        # Form data
        form_data = {
            "name": "perf_ind4",
            "description": "description4",
        }
        response = self.client.post(reverse("new"), data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Must be logged in.")

        # Check if object were created
        try:
            PerformanceIndicator.objects.get(name="perf_ind4")
            self.fail("Object were created")
        except:
            self.assertTrue(True)

    def testNewPerfIndFormNotPost(self):
        self.client.login(username="user1", password="password1")
        # Form data
        form_data = {
            "name": "perf_ind4",
            "description": "description4",
        }
        response = self.client.get(reverse("new"), data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "POST request required.")

        # Check if object were created
        try:
            PerformanceIndicator.objects.get(name="perf_ind4")
            self.fail("Object were created")
        except:
            self.assertTrue(True)

    def testNewPerfIndFormWrongParams(self):
        self.client.login(username="user1", password="password1")
        # Form data
        form_data = {
            "wrong_name": "perf_ind4",
            "wrong_description": "description4",
        }
        response = self.client.post(reverse("new"), data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"], "Invalid performance indicator data."
        )

        # Check if object were created
        try:
            PerformanceIndicator.objects.get(name="perf_ind4")
            self.fail("Object were created")
        except:
            self.assertTrue(True)

    # New DataPoint form
    def testNewDataPointFormNotAuth(self):
        # Form data
        form_data = {
            "competition_type": self.perf_ind1.id,
            "score": 20,
        }
        response = self.client.post(reverse("comp_new"), data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Must be logged in.")

        # Check if object were created
        try:
            DataPoint.objects.get(score_table=self.perf_ind1, score=20)
            self.fail("Object were created")
        except:
            self.assertTrue(True)

    def testNewDataPointFormNotPost(self):
        self.client.login(username="user1", password="password1")
        # Form data
        form_data = {
            "competition_type": self.perf_ind1.id,
            "score": 20,
        }
        response = self.client.get(reverse("comp_new"), data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "POST request required.")

        # Check if object were created
        try:
            DataPoint.objects.get(score_table=self.perf_ind1, score=20)
            self.fail("Object were created")
        except:
            self.assertTrue(True)

    def testNewDataPointFormWrongPerfInd(self):
        self.client.login(username="user1", password="password1")
        # Form data
        form_data = {
            "wrong_competition_type": self.perf_ind1.id,
            "score": 20,
        }
        response = self.client.post(reverse("comp_new"), data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid perfomance indicator.")

        # Check if object were created
        try:
            DataPoint.objects.get(score_table=self.perf_ind1, score=20)
            self.fail("Object were created")
        except:
            self.assertTrue(True)

    def testNewDataPointFormWrongScore(self):
        self.client.login(username="user1", password="password1")
        # Form data
        form_data = {
            "competition_type": self.perf_ind1.id,
            "wrong_score": 20,
        }
        response = self.client.post(reverse("comp_new"), data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"], "Invalid data point data. Wrong parameters."
        )

        # Check if object were created
        try:
            DataPoint.objects.get(score_table=self.perf_ind1, score=20)
            self.fail("Object were created")
        except:
            self.assertTrue(True)

    # Edit Performance indicator tests
    def testEditPerfIndFormNotAuth(self):
        current_id = self.perf_ind1.id
        # Old object
        old = PerformanceIndicator.objects.get(id=current_id)

        # Form data
        form_data = {
            "submit-type": current_id,
            "name": "perf_ind5",
            "description": "description5",
        }

        self.assertEqual(1, 1)
        response = self.client.post(reverse("edit"), data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Must be logged in.")

        new = PerformanceIndicator.objects.get(id=current_id)

        # Assertions: object
        # Check if something has been changed
        self.assertEqual(new.id, old.id)  # id of object
        self.assertEqual(new.name, old.name)  # name of objects
        self.assertEqual(new.description, old.description)  # description of objects

    def testEditPerfIndFormNotPost(self):
        current_id = self.perf_ind1.id
        # Old object
        old = PerformanceIndicator.objects.get(id=current_id)

        self.client.login(username="user1", password="password1")

        # Form data
        form_data = {
            "submit-type": current_id,
            "name": "perf_ind5",
            "description": "description5",
        }

        self.assertEqual(1, 1)
        response = self.client.get(reverse("edit"), data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "POST request required.")

        new = PerformanceIndicator.objects.get(id=current_id)

        # Assertions: object
        # Check if something has been changed
        self.assertEqual(new.id, old.id)  # id of object
        self.assertEqual(new.name, old.name)  # name of objects
        self.assertEqual(new.description, old.description)  # description of objects

    def testEditPerfIndFormWrongSubmitType(self):
        current_id = self.perf_ind1.id
        # Old object
        old = PerformanceIndicator.objects.get(id=current_id)

        self.client.login(username="user1", password="password1")

        # Form data
        form_data = {
            "wrong_submit-type": current_id,
            "name": "perf_ind5",
            "description": "description5",
        }

        self.assertEqual(1, 1)
        response = self.client.post(reverse("edit"), data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"],
            "Could not find a Perfomance indicator with the specified ID and user.",
        )

        new = PerformanceIndicator.objects.get(id=current_id)

        # Assertions: object
        # Check if something has been changed
        self.assertEqual(new.id, old.id)  # id of object
        self.assertEqual(new.name, old.name)  # name of objects
        self.assertEqual(new.description, old.description)  # description of objects

    def testEditPerfIndFormWrongNames(self):
        current_id = self.perf_ind1.id
        # Old object
        old = PerformanceIndicator.objects.get(id=current_id)

        self.client.login(username="user1", password="password1")

        # Form data
        form_data = {
            "submit-type": current_id,
            "wrong_name": "perf_ind5",
            "wrong_description": "description5",
        }

        self.assertEqual(1, 1)
        response = self.client.post(reverse("edit"), data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"], "Invalid performance indicator data."
        )

        new = PerformanceIndicator.objects.get(id=current_id)

        # Assertions: object
        # Check if something has been changed
        self.assertEqual(new.id, old.id)  # id of object
        self.assertEqual(new.name, old.name)  # name of objects
        self.assertEqual(new.description, old.description)  # description of objects

    def testEditPerfIndFormWrongUser(self):
        current_id = self.perf_ind1.id
        # Old object
        old = PerformanceIndicator.objects.get(id=current_id)

        self.client.login(username="user2", password="password2")

        # Form data
        form_data = {
            "submit-type": current_id,
            "name": "perf_ind5",
            "description": "description5",
        }

        self.assertEqual(1, 1)
        response = self.client.post(reverse("edit"), data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["error"],
            "Could not find a Perfomance indicator with the specified ID and user.",
        )

        new = PerformanceIndicator.objects.get(id=current_id)

        # Assertions: object
        # Check if something has been changed
        self.assertEqual(new.id, old.id)  # id of object
        self.assertEqual(new.name, old.name)  # name of objects
        self.assertEqual(new.description, old.description)  # description of objects

    # Edit DataPoint tests
    def testEditDataPointFormNotAuth(self):
        current_id = self.datap3.id
        # Old object
        old = DataPoint.objects.get(id=current_id)

        # Form data
        form_data = {
            "submit_type": current_id,
            "score": 20,
        }
        response = self.client.post(reverse("comp_edit"), data=form_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Must be logged in.")

        new = DataPoint.objects.get(id=current_id)

        # Assertions: object
        self.assertEqual(new.id, old.id)  # id of object
        self.assertEqual(new.score_table, old.score_table)  # owner of object
        self.assertEqual(new.score, old.score)  # score of objects


class UserEditTests(TrackerTestCase): ...
