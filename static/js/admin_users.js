/* ===== SAMPLE USER DATA ===== */
let users = [];
fetch("/Admin_users_d")
.then(res=>res.json())
.then(data=>{users=data.users;
  renderUsers(users);
})
.catch(err=>console.error(err))
const userTable = document.getElementById("userTable");
const output = document.getElementById("userActionOutput");

/* ===== RENDER USERS ===== */
function renderUsers(data) {
  userTable.innerHTML = "";
  data.forEach((user, index) => {
    userTable.innerHTML += `
      <tr>
        <td>${index+1}</td>
        <td>${user.Name}</td>
        <td>${user.Email}</td>
        <td>
          <span class="badge ${user.active ? "badge-active" : "badge-inactive"}">
            ${user.active ? "Active" : "Inactive"}
          </span>
        </td>
        <td>
          <button class="btn btn-outline-primary btn-sm"
            onclick="toggleStatus(${user.id})">
            ${user.active ? "Deactivate" : "Activate"}
          </button>

          <button class="btn btn-outline-danger btn-sm"
            onclick="deleteUser(${user.id})">
            Delete
          </button>
        </td>
      </tr>
    `;
  });
}

//renderUsers(users);

/* ===== TOGGLE STATUS ===== */
function toggleStatus(id) {
  fetch(`/Admin_users_active/${id}`,{method:"POST"})
  users = users.map(user => {
    if (user.id === id) {
      user.active = !user.active;
      output.innerHTML =
        `User <strong>${user.Name}</strong> is now
         <strong>${user.active ? "Active" : "Inactive"}</strong>.`;
    }
    return user;
  });
  renderUsers(users);
}

/* ===== DELETE USER ===== */
function deleteUser(id) {
  fetch(`/Admin_users_delete/${id}`,{method:"POST"})
  const user = users.find(u => u.id === id);
  if (confirm(`Delete user ${user.Name}?`)) {
    users = users.filter(u => u.id !== id);
    output.innerHTML =
      `User <strong>${user.Name}</strong> has been deleted.`;
    renderUsers(users);
  }
}

/* ===== SEARCH ===== */
document.getElementById("searchUser").addEventListener("input", function () {
  const value = this.value.toLowerCase();
  const filtered = users.filter(user =>
    user.Name.toLowerCase().includes(value) ||
    user.Email.toLowerCase().includes(value)
  );
  renderUsers(filtered);
});
