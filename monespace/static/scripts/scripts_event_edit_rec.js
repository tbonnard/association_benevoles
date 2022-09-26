document.addEventListener("DOMContentLoaded", function () {


  let confirm_button = document.querySelector('#confirm');
  confirm_button.style.display = 'none';

  let url = new URL(window.location.href);
  let params = new URLSearchParams(url.search);
  let param_from_value = params.get('date');

  let form_event_rec = document.querySelector('#form_rec');
  let eventid = form_event_rec.dataset.eventid;
  let yes_all = document.querySelector('#yes');
  let no_only = document.querySelector('#no');
  let recurringDiv = document.querySelector('#recurring');
  let recurringDivMaster = document.querySelector('#recurringMaster');

  let div_event_original_start_date = document.querySelector('#dates_event')
  let event_original_start_date = div_event_original_start_date.dataset.original_start_date;
  let startDateInput = document.querySelector('#id_start_date');
  let endDateInput = document.querySelector('#id_end_date');

  form_event_rec.style.display = 'none';

  yes_all.addEventListener('click', () => {
    form_event_rec.action = `${window.location.origin}/event/modifier/${eventid}/`;
    confirm_button.style.display = 'block';
    recurringDivMaster.style.display = 'block';
    form_event_rec.style.display = 'block';
    div_event_original_start_date.style.display = 'none';
    startDateInput.value = event_original_start_date;
    endDateInput.value = event_original_start_date;
  });

  no_only.addEventListener('click', () => {
    form_event_rec.action = `${window.location.origin}/event/modifier/simple/${eventid}/?date=${param_from_value}`;
    confirm_button.style.display = 'block';
    recurringDivMaster.style.display = 'none';
    form_event_rec.style.display = 'block';
    div_event_original_start_date.style.display = 'block';
    startDateInput.value = param_from_value;
    endDateInput.value = param_from_value;
  });




});
