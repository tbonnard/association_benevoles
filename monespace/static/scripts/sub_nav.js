document.addEventListener("DOMContentLoaded", function () {

if (document.querySelectorAll('.sub_nav_hor')) {

  let subMenus = document.querySelectorAll('.sub_nav_hor');

  subMenus.forEach( i => {
    i.addEventListener('click', () => {
      window.scrollTo({top:0,left:0,behavior:'smooth'});
      currentActive = document.querySelectorAll('.sub_nav_hor.active');
      i.className += " active";
      currentActive[0].className = "sub_nav_hor";
    })
  })
}


});
