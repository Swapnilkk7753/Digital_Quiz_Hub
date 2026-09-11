/* ===== SAMPLE QUIZ DATA ===== */
let quizzes = [];
fetch("/Admin_quizzes_d")
.then(res=>res.json())
.then(data=>{quizzes=data.quizzes;
  renderQuizzes(quizzes);
})
.catch(err=>console.error(err))


const quizTable = document.getElementById("quizTable");
const output = document.getElementById("quizOutput");

/* ===== RENDER QUIZZES ===== */
function renderQuizzes(data) {
  quizTable.innerHTML = "";
  data.forEach((quiz, index) => {
    quizTable.innerHTML += `
      <tr>
        <td>${index + 1}</td>
        <td>${quiz.title}</td>
        <td>${quiz.category}</td>
        <td>${quiz.time} min</td>
        <td>
          <span class="badge ${quiz.active ? "badge-active" : "badge-inactive"}">
            ${quiz.active ? "Active" : "Inactive"}
          </span>
        </td>
        <td>
          <button class="btn btn-outline-primary btn-sm"
            onclick="toggleQuiz(${quiz.id})">
            ${quiz.active ? "Disable" : "Enable"}
          </button>

          <button class="btn btn-outline-danger btn-sm"
            onclick="deleteQuiz(${quiz.id})">
            Delete
          </button>
        </td>
      </tr>
    `;
  });
}

//renderQuizzes(quizzes);

/* ===== ADD QUIZ ===== 
function addQuiz() {
  const title = document.getElementById("quizTitle").value.trim();
  const category = document.getElementById("quizCategory").value;
  const time = document.getElementById("quizTime").value;

  if (!title || !category || !time) return;

  quizzes.push({
    id: Date.now(),
    title,
    category,
    time,
    active: true
  });

  output.innerHTML =
    `Quiz <strong>${title}</strong> added successfully.`;

  document.getElementById("quizTitle").value = "";
  document.getElementById("quizCategory").value = "";
  document.getElementById("quizTime").value = "";

  renderQuizzes(quizzes);
}*/

/* ===== TOGGLE QUIZ ===== */
function toggleQuiz(id) {
      fetch(`/Admin_quizzes_active/${id}`,{method:"POST"})
  quizzes = quizzes.map(quiz => {
    if (quiz.id === id) {
      quiz.active = !quiz.active;
      output.innerHTML =
        `Quiz <strong>${quiz.title}</strong> is now
         <strong>${quiz.active ? "Active" : "Inactive"}</strong>.`;
    }
    return quiz;
  });
  renderQuizzes(quizzes);
}

/* ===== DELETE QUIZ ===== */
function deleteQuiz(id) {
        fetch(`/Admin_quizzes_delete/${id}`,{method:"POST"})
  const quiz = quizzes.find(q => q.id === id);
  if (confirm(`Delete quiz "${quiz.title}"?`)) {
    quizzes = quizzes.filter(q => q.id !== id);
    output.innerHTML =
      `Quiz <strong>${quiz.title}</strong> deleted.`;
    renderQuizzes(quizzes);
  }
}

/* ===== SEARCH ===== */
document.getElementById("searchQuiz").addEventListener("input", function () {
  const value = this.value.toLowerCase();
  const filtered = quizzes.filter(quizzes =>
    quizzes.title.toLowerCase().includes(value) ||
    quizzes.category.toLowerCase().includes(value)
  );
  renderQuizzes(filtered);
});
