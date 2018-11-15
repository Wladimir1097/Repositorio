$(function () {

    $('#frmForm').formValidation({
        message: 'El valor no es valido',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            date_joined: {
                validators: {
                    date: {
                        format: 'YYYY-MM-DD',
                        message: 'La fecha no es válida'
                    }
                }
            },
            description: {
                validators: {
                    stringLength: {
                        min: 4
                    }
                }
            },
            image: {
                validators: {
                    file: {
                        extension: 'jpeg,jpg,png',
                        type: 'image/jpeg,image/png',
                        maxFiles: 1,
                        message: 'Introduzca una imagen válida'
                    }
                }
            }
        }
    })
        .on('err.validator.fv', function (e, data) {
            data.element
                .data('fv.messages')
                .find('.help-block[data-fv-for="' + data.field + '"]').hide()
                .filter('[data-fv-validator="' + data.validator + '"]').show();
        }).on('success.field.fv', function (e, data) {
        var $parent = data.element.parents('.form-group');
        $parent.removeClass('has-success');
        data.element.data('fv.icon').hide();
    })
        .on('success.form.fv', function (e) {
            e.preventDefault();
            var message = get_message_action_by_id(parseInt($('#id').val()));
            save_registry_by_submit(e, message, function () {
                location.href = pathname;
            });
        });

    $('#id_date_joined').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        orientation: 'bottom bottom',
        language: 'es'
    }).on('changeDate', function (e) {
        $('#frmIngress').formValidation('revalidateField', 'date_joined');
    });
});
