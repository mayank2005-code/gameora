/* Gameora portal: search and category filtering for the server-rendered grid. */
(function () {
  "use strict";

  const grid = document.getElementById("games-grid");
  if (!grid) return;

  const cards = Array.from(grid.querySelectorAll(".game-card"));
  const chips = Array.from(document.querySelectorAll(".filter-chip"));
  const search = document.getElementById("game-search");
  const count = document.getElementById("game-count");
  const empty = document.getElementById("empty-state");

  let category = "All";

  function normalise(value) {
    return String(value || "").toLowerCase();
  }

  function applyFilters() {
    const query = normalise(search ? search.value.trim() : "");
    let visible = 0;

    cards.forEach(function (card) {
      const title = normalise(card.dataset.title);
      const description = normalise(card.dataset.description);
      const cardCategory = card.dataset.category || "";
      const matchesCategory = category === "All" || cardCategory === category;
      const matchesQuery =
        query === "" ||
        title.indexOf(query) !== -1 ||
        description.indexOf(query) !== -1 ||
        normalise(cardCategory).indexOf(query) !== -1;

      const show = matchesCategory && matchesQuery;
      card.hidden = !show;
      if (show) visible += 1;
    });

    if (count) {
      count.textContent = visible + (visible === 1 ? " game" : " games");
    }
    if (empty) {
      empty.hidden = visible !== 0;
    }
  }

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      category = chip.dataset.category || "All";

      chips.forEach(function (other) {
        const active = other === chip;
        other.classList.toggle("is-active", active);
        other.setAttribute("aria-pressed", active ? "true" : "false");
      });

      applyFilters();
    });
  });

  if (search) {
    search.addEventListener("input", applyFilters);
    search.addEventListener("search", applyFilters);
    search.addEventListener("change", applyFilters);
  }

  document.addEventListener("keydown", function (event) {
    if (event.key !== "/" || event.metaKey || event.ctrlKey || event.altKey) return;
    const target = event.target;
    const typing =
      target instanceof HTMLElement &&
      (target.tagName === "INPUT" ||
        target.tagName === "TEXTAREA" ||
        target.isContentEditable);
    if (typing || !search) return;
    event.preventDefault();
    search.focus();
  });

  applyFilters();
})();
