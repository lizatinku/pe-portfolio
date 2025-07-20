# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app, TimelinePost

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        # Create tables before each test
        TimelinePost.create_table()

    def tearDown(self):
        # Drop tables after each test to keep the DB clean
        TimelinePost.drop_table()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        # Additional home page tests
        assert "timeline" in html.lower()  # Check if timeline is mentioned on the page

    def test_timeline(self):
        # GET should return empty at first
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # POST a new timeline post
        post_data = {
            "name": "Test User",
            "email": "test@example.com",
            "content": "This is a test post!"
        }
        post_response = self.client.post("/api/timeline_post", data=post_data)
        assert post_response.status_code == 200
        post_json = post_response.get_json()
        assert post_json["name"] == "Test User"
        assert post_json["email"] == "test@example.com"
        assert post_json["content"] == "This is a test post!"

        # GET should now return one post
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]["name"] == "Test User"
        assert json["timeline_posts"][0]["email"] == "test@example.com"
        assert json["timeline_posts"][0]["content"] == "This is a test post!"

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={
            "email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={
            "name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html