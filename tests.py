from unittest import TestCase
from flask import jsonify
from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_testdb'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5.0,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10.0,
    "image": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data / set app context"""
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        Cupcake.query.delete()

        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions / clear app context"""
        db.session.rollback()
        self.app_context.pop()

    def test_list_cupcakes(self):

        with self.app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json

            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

            # db.session.rollback()

    def test_get_cupcake(self):

        with self.app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):

        with self.app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10.0,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):

        with self.app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            json = {"flavor": "Updated Flavor", "size": "TestSize",
                    "rating": "5", "image": "http://test.com/cupcake2.jpg"}
            resp = client.patch(url, json=json)

            data = resp.json

            self.assertEqual(resp.status_code, 200)

            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']
            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "Updated Flavor",
                    "size": "TestSize",
                    "rating": 5.0,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

    def test_delete(self):

        with self.app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"

            resp = client.delete(url)

            data = resp.json

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(data, {"message": "Deleted"})

    def test_404(self):
        with self.app.test_client() as client:
            cupcake_detail_get = client.get('/api/cupcakes/1000')
            html = cupcake_detail_get.get_data(as_text=True)
            self.assertIn('404', html)

            cupcake_detail_patch = client.patch('/api/cupcakes/1000')
            html1 = cupcake_detail_patch.get_data(as_text=True)
            self.assertIn('404', html1)

            cupcake_delete = client.delete('/api/cupcakes/1000')
            html2 = cupcake_delete.get_data(as_text=True)
            self.assertIn('404', html2)
