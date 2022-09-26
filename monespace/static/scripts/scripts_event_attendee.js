document.addEventListener("DOMContentLoaded", function () {


function api_call(eventid, date, type, plus_other=null) {
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const request = new Request(
                    `${window.location.origin}/api_attend_decline_event/`,
                    {headers: {'X-CSRFToken': csrftoken}}
                );
  const response = fetch(request, {
    method:'POST',
    mode: 'same-origin',
    body: JSON.stringify({
            parent_event: eventid,
            event_date: date,
            type: type,
            plus_other: plus_other
        }),
  })
  .then(response => response.json())
  .then(data => {window.location.reload(true);})
  }

  let buttons_attend = document.querySelectorAll('.button_attendees');
  buttons_attend.forEach(i => {
    let eventid = i.dataset.eventid;
    let date = i.dataset.date;
    let attendee_type = i.dataset.type;
    i.addEventListener('click', (e) => {
      e.preventDefault();
      api_call(eventid, date, attendee_type);
    })
  })


  if (document.querySelector('#plus_other')) {
    let plus_other = document.querySelector('#plus_other');
    let eventid = plus_other.dataset.eventid;
    let date = plus_other.dataset.date;
    plus_other.addEventListener('change', () => {
      api_call(eventid, date, 'plus_other', plus_other.value);
    })
    plus_other.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      api_call(eventid, date, 'plus_other', plus_other.value);
      }
    });
  }



});
