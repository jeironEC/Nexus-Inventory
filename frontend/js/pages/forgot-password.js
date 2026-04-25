/**
 * FORGOT-PASSWORD.JS
 * El fetch lo conectará el compañero de backend.
*/

document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('forgot-password-form');
    const submitBtn = document.getElementById('btn-submit');

    if (form && submitBtn) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();

            // Sustituir esto por el fetch real
            console.log('Formulario de recuperación enviado');
        });
    }

});
