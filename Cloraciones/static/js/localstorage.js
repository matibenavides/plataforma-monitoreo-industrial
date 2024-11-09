// Función para cargar los datos guardados en localStorage al iniciar la página
function cargarBorrador(seccion) {
    const form = document.getElementById(`form-${seccion}`);
    
    if (!form) {
        console.error('Formulario con id form-${seccion} no encontrado.');
        return;
    }
    
    // Obtiene los datos del borrador en formato JSON
    const data = JSON.parse(localStorage.getItem(`borrador-${seccion}`)) || {};
    
    // Asigna los valores a cada campo del formulario
    for (const [name, value] of Object.entries(data)) {
        const input = form.elements[name];
        if (input) {
            input.value = value;
        }
    }
}

// Función para mostrar el nuevo Toast de validación
function mostrarToastSector(mensaje) {
    const toastBody = document.querySelector("#SectorToast .toast-body");
    if (toastBody) {
        toastBody.textContent = mensaje;
    }

    const toastElement = document.getElementById("SectorToast");
    if (toastElement) {
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
    }
}

// Función para guardar los datos en localStorage al hacer clic en "Guardar Borrador"
function guardarBorrador(seccion) {
    const form = document.getElementById(`form-${seccion}`);
    
    if (!form) {
        console.error(`Formulario con id form-${seccion} no encontrado.`);
        return;
    }
    
    const data = {};
    Array.from(form.elements).forEach(input => {
        if (input.name) {
            data[input.name] = input.value;
        }
    });

    // Guarda el objeto `data` como JSON en localStorage
    localStorage.setItem(`borrador-${seccion}`, JSON.stringify(data));
    mostrarToastSector("Borrador guardado para " + seccion);
}

// Función para eliminar los datos del borrador en localStorage cuando se envían los datos
function eliminarBorrador(seccion) {
    localStorage.removeItem(`borrador-${seccion}`);
    console.log(`Borrador de la sección ${seccion} eliminado.`);
}

// Función para mostrar el nuevo Toast de validación
function mostrarToastRequired(mensaje) {
    const toastBody = document.querySelector("#validationToast .toast-body");
    if (toastBody) {
        toastBody.textContent = mensaje;
    }

    const toastElement = document.getElementById("validationToast");
    if (toastElement) {
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
    }
}


// Función que se llama cuando se envían los datos
function enviarDatos(event, seccion) {
    // Previene el envío predeterminado del formulario si hay campos vacíos
    event.preventDefault();

    // Obtiene el formulario
    const form = document.getElementById(`form-${seccion}`);
    
    // Verifica si todos los campos requeridos están llenos
    let allFieldsValid = true;
    Array.from(form.elements).forEach(input => {
        if (input.required && !input.value) {
            allFieldsValid = false;
            mostrarToastRequired("Asegúrate de completar los campos obligatorios, como: Turno, Especie y Lotes de Producto.");
        }
    });

    // Si hay campos vacíos, no borres el borrador ni envíes el formulario
    if (!allFieldsValid) {
        return;  // Detiene la ejecución de la función sin afectar el flujo de `enviarDatos`
    }

    // Si todos los campos son válidos, elimina los datos del borrador
    eliminarBorrador(seccion);

    // Envía el formulario
    form.submit();
}

// Cargar los borradores al iniciar la página para cada sección
window.onload = function() {
    cargarBorrador("estanque");
    cargarBorrador("corta-pedicelo");
    cargarBorrador("retorno");
};
