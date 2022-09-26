document.addEventListener("DOMContentLoaded", function () {

  let tr_td_row = document.querySelectorAll('.tr_td_row');
  let td_row = document.querySelectorAll('.td_row');
  let locationCheckBox = document.querySelectorAll('.locations_checkbox');
  let locationsName = document.querySelectorAll('.locations_name');
  let distribCheckBox = document.querySelectorAll('.distrib_checkbox');
  let infoIconEventManager = document.querySelectorAll('.info_icon');
  const user_id = document.querySelector('#us');


  infoIconEventManager.forEach(i => {
    i.style.visibility = 'hidden';
  })

  tr_td_row.forEach(i => {
    i.style.display = 'none';
  })

  // get_event_location();
  get_user_distrib()


  locationCheckBox.forEach(j => {
    j.addEventListener('click', () => {
      tr_td_row.forEach(z => {
        if (j.dataset.state == 'closed') {
          if (z.dataset.loc == j.dataset.loc) {
            z.style.display = 'contents';
            j.dataset.state = 'open'
            j.innerHTML = "<i class='fas fa-chevron-up'></i>"
            locationsName.forEach(c => {
              if (c.dataset.loc == j.dataset.loc) {
                c.dataset.state='open';
              }
            })
          }
        } else {
          if (z.dataset.loc == j.dataset.loc) {
            z.style.display = 'none';
            j.dataset.state = 'closed'
            j.innerHTML = "<i class='fas fa-chevron-down'></i>"
            locationsName.forEach(c => {
              if (c.dataset.loc == j.dataset.loc) {
                c.dataset.state='closed';
              }
            })
          }
        }

      })
    })
    get_count_event_location(j.dataset.loc);
  })

  locationsName.forEach(j => {
    j.addEventListener('click', () => {
      tr_td_row.forEach(z => {
        if (j.dataset.state=='closed') {
          if (z.dataset.loc == j.dataset.loc) {
            z.style.display = 'contents';
            j.dataset.state='open';
            locationCheckBox.forEach(c => {
              if (c.dataset.loc == j.dataset.loc) {
                c.dataset.state='open';
                c.innerHTML = "<i class='fas fa-chevron-up'></i>"
              }
            })
          }
        } else {
          if (z.dataset.loc == j.dataset.loc) {
            z.style.display = 'none';
            j.dataset.state='closed';
            locationCheckBox.forEach(c => {
              if (c.dataset.loc == j.dataset.loc) {
                c.dataset.state='closed';
                c.innerHTML = "<i class='fas fa-chevron-down'></i>"
              }
            })
          }
        }

      })
    })
    get_count_event_location(j.dataset.loc);
  })

  function get_count_event_location (location_id) {
    const request = new Request(`${window.location.origin}/get_count_event_location/${location_id}/`);
    const response = fetch(request, {
      method:'GET',
      mode: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
      if (data == 0) {
        td_row.forEach(a => {
          if (a.dataset.loc == location_id) {
            a.innerHTML = "<span class='info_text'>Aucune distribution pour ce site actuellement</span>";
          }
        })
        locationsName.forEach(i => {
          if (i.dataset.loc == location_id) {
                i.style.color='#222222';
          }
        })
        locationCheckBox.forEach(y => {
          if (y.dataset.loc == location_id) {
            y.style.color='#222222';
          }
        })
      } else {
        tr_td_row.forEach(a => {
          if (a.dataset.loc == location_id) {
            a.style.display = "contents";
          }
        })
        locationsName.forEach(i => {
          if (i.dataset.loc == location_id) {
                i.dataset.state='open';
          }
        })
        locationCheckBox.forEach(y => {
          if (y.dataset.loc == location_id) {
            y.dataset.state='open';
            y.innerHTML = "<i class='fas fa-chevron-up'></i>";
          }
        })
      }


    })
  }


  // function get_event_location() {
  //   const request = new Request(`${window.location.origin}/get_event_location/`);
  //   const response = fetch(request, {
  //     method:'GET',
  //     mode: 'same-origin'
  //   })
  //   .then(response => response.json())
  //   .then(data => {
  //     data.forEach(i => {
  //       // console.log(i);
  //       locationCheckBox.forEach(j => {
  //         if (j.dataset.loc == i.location.id) {
  //         } else {
  //           // j.style.display = 'none';
  //         }
  //       })
  //       locationsName.forEach(y => {
  //         if (y.dataset.loc == i.location.id) {
  //         } else {
  //           // y.style.pointerEvents="none";
  //           // y.style.cursor="default";
  //           // y.style.color='#222222';
  //         }
  //       })
  //     })
  //   })
  // }

  function get_user_distrib() {
    const request = new Request(`${window.location.origin}/get_user_distrib/`);
    const response = fetch(request, {
      method:'GET',
      mode: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
      data.forEach(i => {
        distribCheckBox.forEach(j => {
          if (i.id_distrib == j.value) {
            j.checked = true;
          }
          if (i.user_id == j.dataset.distrib_us) {
            j.style.visibility = 'hidden';
          }
        })
        // locationCheckBox.forEach(z => {
        //   if (i.location_id == z.dataset.loc) {
        //     z.innerHTML="<i class='fas fa-chevron-up'></i>";
        //     z.dataset.state='open';
        //   }
        // })
        // tr_td_row.forEach(a => {
        //   if (a.dataset.loc == i.location_id) {
        //     a.style.display = 'contents';
        //   }
        // })
        // locationsName.forEach(b => {
        //   if (b.dataset.loc == i.location_id) {
        //     b.dataset.state='open';
        //   }
        // })
        infoIconEventManager.forEach(c => {
          if(i.user_id == c.dataset.distrib_us) {
            c.style.visibility = '';
          }
        })
      })
    })

  }




});
