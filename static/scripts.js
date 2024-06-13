// Get username from URL parameters or local storage (adjust as needed)
const urlParams = new URLSearchParams(window.location.search);
const username = urlParams.get('username') || localStorage.getItem('username');

// Display username or default message
const usernameSpan = document.getElementById("username");
usernameSpan.textContent = username || "there"; 
