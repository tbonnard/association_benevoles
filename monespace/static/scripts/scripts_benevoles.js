document.addEventListener("DOMContentLoaded", function () {


  let active_button= document.querySelectorAll('.button_active_status');

  let user_status = document.querySelectorAll('.user_status')
  let form_status_button= document.querySelectorAll('.button_form_status');
  let form_status= document.querySelectorAll('.form_status');
  let validatePendingUserStatus = document.querySelector('#validate_pending_user_status');

  form_status.forEach(i => {
    i.style.display = 'none';
  })

  user_status.forEach(i => {
    i.style.display = 'block';
  })


  form_status_button.forEach(i => {
    i.addEventListener('click', () => {
      form_status.forEach(j => {
        if (i.dataset.user==j.dataset.user && j.style.display == 'block') {
          j.style.display = 'none';
        } else  if (i.dataset.user==j.dataset.user && j.style.display == 'none') {
          j.style.display = 'block';
        }
        if (i.dataset.type == 'edit' && i.dataset.user==j.dataset.user) {
          i.innerHTML = "<i class='far fa-window-close'></i>";
          i.dataset.type = 'cancel';
        } else if (i.dataset.type == 'cancel' && i.dataset.user==j.dataset.user)  {
          i.innerHTML = "<i class='far fa-edit'></i>";
          i.dataset.type = 'edit';
        }
      })
      user_status.forEach(k => {
        if (i.dataset.user==k.dataset.user && k.style.display == 'block') {
          k.style.display = 'none';
        } else  if (i.dataset.user==k.dataset.user && k.style.display == 'none') {
          k.style.display = 'block';
        }
      })
    })
  })

});
