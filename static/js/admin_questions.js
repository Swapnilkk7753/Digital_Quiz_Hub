/* ===== SAMPLE QUESTIONS ===== */
let questions = [];
fetch("/Admin_questions_d")
.then(res=>res.json())
.then(data=>{questions=data.questions;
  renderQuestions(questions);
})
.catch(err=>console.error(err))


const table = document.getElementById("questionTable");
const output = document.getElementById("questionOutput");

/* ===== RENDER QUESTIONS ===== */
function renderQuestions(data) {
  table.innerHTML = "";
  data.forEach((q, index) => {
    table.innerHTML += `
      <tr>
        <td>${index + 1}</td>
        <td>${q.quiz}</td>
        <td>${q.text}</td>
        <td><strong>${q.correct}</strong></td>
        <td class="text-center">
          <button class="btn btn-outline-danger btn-sm"
            onclick="deleteQuestion(${q.id})">
            Delete
          </button>
        </td>
      </tr>
    `;
  });
}

renderQuestions(questions);

/* ===== ADD QUESTION ===== 
function addQuestion() {
  const quiz = document.getElementById("quizSelect").value;
  const text = document.getElementById("questionText").value;
  const correct = document.getElementById("correctOption").value;

  if (!quiz || !text || !correct) return;

  questions.push({
    id: Date.now(),
    quiz,
    text,
    correct
  });

  output.innerHTML =
    `Question added successfully to <strong>${quiz}</strong>.`;

  document.getElementById("quizSelect").value = "";
  document.getElementById("questionText").value = "";
  document.getElementById("correctOption").value = "";

  renderQuestions(questions);
}*/

/* ===== DELETE QUESTION ===== */
function deleteQuestion(id) {
    fetch(`/Admin_questions_delete/${id}`,{method:"POST"})
  const q = questions.find(q => q.id === id);
  if (confirm("Delete this question?")) {
    questions = questions.filter(q => q.id !== id);
    output.innerHTML =
      `Question deleted successfully.`;
    renderQuestions(questions);
  }
}

/* ===== SEARCH ===== */
document.getElementById("searchQuestion").addEventListener("input", function () {
  const value = this.value.toLowerCase();
  const filtered = questions.filter(q =>
    q.text.toLowerCase().includes(value) ||
    q.quiz.toLowerCase().includes(value)
  );
  renderQuestions(filtered);
});
