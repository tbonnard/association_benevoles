document.addEventListener("DOMContentLoaded", function () {

  let sendMessagesGlobal = document.querySelector('#send_messages_global');
  let successMessages = document.querySelector('#success_message_result');
  let sendMessagesDiv = document.querySelector('#send_message_div');
  let sendMessagesFormButton = document.querySelector('#send_messages_form_button');


  let event_id = null;
  let event_date = null;
  let group = null;
  let all_site = false;
  let user = null;
  let site = null;
  let groupField = null;
  let groupFieldManager = null;
  let subject = null;
  let subjectField = document.querySelector('#id_subject');
  let descriptionField = document.querySelector('#id_description');
  const borderColor = "#cacaca";

  if (document.querySelector('#id_to_event_group')) {
    groupField = document.querySelector('#id_to_event_group');
  }

  if (document.querySelector('#id_to_event_manager_group')) {
    groupFieldManager = document.querySelector('#id_to_event_manager_group');
  }


   let listFieldsValidation = [descriptionField,subjectField]
   if (groupField != null) {
     listFieldsValidation.push(groupField)
     }
  if (groupFieldManager != null) {
    listFieldsValidation.push(groupFieldManager)
       }

  let close_message_box = document.querySelector('#close_message_box');

  close_message_box.addEventListener('click',() =>{
    sendMessagesGlobal.style.display = 'none';
    listFieldsValidation.forEach(i => {
        i.style.borderColor = borderColor;
        i.value = null;
    })
  })

  function send_message(event_id, event_date, all_site, user, site, group, description, subject, groupManager) {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const request = new Request(
                      `${window.location.origin}/send_message/`,
                      {headers: {'X-CSRFToken': csrftoken}}
                  );
    const response = fetch(request, {
      method:'POST',
      mode: 'same-origin',
      body: JSON.stringify({
              event: event_id,
              date: event_date,
              all_site: all_site,
              user: user,
              site: site,
              group: group,
              description: description,
              subject:subject,
              groupManager:groupManager
          }),
    })
    .then(response => response.json())
    .then(data => {
      console.log(data);
    })

    }


  sendMessagesFormButton.addEventListener('click', (e) => {
    let description = descriptionField.value;
    let validationNumber = 0

    listFieldsValidation.forEach(i => {
      if (i.value != '') {
        validationNumber+=1
      }
    })

    if (validationNumber == listFieldsValidation.length) {

      subject = subjectField.value;

      if (groupField != null) {
        group = groupField.value;
      } else {group = 1}

      if (groupFieldManager != null) {
        groupManager = groupFieldManager.value;
      } else {groupManager = null}



       if (sendMessagesFormButton.dataset.event) {
         event_id = sendMessagesFormButton.dataset.event
       }
       if (sendMessagesFormButton.dataset.site) {
         site = sendMessagesFormButton.dataset.site
       }
       if (sendMessagesFormButton.dataset.date) {
         event_date = sendMessagesFormButton.dataset.date
       }
       if (sendMessagesFormButton.dataset.all_site) {
         all_site = sendMessagesFormButton.dataset.all_site
       }
       if (sendMessagesFormButton.dataset.user) {
         user = sendMessagesFormButton.dataset.user
       }

       send_message(event_id, event_date, all_site, user, site, group, description, subject, groupManager);

       listFieldsValidation.forEach(i => {
           i.style.borderColor = borderColor;
           i.value = null;
       })

       sendMessagesDiv.style.display = 'none';
       successMessages.style.display = 'block';
       setTimeout(function(){
         sendMessagesGlobal.style.display = 'none';
         successMessages.style.display = 'none';
         sendMessagesDiv.style.display = 'block';
         window.location.reload(true);
      }, 2000);



    } else {
      listFieldsValidation.forEach(i => {
        if (i.value == '') {
          i.style.borderColor = "red";
        }
      })
    }

  })


});
