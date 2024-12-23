function calculosumhi() {
    let sum = 0;
    for (let i = 1; i <= 11; i++) {
        sum += parseInt(document.getElementById(`su_hi_${i}`).value) || 0;
    }
    document.getElementById("gastohipoclorito").value = sum;
}

function calculosumac() {
    let sum = 0;
    for (let i = 1; i <= 11; i++) {
        sum += parseInt(document.getElementById(`su_ac_${i}`).value) || 0;
    }
    document.getElementById("gastoacido").value = sum;
}


/// Concepto inicial ///
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
