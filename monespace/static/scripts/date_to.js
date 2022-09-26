document.addEventListener("DOMContentLoaded", function () {

  if (document.querySelector('#event_link_date_distrib_loc')) {
    let numWeeks = 8;
    let now = new Date();
    now.setDate(now.getDate() + numWeeks * 7);
    event_link = document.querySelector('#event_link_date_distrib_loc');
    event_link_original = event_link.href
    date_to = now.toISOString().split('T')[0];
    event_link.href = event_link_original+date_to;
  }


});
