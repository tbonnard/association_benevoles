document.addEventListener("DOMContentLoaded", function () {

  let profile = document.querySelector('#profile');
  let locations = document.querySelector('#locations');

  locations.style.display = 'none';

  let profileMenu = document.querySelector('#profile_menu');
  let locationsMenu = document.querySelector('#locations_menu');

  profileMenu.addEventListener('click', () => {
    profile.style.display = 'block';
    locations.style.display = 'none';
  })

  locationsMenu.addEventListener('click', () => {
    profile.style.display = 'none';
    locations.style.display = 'block';
  })


  let sendMessagesFormButton = document.querySelector('#send_messages_form_button');
  let sendMessagesGlobal = document.querySelector('#send_messages_global');
  let iconMessage = document.querySelectorAll('#message_icon_button');
  iconMessage.forEach(i => {
    i.addEventListener('click', () => {
      sendMessagesGlobal.style.display = 'block';
      sendMessagesFormButton.dataset.user = i.dataset.user;
    })
  })


});
