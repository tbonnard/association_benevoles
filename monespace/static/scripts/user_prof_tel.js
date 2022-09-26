document.addEventListener("DOMContentLoaded", function () {

  function Verifier_Numero_Telephone(num_tel)
  {
  	// Definition du motif a matcher
  	const regex = new RegExp(/^(01|02|03|04|05|06|08)[0-9]{8}/gi);

  	// Definition de la variable booleene match
  	let match = false;

  	// Test sur le motif
  	if(regex.test(num_tel) && num_tel.length <= 10)
  	{
  		match = true;
  	}
  	  else
  	{
  		match = false;
  	}

  	// On renvoie match
  	return match;
  }


  let telInput = document.querySelector('#id_tel');
  let buttonConfirm = document.querySelector('#confirm');


  telInput.addEventListener('keyup', () => {
    if (telInput.value.length > 0) {
      buttonConfirm.disabled = true;
      let phoneFormatVal = Verifier_Numero_Telephone(telInput.value);
      if (phoneFormatVal) {
        buttonConfirm.disabled = false;
      }
    } else {
      buttonConfirm.disabled = false;
    }

  })







});
