import unittest
import pytest
import json
from app import app, db
import os


TEST_DB = "testpeterpark.sqlite3"
# os.remove(TEST_DB)


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.testing = True
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{TEST_DB}"
        db.init_app(app)
        db.create_all()
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_wrong_plate(self):
        wrong_plates = ['AAAA-AA0000', '00-AA1000', 'AA-AAA1000', 'AA-111000', 'AA-AA0000', 'AA-A10000']
        for plate in wrong_plates:
            response = self.client.post("/plate", data={"plate": plate})
            assert response.status_code == 422

    @pytest.mark.order1
    def test_correct_plate(self):
        correct_plates = ['AAA-A1000', 'A-AA100', 'AA-AA1000']
        for plate in correct_plates:
            response = self.client.post("/plate", data={"plate": plate})
            assert response.status_code == 200

    def test_get_plate(self):
        response = self.client.get("/plate")
        data = response.data.decode("utf-8").replace("'", '"')
        assert len(json.loads(data)) == 3

    def test_search_plate(self):
        response = self.client.get("/search-plate?key=AA-AA1000&levenshtein=1")
        data = response.data.decode("utf-8").replace("'", '"')
        assert len(json.loads(data)) == 2


if __name__ == "__main__":
    unittest.main()
