/* ===== ADMIN DATA ===== */
let adminProfile = {
  name: "",
  email: "admin@quizhub.com"
};

/* ===== REDIRECT MODULE ===== */
function openModule(page) {
  window.location.href = page;
}

/* ===== EDIT PROFILE ===== */
function openEditProfile() {
  document.getElementById("adminNameInput").value = adminProfile.name;
  new bootstrap.Modal(document.getElementById("editProfileModal")).show();
}

function saveAdminProfile() {
  const newName = document.getElementById("adminNameInput").value.trim();
  fetch(`/UpdateName/${newName}`,{method:"POST"})

  if (!newName) return;

  adminProfile.name = newName;
  document.getElementById("adminNameText").textContent = newName;

  bootstrap.Modal.getInstance(
    document.getElementById("editProfileModal")
  ).hide();
}

/* ===== COUNT ANIMATION ===== */
document.querySelectorAll(".stat-card").forEach(card => {
  const target = +card.dataset.count;
  const counter = card.querySelector(".count");
  let count = 0;

  function update() {
    if (count < target) {
      count += Math.ceil(target / 50);
      counter.textContent = count;
      setTimeout(update, 30);
    } else {
      counter.textContent = target;
    }
  }
  update();
});
