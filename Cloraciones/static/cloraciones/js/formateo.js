function formateo(input) {
    var inputField = document.querySelector('input')

  input.onkeyup = function(){
    var removeChar = this.value.replace(/[^0-9\.]/g, '')

    var removeDot = removeChar.replace(/\,/g, '')
    this.value = removeDot

    var formatedNumber = this.value.replace(/\B(?=(\d{1})+(?!\d))/g, '.');
    this.value = formatedNumber
  }
  }

  

  