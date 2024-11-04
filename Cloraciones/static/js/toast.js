document.addEventListener('DOMContentLoaded', function () {
    const toastElement = document.getElementById('liveToast');
    if (toastElement) {
        const toast = new bootstrap.Toast(toastElement);
        toast.show();  // Muestra el toast automáticamente
    }
});