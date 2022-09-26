document.addEventListener("DOMContentLoaded", function () {

  let startDate = document.querySelector('#id_start_date');
  let dayValue = document.querySelector('#id_dayValue');
  let nameDistrib = document.querySelector('#id_name');
  let time_from = document.querySelector('#id_time_from');

  const weekday = ["Dimanche","Lundi","Mardi","Mercredi","Jeudi","vendredi","Samedi"];


  startDate.addEventListener('change', () => {
    changeDayName();
  })

  function changeDayName() {
    let valueDate = startDate.value + "T00:00:00.000";
    let d = new Date(valueDate);
    let day = d.getDay();
    nameDistrib.value = `Distribution du ${weekday[day]}`;
  }

  changeDayName();


});
