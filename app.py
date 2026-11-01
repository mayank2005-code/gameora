"""Gameora - a unified Flask portal for the games from website-v2.

Run locally with:

    pip install -r requirements.txt
    python app.py

The four games are standalone HTML5 documents.  Flask serves them from
``static/games/<folder>/index.html`` without rewriting their code, and adds a
single floating "All games" link so players can always get back to the portal.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from flask import (
    Flask,
    Response,
    abort,
    jsonify,
    render_template,
    send_from_directory,
    url_for,
)

from games import all_games, categories, get_game

BASE_DIR = Path(__file__).resolve().parent
GAMES_DIR = BASE_DIR / "static" / "games"
HOME_LINK_MARKER = "<!-- gameora:home-link -->"

app = Flask(__name__)

app.config.update(TEMPLATES_AUTO_RELOAD=True)
app.json.sort_keys = False


@app.context_processor
def inject_globals():
    return {"current_year": date.today().year}


def portal_context(active_page):
    """Shared variables for the portal templates."""
    return {
        "games": all_games(),
        "categories": categories(),
        "game_count": len(all_games()),
        "active_page": active_page,
    }


def home_link_snippet():
    """A small, self-contained link injected into each standalone game page."""
    href = url_for("games_page")
    return f"""
{HOME_LINK_MARKER}
<a href="{href}" aria-label="Back to all games"
   style="position:fixed;left:14px;bottom:14px;z-index:2147483647;display:inline-flex;align-items:center;gap:6px;padding:8px 14px;border-radius:999px;background:rgba(12,18,32,.82);color:#fff;font:600 13px/1 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;text-decoration:none;box-shadow:0 4px 14px rgba(0,0,0,.35);border:1px solid rgba(255,255,255,.22);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);-webkit-tap-highlight-color:transparent;">&#8592; All games</a>
"""


def render_game_document(game):
    """Read the original game document and add the portal link to it."""
    game_path = GAMES_DIR / game["folder"] / "index.html"
    if not game_path.is_file():
        abort(404, description=f"Game files for {game['title']} could not be found.")

    html = game_path.read_text(encoding="utf-8")
    if HOME_LINK_MARKER in html:
        return html

    snippet = home_link_snippet()
    closing_body = html.lower().rfind("</body>")
    if closing_body == -1:
        return html + snippet
    return html[:closing_body] + snippet + html[closing_body:]


@app.get("/favicon.ico")
def favicon():
    """Serve the portal icon for games that do not declare their own favicon."""
    return send_from_directory(BASE_DIR / "static", "favicon.svg", mimetype="image/svg+xml")


@app.get("/")
def index():
    return render_template("index.html", **portal_context("home"))


@app.get("/games")
def games_page():
    return render_template("games.html", **portal_context("games"))


@app.get("/game/<game_id>")
def play_game(game_id):
    game = get_game(game_id)
    if game is None:
        abort(404, description=f"No game is registered with the id '{game_id}'.")

    response = Response(render_game_document(game), mimetype="text/html")
    response.headers["X-Gameora-Game"] = game["id"]
    return response


@app.get("/api/games")
def api_games():
    payload = []
    for game in all_games():
        payload.append(
            {
                "id": game["id"],
                "title": game["title"],
                "category": game["category"],
                "description": game["description"],
                "thumbnail": url_for("static", filename=f"images/{game['thumbnail']}"),
                "play_url": url_for("play_game", game_id=game["id"]),
                "aliases": list(game.get("aliases", ())),
            }
        )
    return jsonify(games=payload, count=len(payload))


@app.errorhandler(404)
def not_found(error):
    return (
        render_template(
            "404.html",
            **portal_context(None),
            message=getattr(error, "description", "That page does not exist."),
        ),
        404,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
