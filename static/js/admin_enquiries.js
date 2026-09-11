/* ===== SAMPLE ENQUIRY DATA ===== */
let enquiries = [];
fetch("/Admin_enquiry_d")
.then(res=>res.json())
.then(data=>{enquiries=data.users;
  renderEnquiries(enquiries);
})
.catch(err=>console.error(err))

const enquiryTable = document.getElementById("enquiryTable");
const output = document.getElementById("enquiryOutput");

/* ===== RENDER ENQUIRIES ===== */
function renderEnquiries(data) {
  enquiryTable.innerHTML = "";
  data.forEach((enq, index) => {
    enquiryTable.innerHTML += `
      <tr>
        <td>${index + 1}</td>
        <td>${enq.name}</td>
        <td>${enq.email}</td>
        <td>${enq.message}</td>
        <td>
          <span class="badge ${!enq.read ? "badge-read" : "badge-new"}">
            ${!enq.read ? "Read" : "New"}
          </span>
        </td>
        <td>
          <button class="btn btn-outline-primary btn-sm"
            onclick="markRead(${enq.id})">
            Mark Read
          </button>

          <button class="btn btn-outline-danger btn-sm"
            onclick="deleteEnquiry(${enq.id})">
            Delete
          </button>
        </td>
      </tr>
    `;
  });
}

//renderEnquiries(enquiries);

/* ===== MARK AS READ ===== */
function markRead(id) {
  fetch(`/Admin_enquiry_active/${id}`,{method:"POST"})
  enquiries = enquiries.map(e => {
    if (e.id === id) {
      e.read = !e.read ;
      output.innerHTML =
        `Enquiry from <strong>${e.name}</strong> marked as read.`;
    }
    return e;
  });
  renderEnquiries(enquiries);
}

/* ===== DELETE ENQUIRY ===== */
function deleteEnquiry(id) {
    fetch(`/Admin_enquiry_delete/${id}`,{method:"POST"})
  const enq = enquiries.find(e => e.id === id);
  if (confirm("Delete this enquiry?")) {
    enquiries = enquiries.filter(e => e.id !== id);
    output.innerHTML =
      `Enquiry from <strong>${enq.name}</strong> deleted.`;
    renderEnquiries(enquiries);
  }
}

/* ===== SEARCH ===== */
document.getElementById("searchEnquiry").addEventListener("input", function () {
  const value = this.value.toLowerCase();
  const filtered = enquiries.filter(e =>
    e.name.toLowerCase().includes(value) ||
    e.email.toLowerCase().includes(value)
  );
  renderEnquiries(filtered);
});
