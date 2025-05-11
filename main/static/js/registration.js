document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.reg-password-toggle').forEach(button => {
        button.addEventListener('click', () => {
            const input = button.parentElement.querySelector('input');
            const icon = button.querySelector('i');
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            icon.classList.toggle('fa-eye');
            icon.classList.toggle('fa-eye-slash');
        });
    });

    const form = document.querySelector('.reg-form');
    if(form) {
        form.addEventListener('submit', function(e) {
            const password1 = document.getElementById('id_password1');
            const password2 = document.getElementById('id_password2');
            
            if(password1.value !== password2.value) {
                e.preventDefault();
                alert('{% trans "Пароли не совпадают!" %}');
                password2.focus();
            }
            
            if(password1.value.length < 8) {
                e.preventDefault();
                alert('{% trans "Пароль должен содержать минимум 8 символов!" %}');
                password1.focus();
            }
        });
    }
});