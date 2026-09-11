/* FILTER QUIZZES BY CATEGORY */
function filterQuizzes() {
  const selected = document.getElementById("categoryFilter").value;
  const quizzes = document.querySelectorAll(".quiz-item");

  quizzes.forEach(quiz => {
    const category = quiz.getAttribute("data-category");

    if (selected === "all" || category === selected) {
      quiz.style.display = "block";
    } else {
      quiz.style.display = "none";
    }
  });
}

/* START QUIZ */
function startQuiz(quizName) {
  alert("Starting Quizz: " + quizName);

  // Later: redirect to quiz attempt page
  // window.location.href = "quiz_attempt.html";
}
