document.addEventListener('DOMContentLoaded', function() {
    const textareas = document.querySelectorAll('textarea');
    
    textareas.forEach(textarea => {
        const defaultHeight = '33px';
        textarea.style.height = defaultHeight;
        
        // Función para ajustar altura
        const adjustHeight = (element) => {
            if (element.value === '') {
                element.style.height = defaultHeight;
            } else {
                element.style.height = 'auto';
                element.style.height = element.scrollHeight + 'px';
            }
        };
        
        // Ajustar altura inicial si hay contenido
        adjustHeight(textarea);
        
        // Eventos existentes
        textarea.addEventListener('input', function() {
            adjustHeight(this);
        });
        
        textarea.addEventListener('blur', function() {
            if (this.value === '') {
                this.style.height = defaultHeight;
            }
        });
    });
});