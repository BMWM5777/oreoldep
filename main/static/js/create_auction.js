document.addEventListener('DOMContentLoaded', function() {
  var addPhotoButton = document.getElementById('add-photo');
  addPhotoButton.addEventListener('click', function(e) {
    e.preventDefault();
    var formContainer = document.querySelector('.auction-photos-flex');
    // Получаем префикс из data-атрибута
    var prefix = formContainer.getAttribute('data-form-prefix');
    var totalFormsInput = document.querySelector('[name="' + prefix + '-TOTAL_FORMS"]');
    var formCount = parseInt(totalFormsInput.value);

    var emptyFormTemplate = document.getElementById('empty-form-template').innerHTML;
    var newFormHtml = emptyFormTemplate.replace(/__prefix__/g, formCount);

    formContainer.insertAdjacentHTML('beforeend', newFormHtml);
    totalFormsInput.value = formCount + 1;
  });
});
