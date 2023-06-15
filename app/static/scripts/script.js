const userInput = document.getElementById("textInput");
const submitBtn = document.getElementById("submitBtn");
const msgChat = document.querySelector(".msg-chat");

const USER = "You";
const BOT = "ChatBot";
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

  // get all the messages of the bot
  let bot_messages = document.querySelectorAll("body > div > main > div.msg.left-msg > div.msg-bubble > div.msg-text");

  // get the last message of the bot
  let last_bot_message = bot_messages[bot_messages.length - 1].textContent;

  // get all the messages of the user
  let user_messages = document.querySelectorAll("body > div > main > div.msg.right-msg > div.msg-bubble > div.msg-text");

  // get the last message of the user
  let last_user_message = user_messages[user_messages.length - 1];

  if (typeof last_user_message === 'object' && last_user_message !== null)
    last_user_message = last_user_message.textContent


  appendMessage(USER, msgText, "right", USER_IMG);
  userInput.value = "";



  botResponse(msgText, last_bot_message, last_user_message);
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

function botResponse(text, last_bot_message, last_user_message) {
  $.get("/get", { msg: text, botMsg: last_bot_message, userMsg: last_user_message }).done((data) => {
    appendMessage(BOT, data, "left", BOT_IMG);
  });
}
