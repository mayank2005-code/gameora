"""Central catalogue of every game migrated from the original website.

The original project (``workspace (3)/website-v2``) kept its catalogue in a
JavaScript array.  Flask is now the single source of truth: add an entry here
and the homepage, games page and routes all pick it up automatically.

Each game is a self-contained HTML5 document stored under
``static/games/<folder>/index.html``.  The files themselves are untouched, so
their artwork, animation, scoring and game logic stay exactly as authored.
"""

from __future__ import annotations

GAMES = [
    {
        "id": "block-blaster",
        "aliases": ("game-1",),
        "folder": "game-1",
        "title": "Block Blaster",
        "category": "Arcade",
        "description": (
            "Drag colourful blocks onto the 8x8 board, fill complete rows or "
            "columns to blast them, and chain clears for huge combo scores."
        ),
        "thumbnail": "game-1.png",
        "accent": "#4dabf7",
        "controls": [
            "Drag a block from the tray onto the board",
            "Fill a full row or column to clear it",
            "Clear several lines at once for combo multipliers",
        ],
        "highlights": ["Endless mode", "Combo scoring", "Best score saved locally"],
    },
    {
        "id": "sudoku",
        "aliases": ("game-2",),
        "folder": "game-2",
        "title": "Sudoku",
        "category": "Puzzle",
        "description": (
            "A freshly generated 9x9 logic puzzle with four difficulty levels, "
            "pencil notes, hints, undo, a timer and mistake tracking."
        ),
        "thumbnail": "game-2.png",
        "accent": "#ff5a41",
        "controls": [
            "Click a cell, then type or tap a digit",
            "Use Notes to pencil in candidates",
            "Press H for a hint and U to undo",
        ],
        "highlights": ["Four difficulties", "Unique-solution generator", "Keyboard friendly"],
    },
    {
        "id": "subway-dash",
        "aliases": ("game-3", "metro-rush"),
        "folder": "game-3",
        "title": "Subway Dash",
        "category": "Action",
        "description": (
            "An endless three-lane runner. Dodge trains, jump hurdles, roll "
            "under signs, and collect coins and power-ups as the speed climbs."
        ),
        "thumbnail": "game-3.png",
        "accent": "#ffcf3f",
        "controls": [
            "Left / Right arrows switch track",
            "Up arrow or Space jumps",
            "Down arrow rolls under obstacles",
        ],
        "highlights": ["Endless runner", "Power-ups", "Crew customisation"],
    },
    {
        "id": "memory-match",
        "aliases": ("game-4",),
        "folder": "game-4",
        "title": "Memory Match",
        "category": "Puzzle",
        "description": (
            "Flip cards two at a time to find every matching pair. Pick Easy, "
            "Classic or Expert and race the clock for your best time."
        ),
        "thumbnail": "game-4.jpeg",
        "accent": "#ff6a5c",
        "controls": [
            "Flip two cards to reveal their symbols",
            "Matched pairs stay face up",
            "Clear the deck in as few moves as possible",
        ],
        "highlights": ["Three deck sizes", "Star ratings", "Best times saved locally"],
    },
]

GAME_BY_ID = {}
for _game in GAMES:
    GAME_BY_ID[_game["id"]] = _game
    for _alias in _game.get("aliases", ()):
        GAME_BY_ID[_alias] = _game

CATEGORIES = []
for _game in GAMES:
    if _game["category"] not in CATEGORIES:
        CATEGORIES.append(_game["category"])


def get_game(game_id):
    """Return a game by its URL id or any of its legacy aliases."""
    return GAME_BY_ID.get(game_id)


def all_games():
    """Return every registered game in display order."""
    return list(GAMES)


def categories():
    """Return the unique categories in catalogue order."""
    return list(CATEGORIES)
