document.addEventListener("DOMContentLoaded", function () {

  let locationDetailsMenu = document.querySelector('#location_details_menu');
  let locationSoireeMenu = document.querySelector('#location_soirees_menu');

  let locationDetails = document.querySelector('.location_global');
  let locationSoiree = document.querySelector('#soirees');

  locationSoiree.style.display = 'none';

  locationDetailsMenu.addEventListener('click', () => {
    locationDetails.style.display = 'flex';
    locationSoiree.style.display = 'none';
  })

  locationSoireeMenu.addEventListener('click', () => {
    locationDetails.style.display = 'none';
    locationSoiree.style.display = 'contents';
  })


});
