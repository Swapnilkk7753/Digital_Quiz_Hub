/* ===== SAMPLE RESULT DATA ===== */
let results = [];
fetch("/Admin_results_d")
.then(res=>res.json())
.then(data=>{results=data.results;
  renderResults(results);
})
.catch(err=>console.error(err))

const resultTable = document.getElementById("resultTable");
const output = document.getElementById("resultOutput");

/* ===== RENDER RESULTS ===== */
function renderResults(data) {
  resultTable.innerHTML = "";
  data.forEach((res, index) => {
    const pass = (res.score*100)/res.total >= 40;

    resultTable.innerHTML += `
      <tr>
        <td>${index + 1}</td>
        <td>${res.user}</td>
        <td>${res.quiz}</td>
        <td>${(res.score*100)/res.total}%</td>
        <td>
          <span class="badge ${pass ? "badge-pass" : "badge-fail"}">
            ${pass ? "Pass" : "Fail"}
          </span>
        </td>
      </tr>
    `;
  });
}

renderResults(results);

/* ===== SEARCH RESULTS ===== */
document.getElementById("searchResult").addEventListener("input", function () {
  const value = this.value.toLowerCase();
  const filtered = results.filter(r =>
    r.user.toLowerCase().includes(value) ||
    r.quiz.toLowerCase().includes(value)
  );
  renderResults(filtered);
});
