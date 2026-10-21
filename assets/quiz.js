/* quiz.js — Quiz widget tái sử dụng cho mọi bài học.
   Cách dùng: 1) include <script src="../assets/quiz.js"></script>
              2) <div class="quiz" data-quiz-id="lesson0001"></div>
              3) định nghĩa câu hỏi trong window.QUIZZES["lesson0001"] trước khi include.
   Mỗi câu: { q, opts: [..], answer: index, explain }
   Quy ước thiết kế: các option cùng số từ để không lộ đáp án qua format. */
(function () {
  "use strict";

  function renderQuiz(container, questions) {
    var state = { answered: 0, correct: 0 };
    var scoreEl = document.createElement("div");
    scoreEl.className = "score";

    function updateScore() {
      scoreEl.textContent = "Điểm: " + state.correct + " / " + questions.length +
        (state.answered === questions.length
          ? (state.correct === questions.length ? " — Xuất sắc! 🎯" : " — Đọc lại phần giải thích rồi thử lần sau nhé.")
          : "");
    }

    questions.forEach(function (item, qi) {
      var qEl = document.createElement("div");
      qEl.className = "q";
      qEl.textContent = (qi + 1) + ". " + item.q;
      container.appendChild(qEl);

      var optsEl = document.createElement("div");
      optsEl.className = "opts";

      var explain = document.createElement("div");
      explain.className = "explain";
      explain.innerHTML = item.explain;

      item.opts.forEach(function (opt, oi) {
        var btn = document.createElement("button");
        btn.className = "opt";
        btn.type = "button";
        btn.textContent = opt;
        btn.addEventListener("click", function () {
          var buttons = optsEl.querySelectorAll("button");
          buttons.forEach(function (b) { b.disabled = true; });
          buttons[item.answer].classList.add("correct");
          if (oi === item.answer) { state.correct += 1; }
          else { btn.classList.add("wrong"); }
          state.answered += 1;
          explain.classList.add("show");
          updateScore();
        });
        optsEl.appendChild(btn);
      });

      container.appendChild(optsEl);
      container.appendChild(explain);
    });

    container.appendChild(scoreEl);
    updateScore();
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-quiz-id]").forEach(function (el) {
      var id = el.getAttribute("data-quiz-id");
      if (window.QUIZZES && window.QUIZZES[id]) {
        renderQuiz(el, window.QUIZZES[id]);
      }
    });
  });
})();
