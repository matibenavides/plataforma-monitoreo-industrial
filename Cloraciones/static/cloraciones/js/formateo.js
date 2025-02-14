function formateo(input) {
  
  function formatValue() {
    var removeChar = input.value.replace(/[^0-9\.]/g, '')
    var removeDot = removeChar.replace(/\,/g, '')
    input.value = removeDot
    var formatedNumber = input.value.replace(/\B(?=(\d{1})+(?!\d))/g, '.');
    input.value = formatedNumber
  }

  
  formatValue();

  
  input.onkeyup = formatValue;
}


document.addEventListener('DOMContentLoaded', function() {
  
  var inputs = document.querySelectorAll('input[type="text"]');
  inputs.forEach(input => formateo(input));
});