import os

os.environ["DATABASE_URL"] = 'postgresql:///cupcakes_test'

from unittest import TestCase

from app import app
from models import db, Cupcake, DEFAULT_IMAGE_URL

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image_url": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image_url": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        # "**" means "pass this dictionary as individual named params"
        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake_id = cupcake.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        """Test getting list of all cupcakes from API"""

        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [{
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image_url": "http://test.com/cupcake.jpg"
                }]
            })

    def test_get_cupcake(self):
        """Test getting a single cupcake from API"""

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image_url": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        """Test creating a cupcake"""

        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            cupcake_id = resp.json['cupcake']['id']

            # don't know what ID we'll get, make sure it's an int
            self.assertIsInstance(cupcake_id, int)

            self.assertEqual(resp.json, {
                "cupcake": {
                    "id": cupcake_id,
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image_url": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        """Test updating a cupcake"""

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.patch(
                url,
                json={
                    "flavor": "TestFlavor3",
                    "image_url": ""
                }
            )

            self.assertEqual(resp.status_code, 200)

            self.assertEqual(resp.json, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor3",
                    "size": "TestSize",
                    "rating": 5,
                    "image_url": DEFAULT_IMAGE_URL
                }
            })

            self.assertEqual(Cupcake.query.count(), 1)

    def test_update_cupcake_non_existing(self):
        """Test updating a non existing cupcake"""

        with app.test_client() as client:
            url = "/api/cupcakes/9999999"
            resp = client.patch(url, json={"flavor": "TestFlavor3"})

            self.assertEqual(resp.status_code, 404)

    def test_delete_cupcake(self):
        """Test deleting a cupcake"""

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.delete(url)

            self.assertEqual(resp.status_code, 200)

            self.assertEqual(resp.json, {
                "deleted": self.cupcake_id
            })

            self.assertEqual(Cupcake.query.count(), 0)
