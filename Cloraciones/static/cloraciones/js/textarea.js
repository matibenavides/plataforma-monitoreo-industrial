document.addEventListener('DOMContentLoaded', function() {
    const textareas = document.querySelectorAll('textarea');
    
    textareas.forEach(textarea => {
        const defaultHeight = '33px'; // Altura inicial
        
        // Establece la altura inicial
        textarea.style.height = defaultHeight;
        
        textarea.addEventListener('input', function() {
            // Si está vacío, vuelve a la altura por defecto
            if (this.value === '') {
                this.style.height = defaultHeight;
            } else {
                this.style.height = 'auto';
                this.style.height = this.scrollHeight + 'px';
            }
        });
        
        // Añade evento para cuando se borre todo el contenido
        textarea.addEventListener('blur', function() {
            if (this.value === '') {
                this.style.height = defaultHeight;
            }
        });
    });
});