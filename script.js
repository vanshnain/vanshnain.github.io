const correctUsername = "admin";
const correctPassword = "admin@vntech";
const correctUsername = "vanshnain";
const correctPassword = "vansh@76";
const correctUsername = "web.view";
const correctPassword = "web@view";
const correctUsername = "or.vntech";
const correctPassword = "or@vntech";

function login() {
  const user = document.getElementById("username").value;
  const pass = document.getElementById("password").value;

  if (user === correctUsername && pass === correctPassword) {
    localStorage.setItem("loggedIn", "true");
    window.location.href = "dashboard.html";
  } else {
    document.getElementById("error").innerText = "Invalid ID or Password";
  }
}

function logout() {
  localStorage.removeItem("loggedIn");
  window.location.href = "index.html";
}

if (window.location.pathname.includes("dashboard.html")) {
  if (localStorage.getItem("loggedIn") !== "true") {
    window.location.href = "index.html";
  }
}
