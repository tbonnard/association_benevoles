

document.addEventListener("DOMContentLoaded", function () {



function api_call_attend_decline(eventid, date, type) {
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
            type: type
        }),
  })
  .then(response => response.json())
  .then(data => {
    document.querySelectorAll(`#div_${eventid}${date}`).forEach(e => e.parentNode.removeChild(e));
    document.querySelectorAll(`#span_${eventid}${date}`).forEach(e => e.parentNode.removeChild(e));
    get_specific_attendees(eventid, date);
  })

  }


  function create_elements_attendees(parentDiv, eventid, date, pInner, buttonText, type) {
    let div = document.createElement('div');
    div.className = 'attendees_declines';
    div.id = `div_${eventid}${date}`
    parentDiv.append(div);
    let p = document.createElement('p');
    div.append(p);
    let button = document.createElement('button');
    div.append(button);
    p.innerHTML = pInner;
    button.innerHTML = buttonText;
    button.id = `${eventid}_${date}`;
    if (type == "decline") {
      button.className="button_attendee_decline button_inversed button_attendance";
    } else {
      button.className="button_attendee_decline button_attendance";
    }
    button.addEventListener('click', (e) => {
      e.preventDefault();
      api_call_attend_decline(eventid, date, type);
      if (window.location.href.slice(0, -1) == window.location.origin ) {
        window.location.reload();
      }
    })

  }


  function get_number_attendees(eventid, date) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
                      `${window.location.origin}/api_get_count_specific_attendees/`,
                      {headers: {'X-CSRFToken': csrftoken}}
                  );
    const response = fetch(request, {
      method:'POST',
      mode: 'same-origin',
      body: JSON.stringify({
              parent_event: eventid,
              event_date: date,
          }),
    })
    .then(response => response.json())
    .then(data => {
      // console.log(data[0])
      update_benev_number_box(eventid, date, data);
      if (document.querySelector('#box_to_items')) {
        update_benev_number_list(eventid, date, data);
      }
    })

  }

  function update_benev_number_box(eventid, date, data) {
    let span_number_attendees = document.querySelector(`#attend_event_number_${eventid}${date}`);
    if (data[0] > 1 ) {
      text_attendees_number = `${data} personnes confirmées`
    } else if (data[0] > 0 ) {
      text_attendees_number = `${data} personne confirmée`
    } else {
      text_attendees_number = "0 personne confirmée"
    }
    span_number_attendees.innerHTML = text_attendees_number;
  }



  let attendees_number_event = document.querySelectorAll(`.attend_event_number`);
  attendees_number_event.forEach( i => {
    get_number_attendees(i.dataset.eventid, i.dataset.date);
  })



  function get_specific_attendees (eventid, date) {
    fetch(`${window.location.origin}/api_get_specific_attendees/?parent_event=${eventid}&event_date=${date}`)
    .then(response => response.json())
    .then(data => {

      let div_attendees = document.querySelector(`#parent_${eventid}${date}`);
      let div_attendees_list = document.querySelector(`#parent_list_${eventid}${date}`);


      for (const j in data) {
        if (data[j].parent_event == eventid && data[j].event_date == date) {
          create_elements_attendees(div_attendees, eventid, date, '', '<i class="fas fa-check-square icon_attend"></i>Je serai là', 'decline');
          createElementsList(div_attendees_list, eventid, date, '<i class="fas fa-check-square icon_attend"></i>Je serai là', 'decline');
          get_number_attendees(eventid, date);
        }
      }

      if (div_attendees.children.length == 0 ) {
        create_elements_attendees(div_attendees, eventid, date, '', '<i class="far fa-square icon_attend"></i>Confirmer ma présence', 'attend');
        createElementsList(div_attendees_list, eventid, date, '<i class="far fa-square icon_attend"></i>Confirmer ma présence', 'attend');
        get_number_attendees(eventid, date);
      }

    })

}


  function all_attendees_user() {
    fetch(`${window.location.origin}/api_get_all_attendees_user/`)
    .then(response => response.json())
    .then(data => {

      let attendees = document.querySelectorAll('.attendees');
      attendees.forEach(i => {

        let eventid = i.dataset.eventid;
        let date = i.dataset.date;
        for (const j in data) {

          if (data[j].parent_event == eventid && data[j].event_date == date) {
            create_elements_attendees(i, eventid, date, '', '<i class="fas fa-check-square icon_attend"></i>Je serai là', 'decline');
          }
        }
      })

      attendees.forEach(i => {
        let eventid = i.dataset.eventid;
        let date = i.dataset.date;
        if (i.children.length == 0 ) {
          create_elements_attendees(i, eventid, date, '', '<i class="far fa-square icon_attend"></i>Confirmer ma présence', 'attend');
        }
      })


      let attendees_list = document.querySelectorAll('.attendees_list');
      attendees_list.forEach(i => {

        let eventid = i.dataset.eventid;
        let date = i.dataset.date;
        for (const j in data) {

          if (data[j].parent_event == eventid && data[j].event_date == date) {
            createElementsList(i, eventid, date, '<i class="fas fa-check-square icon_attend"></i>Je serai là', 'decline');
          }
        }
      })

      attendees_list.forEach(i => {
        let eventid = i.dataset.eventid;
        let date = i.dataset.date;
        if (i.children.length == 0 ) {
          createElementsList(i, eventid, date, '<i class="far fa-square icon_attend"></i>Confirmer ma présence', 'attend');
        }
      })


    })

  };

