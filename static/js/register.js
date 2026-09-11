/* Show / Hide Password */
function togglePassword(id) {
  const input = document.getElementById(id);
  input.type = input.type === "password" ? "text" : "password";
}

/* Form Validation */
document.getElementById("registerForm").addEventListener("submit", function (e) {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirmPassword").value;

  let valid = true;

  // Email validation
  const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,}$/;
  if (!emailPattern.test(email)) {
    document.getElementById("emailError").textContent =
      "Enter a valid email address";
    valid = false;
  } else {
    document.getElementById("emailError").textContent = "";
  }

  // Confirm password validation
  if (password !== confirmPassword) {
    document.getElementById("passwordError").textContent =
      "Passwords do not match";
    valid = false;
  } else {
    document.getElementById("passwordError").textContent = "";
  }

  if (!valid) {
    e.preventDefault();
  }
});

function gett()
{
n=document.getElementById("name").value
e=document.getElementById("emai").value
p=document.getElementById("password").value
cp=document.getElementById("confirmPassword").value

fetch(`/Register_Status/${n}/${e}/${p}/${cp}`,{method:"POST"})
.then(res=>res.json())
.then(data=>{
   if (data.sta==0)
   {
    alert(data.mess)
  window.location.href=data.url
   }
});

}