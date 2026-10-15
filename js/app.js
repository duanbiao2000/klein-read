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

  /* ---------- Split view: source | notes sync ---------- */
  var srcParas = Array.prototype.slice.call(document.querySelectorAll(".src-para"));
  var noteGroups = Array.prototype.slice.call(
    document.querySelectorAll(".note-group[data-para]")
  );
  var paneLeft = document.getElementById("paneLeft");
  var paneRight = document.getElementById("paneRight");
  var syncPill = document.getElementById("syncPill");
  var current = 0;

  function scrollPaneTo(pane, el) {
    if (!pane || !el) return;
    var top = el.offsetTop - pane.offsetTop - 24;
    pane.scrollTo({ top: Math.max(0, top), behavior: "smooth" });
  }

  function activate(i, from) {
    if (i < 0 || i >= srcParas.length || i >= noteGroups.length) return;
    current = i;
    srcParas.forEach(function (p, j) { p.classList.toggle("active", j === i); });
    noteGroups.forEach(function (g, j) { g.classList.toggle("active", j === i); });
    if (syncPill) syncPill.textContent = "SYNC · PARA " + (i + 1);
    if (from !== "right") scrollPaneTo(paneRight, noteGroups[i]);
    if (from !== "left") scrollPaneTo(paneLeft, srcParas[i]);
  }

  srcParas.forEach(function (p, i) {
    p.addEventListener("click", function () { activate(i, "left"); });
  });
  noteGroups.forEach(function (g, i) {
    var head = g.querySelector(".ng-head");
    if (head) head.addEventListener("click", function () { activate(i, "right"); });
  });

  /* ---------- Theme word click: flash its word note on the right ---------- */
  document.querySelectorAll(".tword").forEach(function (el) {
    el.addEventListener("click", function (e) {
      e.stopPropagation();
      var key = (el.getAttribute("data-word") || el.textContent).trim().toLowerCase();
      var para = el.closest(".src-para");
      var group = para
        ? document.getElementById("ng" + para.getAttribute("data-para"))
        : noteGroups[current];
      if (!group) return;
      group.querySelectorAll(".w-item").forEach(function (item) {
        var w = item.querySelector(".w");
        if (!w) return;
        var forms = (w.textContent + " " + (w.getAttribute("data-forms") || "")).trim().toLowerCase();
        if (forms.indexOf(key) !== -1 || key.indexOf(w.textContent.trim().toLowerCase()) !== -1) {
          item.classList.add("flash");
          item.scrollIntoView({ behavior: "smooth", block: "nearest" });
          setTimeout(function () { item.classList.remove("flash"); }, 1600);
        }
      });
    });
  });

  /* ---------- Keyboard: J / K / arrows to move, D for demo mode ---------- */
  function splitVisible() {
    var win = document.getElementById("splitWindow");
    if (!win) return false;
    var r = win.getBoundingClientRect();
    return r.bottom > 80 && r.top < window.innerHeight - 80;
  }

  document.addEventListener("keydown", function (e) {
    var tag = (e.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea") return;
    if (e.key === "j" || e.key === "J") {
      activate(current + 1);
    } else if (e.key === "k" || e.key === "K") {
      activate(current - 1);
    } else if (e.key === "d" || e.key === "D") {
      toggleDemo();
    } else if (e.key === "ArrowDown" && splitVisible()) {
      e.preventDefault(); activate(current + 1);
    } else if (e.key === "ArrowUp" && splitVisible()) {
      e.preventDefault(); activate(current - 1);
    }
  });

  /* ---------- Source font size ---------- */
  var size = 19;
  function setSize(n) {
    size = Math.min(23, Math.max(16, n));
    document.documentElement.style.setProperty("--src-size", size + "px");
  }
  var fontPlus = document.getElementById("fontPlus");
  var fontMinus = document.getElementById("fontMinus");
  if (fontPlus) fontPlus.addEventListener("click", function () { setSize(size + 1); });
  if (fontMinus) fontMinus.addEventListener("click", function () { setSize(size - 1); });

  /* ---------- Demo mode (for screen recording) ---------- */
  var demoBtn = document.getElementById("demoToggle");
  function toggleDemo() {
    document.body.classList.toggle("demo");
    var on = document.body.classList.contains("demo");
    if (demoBtn) {
      demoBtn.textContent = on ? "✕ 退出演示" : "🎬 演示模式";
      demoBtn.classList.toggle("on", on);
    }
    if (on) window.scrollTo({ top: 0, behavior: "smooth" });
  }
  if (demoBtn) demoBtn.addEventListener("click", toggleDemo);

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
    var topicBtn = document.querySelector(".filter-chip.active[data-topic]");
    var langBtn = document.querySelector(".filter-chip.active[data-source-lang]");
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

  /* Init: first paragraph active */
  if (srcParas.length) activate(0, "init");
})();