all_attendees_user();



  function get_user_distrib() {
    const request = new Request(`${window.location.origin}/get_user_distrib/`);
    const response = fetch(request, {
      method:'GET',
      mode: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
      let attendeesForm = document.querySelectorAll('.attendees');
      let attendeesList= document.querySelectorAll('.attendees_list');
      attendeesForm.forEach(i => {
        data.forEach(y => {
          if (y.id_distrib == i.dataset.eventid && y.user_status == 1) {
            i.innerHTML = "<p class='info_text'>en attente de confirmation par le responsable afin de pouvoir rejoindre cette distribution</p>"
          }
        })
      })

      attendeesList.forEach(i => {
        data.forEach(y => {
          if (y.id_distrib == i.dataset.eventid && y.user_status == 1) {
            i.innerHTML = "<p class='info_text'>en attente du responsable</p>"
          }
        })
      })


    })
  }


get_user_distrib();


// BOX TO ITEMS ELEMENTS


if (document.querySelector('#box_to_items')) {
  let box_to_items = document.querySelector('#box_to_items');
  let items_to_box = document.querySelector('#items_to_box');

  let box_items_distrib = document.querySelector('#box_items_distrib');
  let list_items_distrib = document.querySelector('#list_items_distrib');


  items_to_box.style.display = 'none';
  list_items_distrib.style.display = 'none';

  box_to_items.addEventListener('click', () => {
    window.scrollTo({top:0,left:0,behavior:'smooth'});
    items_to_box.style.display = 'block';
    list_items_distrib.style.display = 'block';
    box_to_items.style.display = 'none';
    box_items_distrib.style.display = 'none';
  })

  items_to_box.addEventListener('click', () => {
    window.scrollTo({top:0,left:0,behavior:'smooth'});
    items_to_box.style.display = 'none';
    list_items_distrib.style.display = 'none';
    box_to_items.style.display = 'block';
    box_items_distrib.style.display = 'block';
  })


  let attendanceBenev = document.querySelectorAll('.attendance_benev');
  attendanceBenev.forEach( i => {
    get_number_attendees(i.dataset.event, i.dataset.date);
  })

  }

  function update_benev_number_list(eventid, date, data) {
    let tdBenevoleText = document.querySelector(`#attend_event_number_manager_${eventid}${date}`);
    tdBenevoleText.textContent = data[0];
  }


  // let benevListAttendance = document.querySelectorAll('.attendees_list');
  // benevListAttendance.forEach( i => {
  //   createElementsList(i, i.dataset.event, i.dataset.date);
  // })


  function createElementsList (parentDivList, eventid, date, aText, type) {
    let span = document.createElement('span');
    span.id = `span_${eventid}${date}`
    parentDivList.append(span);
    let a = document.createElement('a');
    a.innerHTML = aText;
    a.id = `${eventid}__${date}`;
    span.append(a);
    if (type == "decline") {
      a.className = "a_reverse";
    } else {
    }
      a.addEventListener('click', (e) => {
      e.preventDefault();
      api_call_attend_decline(eventid, date, type);
      if (window.location.href.slice(0, -1) == window.location.origin ) {
        window.location.reload();
      }
    })

  }


});
