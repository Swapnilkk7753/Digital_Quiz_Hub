/* USER PROFILE DATA */
let userProfile = {
  name: "",
  email: "user@email.com"
};

/* OPEN PROFILE MODAL */
function openUserProfile() {
  document.getElementById("userNameInput").value = userProfile.name;
  new bootstrap.Modal(
    document.getElementById("userProfileModal")
  ).show();
}

/* SAVE PROFILE */
function saveUserProfile() {
  const newName = document.getElementById("userNameInput").value.trim();
  fetch(`/UpdateName/${newName}`,{method:"POST"})

  if (!newName) return;

  userProfile.name = newName;
  document.getElementById("userNameText").textContent = newName;

  bootstrap.Modal.getInstance(
    document.getElementById("userProfileModal")
  ).hide();
  
}
