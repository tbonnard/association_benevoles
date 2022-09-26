document.addEventListener("DOMContentLoaded", function () {


//DATES TIME MANAGEMENT
  let startDateInput = document.querySelector('#id_start_date');
  let endDateInput = document.querySelector('#id_end_date');
  let timesDiv = document.querySelector('#times_div');
  let timesSubDiv = document.querySelectorAll('.times_subdiv');
  let timeFromInput = document.querySelector('#id_time_from');
  let timeToInput = document.querySelector('#id_time_to');
  let fullDay = document.querySelector('#id_is_full_day');
  let timeFromInputInitial = timeFromInput.value;
  let timeToInputInitial = timeToInput.value;


  function updateEndDate() {
    endDateInput.value = startDateInput.value;
  }

  function updateToTime() {
    timeToInput.value = timeFromInput.value;
  }

  startDateInput.addEventListener('change', () => {
    updateEndDate();
  })

  endDateInput.addEventListener('change', () => {
    if (endDateInput.value == '') { updateEndDate(); }
  })

  timeFromInput.addEventListener('change', () => {
    updateToTime();
  })


  function hide_display_timesDiv () {
    if (fullDay.checked) {
      timesSubDiv.forEach(i => i.style.display='none')
    } else {
      timesSubDiv.forEach(i => i.style.display='block')
    }
  }

  fullDay.addEventListener('click', () => {
    if (fullDay.checked) {
      timeFromInput.value = "00:00:00";
      timeToInput.value = "23:59:00";
    } else {
      timeFromInput.value = timeFromInputInitial;
      timeToInput.value = timeToInputInitial;
    }
    hide_display_timesDiv();
  })


  hide_display_timesDiv();


// RECURRING MANAGEMENT
  function toggle_rec_form (is_rec, is_rec_form) {
    if (is_rec.checked) {
      is_rec_form.style.display = 'block';
      }
    else {
          is_rec_form.style.display = 'none';
        }
      }

    function manageEndDateRecurring (is_rec, endDateInput) {
      if (is_rec.checked) {endDateInput.disabled = true;}
      else {endDateInput.disabled = false;}
    }


    function validateRecFields (field) {
      if (field.value == "" || isNaN(field.value) || parseInt(field.value) < 0 || parseInt(field.value) == 0 ) {
        field.value =1;
      }
    }



  if ( document.querySelector('#id_is_recurring') && document.querySelector('#recurring') ) {
    let is_rec = document.querySelector('#id_is_recurring');
    let is_rec_form = document.querySelector('#recurring');
    let id_separation_count = document.querySelector('#id_separation_count');
    let id_max_num_occurrences = document.querySelector('#id_max_num_occurrences');

    is_rec.addEventListener('click', () => {
        toggle_rec_form(is_rec, is_rec_form);
        manageEndDateRecurring(is_rec, endDateInput);
        validateRecFields(id_separation_count);
        validateRecFields(id_max_num_occurrences);
    });

    id_separation_count.addEventListener('change', () => {
      validateRecFields(id_separation_count);
    })

    id_max_num_occurrences.addEventListener('change', () => {
      validateRecFields(id_max_num_occurrences);
    })

    toggle_rec_form(is_rec, is_rec_form);
    manageEndDateRecurring(is_rec, endDateInput);
  }



});
