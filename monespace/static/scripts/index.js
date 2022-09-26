
document.addEventListener("DOMContentLoaded", function () {


  let events14Days = document.querySelector('#events_14_days');
  let messages = document.querySelector('#messages');

  let events14DaysMenu = document.querySelector('#events_14_days_menu');
  let messagesMenu = document.querySelector('#messages_menu');


if (document.querySelector('#events_manager_menu')) {
  let eventsManager = document.querySelector('#events_manager');
  let eventsManagerMenu = document.querySelector('#events_manager_menu');

  eventsManager.style.display = 'block';
  events14Days.style.display = 'none';
  messages.style.display = 'none';
  eventsManagerMenu.className = "sub_nav_hor active";
  events14DaysMenu.className = "sub_nav_hor";

  eventsManagerMenu.addEventListener('click', () => {
    events14Days.style.display = 'none';
    messages.style.display = 'none';
    eventsManager.style.display = 'block';
  })

  events14DaysMenu.addEventListener('click', () => {
    events14Days.style.display = 'block';
    messages.style.display = 'none';
    eventsManager.style.display = 'none';
  })

  messagesMenu.addEventListener('click', () => {
    events14Days.style.display = 'none';
    messages.style.display = 'block';
    eventsManager.style.display = 'none';
  })

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
      // console.log(data[0]);
      let tdBenevoleText = document.querySelector(`#attend_event_number_manager_${eventid}${date}`);
      tdBenevoleText.textContent = data[0];
    })

  }

  let buttonEvenManagerLoad = document.querySelector('#button_event_manager_load');
  let info_text = document.querySelector('#no_distrib');
  info_text.style.display = 'none';
  let tableEvent = document.querySelector('.table1');
  tableEvent.style.display = 'none';
  const user_id = buttonEvenManagerLoad.dataset.ideventsearch;



  function createDistrib(fromDateFinal, toDateFinal) {

  let url = `${window.location.origin}/events_list_json/${user_id}/?from=${fromDateFinal}&to=${toDateFinal}`;
  fetch(url)
    .then(response => response.json())
    .then(data => {
      // console.log(data);
      let options = {day: 'numeric', month: 'long', year: 'numeric'};
      if (data.length > 0) {
        tableEvent.style.display = 'block';
        info_text.style.display = 'none';
      data.forEach(i => {

        for (const [key, value] of Object.entries(i[1])) {
          // console.log(value['details']);
          // console.log(value['details']['uuid'])

          let tbody = document.querySelector('#tbody_event_manager');
          let tr = document.createElement('tr');
          let tdDate = document.createElement('td');
          tdDate.className='table_cell';
          let aUrlEvent = document.createElement('a');
          aUrlEvent.className = "event_manager_date";
          aUrlEvent.dataset.event_manager_date = new Date(i[0]+"T00:00:00.000").toISOString().split('T')[0];
          aUrlEvent.textContent = new Date(i[0]+"T00:00:00.000").toLocaleDateString('fr-FR', options);
          aUrlEvent.href = `${window.location.origin}/event/details/${value['details']['uuid']}/?date=${i[0]}`;
          let tdName = document.createElement('td');
          tdName.className='table_cell';
          tdName.textContent = value['details']['name'];
          let atdName = document.createElement('a');
          atdName.href = `${window.location.origin}/distribution/details/${value['details']['uuid']}/`;
          atdName.innerHTML=`<i class='fas fa-angle-right'></i>`;
          atdName.title = 'Détails globaux sur la distribution, et non pas juste cette date';
          let tdLocation = document.createElement('td');
          tdLocation.className='table_cell';
          tdLocation.textContent = value['details']['location']['name'];
          let atdLocation = document.createElement('a');
          atdLocation.href = `${window.location.origin}/site/${value['details']['location']['uuid']}/`;
          atdLocation.innerHTML=`<i class='fas fa-angle-right'></i>`;
          atdLocation.title = 'Détails du site';
          let tdTime = document.createElement('td');
          tdTime.className='table_cell';
          tdTime.textContent = `${value['details']['time_from'].slice(0, -3)} - ${value['details']['time_to'].slice(0, -3)}`;
          let tdBenevoles = document.createElement('td');
          tdBenevoles.className='table_cell button_attendance_manager';
          tdBenevoles.id = `attend_event_number_manager_${value['details']['uuid']}${i[0]}`;
          tdBenevoles.dataset.event_date = `${value['details']['uuid']}_${i[0]}`;
          get_number_attendees(value['details']['uuid'], i[0]);
          let tdMessage = document.createElement('td');
          tdMessage.className='table_cell';
          let aTdMessage = document.createElement('a');
          aTdMessage.title = 'Envoyer un message aux bénévoles';
          aTdMessage.id = `message_icon_button`;
          aTdMessage.dataset.details = `${value['details']['uuid']}${i[0]}`
          aTdMessage.dataset.event = `${value['details']['uuid']}`
          aTdMessage.dataset.date = `${i[0]}`
          if (value['details']['event_date_cancelled'] == 0) {
            aTdMessage.innerHTML=`<i class='fas fa-envelope'></i>`;
          } else {
            aTdMessage.innerHTML=``;
          }
          let tdCancelDate = document.createElement('td');
          tdCancelDate.className='table_cell';
          tbody.append(tr);
          tr.append(tdDate);
          tdDate.append(aUrlEvent);
          tr.append(tdName);
          tdName.append(atdName);
          tr.append(tdLocation);
          tdLocation.append(atdLocation);
          tr.append(tdTime);
          tr.append(tdBenevoles);
          tr.append(tdMessage);
          tdMessage.append(aTdMessage);
          tr.append(tdCancelDate);
          if (value['details']['event_date_cancelled'] == 0) {
            let aURLCancelDate = document.createElement('a');
            aURLCancelDate.title = `Annuler la distribution du ${i[0]}`;
            let iCancelDate = document.createElement('i');
            iCancelDate.className = "far fa-trash-alt";
            tdCancelDate.append(aURLCancelDate);
            aURLCancelDate.append(iCancelDate);
            aURLCancelDate.addEventListener('click', () => {
              tdCancelDate.style.display = 'none';
              let tdValidateCancel = document.createElement('td');
              tdValidateCancel.className='table_cell';
              tdValidateCancel.textContent = "Êtes-vous certain ?";
              let divCancel =document.createElement('div');
              divCancel.style.marginTop = '10px';
              divCancel.style.marginBottom = '5px';
              let aValidateCancelYes = document.createElement('a');
              aValidateCancelYes.href = `${window.location.origin}/event_delete_rec/${value['details']['uuid']}/?date=${i[0]}`;
              aValidateCancelYes.title = `Oui, annuler la distribution du ${i[0]}`;
              let iValidateCancelYes = document.createElement('i');
              iValidateCancelYes.className = "fas fa-check-square";
              iValidateCancelYes.style.marginRight = '10px';
              let aValidateCancelNo = document.createElement('a');
              aValidateCancelNo.title = 'Non, laisser la date';
              let iValidateCancelNo = document.createElement('i');
              iValidateCancelNo.className = "far fa-window-close";
              iValidateCancelNo.style.marginLeft = '5px';
              tr.append(tdValidateCancel);
              tdValidateCancel.append(divCancel);
              divCancel.append(aValidateCancelYes)
              divCancel.append(aValidateCancelNo)
              aValidateCancelYes.append(iValidateCancelYes);
              aValidateCancelNo.append(iValidateCancelNo);
              iValidateCancelNo.addEventListener('click', () => {
                tdValidateCancel.style.display='none';
                tdCancelDate.style.display = 'block';
            })
          })
        } else {
              tdCancelDate.innerHTML = 'annulé';
              let aURLCancelDate = document.createElement('a');
              aURLCancelDate.title = `Réactiver la distribution du ${i[0]}`;
              let iCancelDate = document.createElement('i');
              iCancelDate.className = "far fa-check-circle";
              tdCancelDate.append(aURLCancelDate);
              aURLCancelDate.append(iCancelDate);
              aURLCancelDate.addEventListener('click', () => {
                tdCancelDate.style.display = 'none';
                let tdValidateCancel = document.createElement('td');
                tdValidateCancel.className='table_cell';
                tdValidateCancel.textContent = "Réactiver cette date ?";
                let divCancel =document.createElement('div');
                divCancel.style.marginTop = '10px';
                divCancel.style.marginBottom = '5px';
                let aValidateCancelYes = document.createElement('a');
                aValidateCancelYes.href = `${window.location.origin}/reactivate_event_date/${value['details']['uuid']}/?date=${i[0]}`;
                aValidateCancelYes.title = `Oui, remettre la distribution du ${i[0]}`;
                let iValidateCancelYes = document.createElement('i');
                iValidateCancelYes.className = "fas fa-check-square";
                iValidateCancelYes.style.marginRight = '10px';
                let aValidateCancelNo = document.createElement('a');
                aValidateCancelNo.title = 'Non, laisser cette date annulée';
                let iValidateCancelNo = document.createElement('i');
                iValidateCancelNo.className = "far fa-window-close";
                iValidateCancelNo.style.marginLeft = '5px';
                tr.append(tdValidateCancel);
                tdValidateCancel.append(divCancel);
                divCancel.append(aValidateCancelYes)
                divCancel.append(aValidateCancelNo)
                aValidateCancelYes.append(iValidateCancelYes);
                aValidateCancelNo.append(iValidateCancelNo);
                iValidateCancelNo.addEventListener('click', () => {
                  tdValidateCancel.style.display='none';
                  tdCancelDate.style.display = 'block';
              })
            })
          }
        }

        })
        eventManagerDate = document.querySelectorAll('.event_manager_date');



        let sendMessagesFormButton = document.querySelector('#send_messages_form_button');
        let sendMessagesGlobal = document.querySelector('#send_messages_global');
        let iconMessage = document.querySelectorAll('#message_icon_button');
        iconMessage.forEach(i => {
          i.addEventListener('click', () => {
            sendMessagesGlobal.style.display = 'block';
            sendMessagesFormButton.dataset.event = i.dataset.event;
            sendMessagesFormButton.dataset.date= i.dataset.date;
          })
        })

      } else {
        info_text.style.display = 'block';
        tableEvent.style.display = 'none';
        document.querySelector('.view_more_event_manager').style.display = 'none';
      }

    });

}

  let days = 31;

  buttonEvenManagerLoad.addEventListener('click', (e) => {
    e.preventDefault();
    if (document.querySelector('.event_manager_date')) {
      let eventManagerDate = document.querySelectorAll('.event_manager_date');
      let fromDate = new Date(eventManagerDate[eventManagerDate.length -1].dataset.event_manager_date+"T00:00:00.000");
      fromDate.setDate(fromDate.getDate()+1);
      // +2 because need to search lat date visible+1 day and the search function looks on date-1 day --> NOT ANYMORE
      fromDateFinal = fromDate.toISOString().split('T')[0];
      let toDate = new Date(eventManagerDate[eventManagerDate.length -1].dataset.event_manager_date+"T00:00:00.000");
      toDate.setDate(toDate.getDate()+31);
      toDateFinal = toDate.toISOString().split('T')[0];
    } else {
      // fromDate = new Date();
      // // +1 because the search function looks on date-1 day
      // fromDate.setDate(fromDate.getDate()+1);
      // fromDateFinal = fromDate.toISOString().split('T')[0];
      // console.log(fromDateFinal);
      days+=14;
      toDate = new Date();
      toDate.setDate(toDate.getDate()+days);
      toDateFinal = toDate.toISOString().split('T')[0];
    }
    createDistrib(fromDateFinal, toDateFinal);
  })

  fromDate = new Date();
  // +1 because the search function looks on date-1 day --> NOT ANYMORE
  fromDate.setDate(fromDate.getDate());
  fromDateFinal = fromDate.toISOString().split('T')[0];
  // console.log(fromDateFinal);
  toDate = new Date();
  toDate.setDate(toDate.getDate()+days);
  toDateFinal = toDate.toISOString().split('T')[0];
  createDistrib(fromDateFinal, toDateFinal);


} else {
  events14Days.style.display = 'block';
  messages.style.display = 'none';

  events14DaysMenu.addEventListener('click', () => {
    events14Days.style.display = 'block';
    messages.style.display = 'none';
  })

  messagesMenu.addEventListener('click', () => {
    events14Days.style.display = 'none';
    messages.style.display = 'block';
  })

  }



