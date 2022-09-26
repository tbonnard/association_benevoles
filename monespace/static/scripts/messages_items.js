document.addEventListener("DOMContentLoaded", function () {

  let answers = document.querySelectorAll('.message_unit_div_answer');
  answers.forEach(i => {
    i.style.display = 'none';
  })

  let divMessages = document.querySelectorAll('.message_unit_div');
  divMessages.forEach(j => {
    j.addEventListener('click', () => {
      answers.forEach(i => {
        let icon = document.querySelector(`#icon_left_right_${i.dataset.msg}`);
        if (i.dataset.msg == j.dataset.msg && i.dataset.state=='closed') {
          i.style.display = 'block';
          i.dataset.state='open';
          icon.className = "fas fa-2x fa-chevron-left";
          divMessages.forEach(z => {
            if (i.dataset.msg != z.dataset.msg ) {
              z.style.visibility = 'hidden';
            }
          })
        } else if (i.dataset.msg == j.dataset.msg && i.dataset.state=='open') {
          i.style.display = 'none';
          i.dataset.state='closed';
          icon.className = "fas fa-2x fa-chevron-right";
          divMessages.forEach(z => {
            if (i.dataset.msg != z.dataset.msg ) {
              z.style.visibility = 'visible';
            }
          })
        }
      })

    })

  })


  let answersSent = document.querySelectorAll('.message_unit_div_answer_sent');
  answersSent.forEach(i => {
    i.style.display = 'none';
  })

  let divMessagesSent = document.querySelectorAll('.message_unit_div_sent');
  divMessagesSent.forEach(j => {
    j.addEventListener('click', () => {
      answersSent.forEach(i => {
        let iconSent = document.querySelector(`#icon_lr_sent_${i.dataset.msgent}`);
          if (i.dataset.msg == j.dataset.msg && i.dataset.statesent=='closed') {
            i.style.display = 'block';
            i.dataset.statesent='open';
            iconSent.className = "fas fa-2x fa-chevron-left";
            divMessagesSent.forEach(z => {
              if (i.dataset.msg != z.dataset.msg ) {
                z.style.visibility = 'hidden';
              }
            })
          } else if (i.dataset.msg == j.dataset.msg && i.dataset.statesent=='open') {
            i.style.display = 'none';
            i.dataset.statesent='closed';
            iconSent.className = "fas fa-2x fa-chevron-right";
            divMessagesSent.forEach(z => {
              if (i.dataset.msg != z.dataset.msg ) {
                z.style.visibility = 'visible';
              }
            })
          }
      })
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


    let buttonReply = document.querySelectorAll('.button_reply');
    buttonReply.forEach(i => {
      i.addEventListener('click', (e) => {
        let inputValue = document.querySelector(`#msg${i.dataset.msg}`);
        let subject_pre = document.querySelector(`#subject_${i.dataset.msg}`);
        let subject = `Re: ${subject_pre.innerHTML}`
        if (inputValue.value != '') {
          send_message(null, null, false, i.dataset.to, null, 1, inputValue.value, subject, null);
        }
      })
    })



});
