const userInput = document.getElementById("textInput");
const submitBtn = document.getElementById("submitBtn");
const msgChat = document.querySelector(".msg-chat");

const USER = "You";
const BOT = "Nerdbot";
const USER_IMG = "https://cdn-icons-png.flaticon.com/512/2922/2922510.png";
const BOT_IMG = "https://cdn-icons-png.flaticon.com/512/4712/4712106.png";

// if user press Enter instead of the button
userInput.addEventListener("keypress", (ev) => {
  if (ev.key === "Enter") {
    ev.preventDefault();
    submitBtn.click();
  }
});

submitBtn.addEventListener("click", (ev) => {
  ev.preventDefault();

  const msgText = userInput.value;
  if (!msgText) return;

  appendMessage(USER, msgText, "right", USER_IMG);
  userInput.value = "";

  botResponse(msgText);
});

function appendMessage(name, data, side, img) {
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>
      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
        </div>
        <div class="msg-text">${data}</div>
      </div>
    </div>
      `;


  msgChat.insertAdjacentHTML("beforeend", msgHTML);
  msgChat.scrollTop += 500;
}

function botResponse(text) {
  $.get("/get", { msg: text }).done((data) => {
    appendMessage(BOT, data, "left", BOT_IMG);
  });
}