// MESSAGES

let messageReceivedDiv = document.querySelector('#received_messages');
let aMessageReceivedDiv = document.querySelector('#a_received_messages');
let messageSentDiv = document.querySelector('#sent_messages');
let aMessageSentDiv = document.querySelector('#a_sent_messages');
messageSentDiv.style.display = 'none';

aMessageReceivedDiv.addEventListener('click', () => {
  messageReceivedDiv.style.display = 'block';
  messageSentDiv.style.display = 'none';
  aMessageSentDiv.className = '';
  aMessageReceivedDiv.className = 'active';
})

aMessageSentDiv.addEventListener('click', () => {
  messageReceivedDiv.style.display = 'none';
  messageSentDiv.style.display = 'block';
  aMessageSentDiv.className = 'active';
  aMessageReceivedDiv.className = '';
})


let NotificationTopDiv = document.querySelector('#notification_messages_top');
NotificationTopDiv.style.display = 'none';

let allMessages = document.querySelectorAll('.message_unit_div');

let notificationMessagesSolo = document.querySelectorAll('.notification_messages_solo_div');

notificationMessagesSolo.forEach(i => {
  i.style.display = 'none';
})



function check_if_notif() {
  let url = `${window.location.origin}/get_info_if_new_messages/`;
  fetch(url)
    .then(response => response.json())
    .then(data => {
      // console.log(data);
      let countTopMsg = document.querySelector('#count_messages_new');
      if (data.length > 0) {
        NotificationTopDiv.style.display = 'block';
        countTopMsg.innerHTML = ` (${data.length})`;
        data.forEach(j => {
          notificationMessagesSolo.forEach(i => {
            if (j.uuid == i.dataset.message) {
              i.style.display = 'block';
            }
          })
        })
      } else {
        NotificationTopDiv.style.display = 'none';
        countTopMsg.style.display = 'none';
      }
    })

}



  function seen_messages() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
                      `${window.location.origin}/create_messages_seen/`,
                      {headers: {'X-CSRFToken': csrftoken}}
                  );
    const response = fetch(request, {
      method:'POST',
      mode: 'same-origin',
      body: JSON.stringify({
          }),
    })
    .then(response => response.json())
    .then(data => {
        // console.log(data);
      })
    }

    function seen_message(message) {
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      const request = new Request(
                        `${window.location.origin}/create_message_seen/`,
                        {headers: {'X-CSRFToken': csrftoken}}
                    );
      const response = fetch(request, {
        method:'POST',
        mode: 'same-origin',
        body: JSON.stringify({
          message:message
          }),
      })
      .then(response => response.json())
      .then(data => {
          // console.log(data);
          if (data) {
            notificationMessagesSolo.forEach(j => {
              if (message == j.dataset.message) {
                j.style.display = 'none';
              }
            })
          }
          check_if_notif();
        })
      }


  allMessages.forEach(i => {
    i.addEventListener('click', () => {
      seen_message(i.dataset.message);
    })
  })

  check_if_notif();



});
