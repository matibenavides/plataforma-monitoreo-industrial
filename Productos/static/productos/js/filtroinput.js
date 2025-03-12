function filtro(input, maxLength) {
  // Elimina caracteres que no sean dígitos, coma o punto
  input.value = input.value.replace(/[^0-9,.]/g, '');
  // Limita caracteres
  if (input.value.length > maxLength) {
    input.value = input.value.slice(0, maxLength);
  }
}