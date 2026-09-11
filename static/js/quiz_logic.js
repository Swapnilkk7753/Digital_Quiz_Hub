/* ================= TIMER ================= */
//let totalTime = 0.1 * 60; // 15 minutes
const timeDisplay = document.getElementById("time");
//let totalTime = timeDisplay * 60;
//timeDisplay=timeDisplay*60;
var times=document.getElementById("time");
var ti=times.getAttribute("data-ti");
ti=parseFloat(ti);
let totalTime = ti * 60;

const timer = setInterval(() => {
  let minutes = Math.floor(totalTime/ 60);
  let seconds = totalTime % 60;

  timeDisplay.textContent =
    `${minutes}:${seconds < 10 ? "0" + seconds : seconds}`;

  totalTime--;

  if (totalTime < 0) {
    clearInterval(timer);
    alert("Question Submitted! Move for next question ");
    window.location.href = "/Next_available_question";
  }
}, 1000);

/* ================= QUESTIONS ================= */
let currentQuestion = 0;
const totalQuestions = document.querySelectorAll(".q-btn").length;
const qButtons = document.querySelectorAll(".q-btn");

function showQuestion(index) {
  qButtons.forEach(btn => btn.classList.remove("active"));
  qButtons[index].classList.add("active");
  currentQuestion = index;
}

/* Question click */
qButtons.forEach((btn, index) => {
  btn.addEventListener("click", () => {
    showQuestion(index);
  });
});

/* ================= NAVIGATION ================= */
document.getElementById("nextBtn").addEventListener("click", () => {
  if (currentQuestion < totalQuestions - 1) {
    showQuestion(currentQuestion + 1);
  }
});

document.getElementById("prevBtn").addEventListener("click", () => {
  if (currentQuestion > 0) {
    showQuestion(currentQuestion - 1);
  }
});

/* ================= ANSWER TRACK ================= */
const options = document.querySelectorAll(".form-check-input");

options.forEach(opt => {
  opt.addEventListener("change", () => {
    qButtons[currentQuestion].classList.add("answered");
  });
});

function submitq()
{
  let res=confirm("Are you sure to submit quiz ?");
  let stt=res ? 1 : 0;
  document.getElementById("sbut").value=stt
}