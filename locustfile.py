from locust import HttpUser, task, between
import random


class NoteAppUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # Login and store the token
        response = self.client.post(
            "/auth/login",
            json={"username": "testuser", "password": "testpass"}
        )
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def create_note(self):
        self.client.post(
            "/notes/",
            json={
                "title": f"Test Note {random.randint(1, 1000)}",
                "content": "Test Content"
            },
            headers=self.headers
        )

    @task(2)
    def list_notes(self):
        self.client.get("/notes/", headers=self.headers)

    @task(1)
    def translate_note(self):
        # First create a note
        response = self.client.post(
            "/notes/",
            json={
                "title": "Note to Translate",
                "content": "Привет, мир!"
            },
            headers=self.headers
        )
        note_id = response.json()["id"]

        # Then translate it
        self.client.post(
            f"/notes/{note_id}/translate",
            json={"target_lang": "en"},
            headers=self.headers
        )
