/* ===== SAMPLE CATEGORY DATA ===== */
let categories = [];
fetch("/Admin_category_d")
.then(res=>res.json())
.then(data=>{categories=data.users;
  renderCategories(categories);
})
.catch(err=>console.error(err))

const categoryTable = document.getElementById("categoryTable");
const output = document.getElementById("categoryOutput");

/* ===== RENDER CATEGORIES ===== */
function renderCategories(data) {
  categoryTable.innerHTML = "";
  data.forEach((cat, index) => {
    categoryTable.innerHTML += `
      <tr>
        <td>${index + 1}</td>
        <td>${cat.Name}</td>
        <td>
          <span class="badge ${cat.active ? "badge-active" : "badge-inactive"}">
            ${cat.active ? "Active" : "Inactive"}
          </span>
        </td>
        <td>
          <button class="btn btn-outline-primary btn-sm"
            onclick="toggleCategory(${cat.id})">
            ${cat.active ? "Disable" : "Enable"}
          </button>

          <button class="btn btn-outline-danger btn-sm"
            onclick="deleteCategory(${cat.id})">
            Delete
          </button>
        </td>
      </tr>
    `;
  });
}

//renderCategories(categories);

/* ===== ADD CATEGORY ===== */
/*function addCategory() {
  const input = document.getElementById("categoryName");
  const name = input.value.trim();

  if (name === "") return;

  categories.push({
    id: Date.now(),
    name: name,
    active: true
  });

  output.innerHTML =
    `Category <strong>${name}</strong> added successfully.`;

  input.value = "";
  renderCategories(categories);
}*/

/* ===== TOGGLE CATEGORY ===== */
function toggleCategory(id) {
    fetch(`/Admin_categories_active/${id}`,{method:"POST"})
  categories = categories.map(cat => {
    if (cat.id === id) {
      cat.active = !cat.active;
      output.innerHTML =
        `Category <strong>${cat.Name}</strong> is now
         <strong>${cat.active ? "Active" : "Inactive"}</strong>.`;
    }
    return cat;
  });
  renderCategories(categories);
}

/* ===== DELETE CATEGORY ===== */
function deleteCategory(id) {
    fetch(`/Admin_categories_delete/${id}`,{method:"POST"})
  const cat = categories.find(c => c.id === id);
  if (confirm(`Delete category ${cat.Name}?`)) {
    categories = categories.filter(c => c.id !== id);
    output.innerHTML =
      `Category <strong>${cat.Name}</strong> deleted.`;
    renderCategories(categories);
  }
}

/* ===== SEARCH ===== */
document.getElementById("searchCategory").addEventListener("input", function () {
  const value = this.value.toLowerCase();
  const filtered = categories.filter(cat =>
    cat.Name.toLowerCase().includes(value)
  );
  renderCategories(filtered);
});
