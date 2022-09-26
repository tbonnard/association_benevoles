document.addEventListener("DOMContentLoaded", function () {

  let eventDetails = document.querySelector('#event_details');
  let attendance = document.querySelector('#attendance');

  attendance.style.display = 'none';

  let eventDetailsMenu = document.querySelector('#eventDetails_menu');
  let attendanceMenu = document.querySelector('#attendance_menu');

  eventDetailsMenu.addEventListener('click', () => {
    eventDetails.style.display = 'block';
    attendance.style.display = 'none';
  })

  attendanceMenu.addEventListener('click', () => {
    eventDetails.style.display = 'none';
    attendance.style.display = 'block';
  })


if (document.querySelector('#cancel_div') && document.querySelector('#cancel_button') && document.querySelector('#cancel_validation') && document.querySelector('#cancel_cancel')) {
  let cancelDiv = document.querySelector('#cancel_div');
  let cancelButton = document.querySelector('#cancel_button');
  let cancelValidation = document.querySelector('#cancel_validation');
  let cancelCancel = document.querySelector('#cancel_cancel');
  cancelValidation.style.display = 'none';

  cancelButton.addEventListener('click', () => {
    cancelValidation.style.display = 'block';
    cancelDiv.style.display = 'none';
    let cancelCancel = document.querySelector('#cancel_cancel');
    cancelCancel.addEventListener('click', () => {
      cancelValidation.style.display = 'none';
      cancelDiv.style.display = 'block';
    })
  })
}


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
