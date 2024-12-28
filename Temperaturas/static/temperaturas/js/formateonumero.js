function formatearNumero(input) {
    // Eliminar caracteres no numéricos excepto el punto
    let valor = input.value.replace(/[^\d.]/g, '');
    
    // Eliminar puntos existentes para manejar nuevo formato
    valor = valor.replace(/\./g, '');
    
    // Aplicar formato según la cantidad de dígitos
    if (valor.length === 2) {
        // Si hay 2 dígitos, insertar punto después del primero (1.2)
        valor = valor.slice(0, 1) + '.' + valor.slice(1);
    } else if (valor.length === 3) {
        // Si hay 3 dígitos, insertar punto después del segundo (12.3)
        valor = valor.slice(0, 2) + '.' + valor.slice(2);
    }
    
    // Limitar a máximo 4 caracteres
    valor = valor.slice(0, 4);
    
    // Actualizar el valor del input
    input.value = valor;
}