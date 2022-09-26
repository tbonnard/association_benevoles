document.addEventListener("DOMContentLoaded", function () {


  let date_from_select= document.querySelector('#date_from');
  let date_to_select = document.querySelector('#date_to');
  let form_action = document.querySelector('#form_search_dates');

  let url = new URL(window.location.href);
  let params = new URLSearchParams(url.search);
  let param_from_value = params.get('from');
  let param_to_value = params.get('to');
  let param_loc_value = params.get('location');

  date_from_select.value = param_from_value ;
  date_to_select.value = param_to_value ;


  function diff_dates () {
    let date_from = document.querySelector('#date_from').value;
    let date_to = document.querySelector('#date_to').value;
    let param_loc_value_update = params.get('location');
    let param_all_value_update = params.get('all');
    let param_distrib_value_update = params.get('distrib');
    if (param_loc_value_update || param_all_value_update ||  param_distrib_value_update) {
      form_action.href = `${window.location.origin}/event/liste/?from=${date_from}&to=${date_to}&location=${param_loc_value}&all=${param_all_value_update}&distrib=${param_distrib_value_update}`
    } else {
      form_action.href = `${window.location.origin}/event/liste/?from=${date_from}&to=${date_to}`
    }
    }

  date_from_select.addEventListener('change', () => {
    console.log('bonjour');
    diff_dates();
  })

  date_to_select.addEventListener('change', () => {
    console.log('bonjaaour');
    diff_dates();
  })

});
