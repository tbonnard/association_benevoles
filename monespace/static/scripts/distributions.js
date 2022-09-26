document.addEventListener("DOMContentLoaded", function () {

  let sendMessagesFormButton = document.querySelector('#send_messages_form_button');
  let sendMessagesGlobal = document.querySelector('#send_messages_global');
  let iconMessage = document.querySelectorAll('#message_icon_button');
  iconMessage.forEach(i => {
    i.addEventListener('click', () => {
      sendMessagesGlobal.style.display = 'block';
      sendMessagesFormButton.dataset.event = i.dataset.event;
    })
  })


});
