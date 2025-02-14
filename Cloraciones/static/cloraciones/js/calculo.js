function calculosumhi(inputElement) {
    const table = inputElement.getAttribute("data-table");

    const inputs = document.querySelectorAll(`[data-table="${table}"][data-type="hipoclorito"]`);

    let total = 0;

    inputs.forEach((input) => {
        total += parseInt(input.value) || 0;
    });

    const sumatotal = document.getElementById(`gastohipoclorito_${table}`);
    sumatotal.value = total;
}

function calculosumac(inputElement) {

    const table = inputElement.getAttribute("data-table");

    const inputs = document.querySelectorAll(`[data-table="${table}"][data-type="acido"]`);

    let total = 0;

    inputs.forEach((input) => {
        total += parseInt(input.value) || 0;
    });

    const sumatotal = document.getElementById(`gastoacido_${table}`);
    sumatotal.value = total;
}

function calcularSumaInicial() {
    // Simular un evento input en cualquiera de los campos para triggear la suma
    const primerInput = document.getElementById('su_hi_1');
    if(primerInput) {
        calculosumhi(primerInput);
        calculosumac(primerInput);
    }

    
}
/// Concepto inicial ///
/// Primer función pensando en la toma y suma de datos, no es útil para multiples tablas de inputs

// function calculosum(){
//     var num1 = parseInt(document.getElementById("su_1").value) || 0,
//         num2 = parseInt(document.getElementById("su_2").value) || 0,
//         num3 = parseInt(document.getElementById("su_3").value) || 0,
//         num4 = parseInt(document.getElementById("su_4").value) || 0,
//         num5 = parseInt(document.getElementById("su_5").value) || 0,
//         num6 = parseInt(document.getElementById("su_6").value) || 0,
//         num7 = parseInt(document.getElementById("su_7").value) || 0,
//         num8 = parseInt(document.getElementById("su_8").value) || 0,
//         num9 = parseInt(document.getElementById("su_9").value) || 0,
//         num10 = parseInt(document.getElementById("su_10").value) || 0,
//         num11 = parseInt(document.getElementById("su_11").value) || 0;

//     document.getElementById("gastohipoclorito").value = num1 + num2 + num3 + num4 + num5 + num6 + num7 + num8 + num9 + num10 + num11;
// }

/// Concepto sin pensar en multiples tablas de inputs ///
/// Cambie la función pensando en que poseo 3 tablas de datos, por ende el identificador multiple o "repetido" se veria mal esteticamente, por ende opto
/// por el data-* y el data-type* para separarlos por identificador por tablas tipo  gastoacido_estanque / gastoacido_retorno / etc. 


// function calculosumhi() {
//     let sum = 0;
//     for (let i = 1; i <= 11; i++) {
//         sum += parseInt(document.getElementById(`su_hi_${i}`).value) || 0;
//     }
//     document.getElementById("gastohipoclorito_estanque").value = sum;
// }


// de todas formas dejare el id de su_hi_{i} y su_ac_{i} en la tabla estanque.html para dar idea de esta funcionalidad.