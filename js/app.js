/* Klein Read — interactions */
(function () {
  "use strict";

  /* ---------- Reading progress bar ---------- */
  var bar = document.querySelector(".progress-bar");
  if (bar) {
    window.addEventListener("scroll", function () {
      var h = document.documentElement;
      var max = h.scrollHeight - h.clientHeight;
      bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + "%";
    }, { passive: true });
  }

  /* ---------- Paragraph panels: Translation / Words / Analysis ---------- */
  document.querySelectorAll(".tool-btn[data-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var panel = document.getElementById(btn.getAttribute("data-toggle"));
      if (!panel) return;
      var open = panel.classList.toggle("open");
      btn.classList.toggle("active", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  });

  /* ---------- Click a theme word in the text: open its note ---------- */
  document.querySelectorAll(".tword").forEach(function (el) {
    el.addEventListener("click", function () {
      var word = (el.getAttribute("data-word") || el.textContent).toLowerCase();
      var card = el.closest(".para-card");
      if (!card) return;
      var wordsBtn = card.querySelector('.tool-btn[data-toggle$="-words"]');
      var wordsPanel = wordsBtn
        ? document.getElementById(wordsBtn.getAttribute("data-toggle"))
        : null;
      if (wordsPanel && !wordsPanel.classList.contains("open")) {
        wordsPanel.classList.add("open");
        if (wordsBtn) wordsBtn.classList.add("active");
      }
      if (!wordsPanel) return;
      var target = null;
      wordsPanel.querySelectorAll(".word-list li").forEach(function (li) {
        var w = li.querySelector(".w");
        if (w && w.textContent.trim().toLowerCase() === word) target = li;
      });
      if (target) {
        target.style.outline = "3px solid var(--klein)";
        target.style.background = "var(--lemon-soft)";
        target.scrollIntoView({ behavior: "smooth", block: "nearest" });
        setTimeout(function () {
          target.style.outline = "";
          target.style.background = "";
        }, 1600);
      }
    });
  });

  /* ---------- Multiple-choice quiz ---------- */
  document.querySelectorAll(".quiz-card").forEach(function (card) {
    var answer = card.getAttribute("data-answer");
    var explain = card.querySelector(".quiz-explain");
    var options = card.querySelectorAll(".option");
    if (options.length) {
      options.forEach(function (opt, i) {
        opt.addEventListener("click", function () {
          if (card.getAttribute("data-done") === "1") return;
          card.setAttribute("data-done", "1");
          var key = String.fromCharCode(65 + i); // A B C D
          if (key === answer) {
            opt.classList.add("correct");
          } else {
            opt.classList.add("wrong");
            options.forEach(function (o, j) {
              if (String.fromCharCode(65 + j) === answer) o.classList.add("correct");
            });
          }
          options.forEach(function (o) { o.disabled = true; });
          if (explain) explain.classList.add("show");
        });
      });
    }
  });

  /* ---------- Fill-in quiz: show answer ---------- */
  document.querySelectorAll(".reveal-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var card = btn.closest(".quiz-card");
      if (!card) return;
      var input = card.querySelector(".fill-input");
      var answer = card.getAttribute("data-fill-answer") || "";
      if (input) {
        var before = input.value;
        input.value = answer;
        input.style.borderColor =
          before.trim().toLowerCase() === answer.trim().toLowerCase()
            ? "var(--mint)" : "var(--klein)";
      }
      var explain = card.querySelector(".quiz-explain");
      if (explain) explain.classList.add("show");
    });
  });

  /* ---------- Home filters: topic and source language ---------- */
  function applyFilters() {
    var topicBtn = document.querySelector('.filter-chip.active[data-topic]');
    var langBtn = document.querySelector('.filter-chip.active[data-source-lang]');
    var topic = topicBtn ? topicBtn.getAttribute("data-topic") : "all";
    var lang = langBtn ? langBtn.getAttribute("data-source-lang") : "all";
    document.querySelectorAll(".article-card").forEach(function (card) {
      var okTopic = topic === "all" || card.getAttribute("data-topic") === topic;
      var okLang = lang === "all" || card.getAttribute("data-source-lang") === lang;
      card.style.display = okTopic && okLang ? "" : "none";
    });
  }

  document.querySelectorAll(".filter-chip[data-topic]").forEach(function (chip) {
    chip.addEventListener("click", function () {
      document.querySelectorAll(".filter-chip[data-topic]").forEach(function (c) {
        c.classList.remove("active");
      });
      chip.classList.add("active");
      applyFilters();
    });
  });

  document.querySelectorAll(".filter-chip[data-source-lang]").forEach(function (chip) {
    chip.addEventListener("click", function () {
      document.querySelectorAll(".filter-chip[data-source-lang]").forEach(function (c) {
        c.classList.remove("active");
      });
      chip.classList.add("active");
      applyFilters();
    });
  });
})();
