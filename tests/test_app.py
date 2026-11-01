"""Smoke tests for the Gameora portal and the migrated game routes."""

import unittest

from app import app
from games import all_games


class PortalTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.update(TESTING=True)
        cls.client = app.test_client()

    def test_homepage_lists_every_game(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.count(b'class="game-card"'), len(all_games()))
        for game in all_games():
            self.assertIn(game["title"].encode(), response.data)

    def test_games_page_lists_every_game(self):
        response = self.client.get("/games")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.count(b'class="game-card"'), len(all_games()))

    def test_every_game_route_serves_the_original_game(self):
        for game in all_games():
            with self.subTest(game=game["id"]):
                response = self.client.get(f"/game/{game['id']}")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.headers.get("X-Gameora-Game"), game["id"])
                self.assertEqual(response.data.count(b"gameora:home-link"), 1)
                self.assertIn(b"</html>", response.data)

    def test_legacy_folder_aliases_still_work(self):
        for game in all_games():
            for alias in game.get("aliases", ()):
                with self.subTest(alias=alias):
                    response = self.client.get(f"/game/{alias}")
                    self.assertEqual(response.status_code, 200)

    def test_api_returns_the_catalogue(self):
        response = self.client.get("/api/games")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertEqual(payload["count"], len(all_games()))
        self.assertEqual(len(payload["games"]), len(all_games()))

    def test_portal_and_thumbnail_assets_exist(self):
        assets = [
            "/favicon.ico",
            "/static/favicon.svg",
            "/static/css/portal.css",
            "/static/js/portal.js",
        ]
        assets += [f"/static/images/{game['thumbnail']}" for game in all_games()]
        for asset in assets:
            with self.subTest(asset=asset):
                response = self.client.get(asset)
                self.assertEqual(response.status_code, 200)
                response.close()

    def test_unknown_routes_return_the_custom_404(self):
        for path in ("/game/not-a-game", "/definitely-not-a-page"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 404)
                self.assertIn(b"Page not found", response.data)


if __name__ == "__main__":
    unittest.main()
