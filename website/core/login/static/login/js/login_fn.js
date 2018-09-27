$(function () {

    $('#frmLogin').formValidation({
        message: 'This value is not valid',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            username: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 3,
                    }
                }
            },
            password: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 3,
                        max: 15
                    }
                }
            }
        }
    }).on('success.field.fv', function(e, data) {
            var $parent = data.element.parents('.form-group');
            $parent.removeClass('has-success');
            data.element.data('fv.icon').hide();
        })
        .on('success.form.fv', function (e) {
        e.preventDefault();
        $.ajax({
            url: pathname,
            data: {
                username: $('#username').val(),
                password: $('#password').val(),
                action: 'connect'
            },
            method: 'POST',
            success: function (data) {
                if (data.resp) {
                    message_url(data.msg,data.url);
                    return false;
                }
                error_message(data.error);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                error_message(errorThrown + ' ' + textStatus);
            },
            complete: function () {
                $('#frmLogin').formValidation('resetForm', true);
                $('#username').focus();
            }
        });
    });

    $('#reset_password').on('click',function () {
        $('#myModalResetPassword').modal('show');
        $('#email').focus();
    });

    $('#myModalResetPassword').on('hidden.bs.modal', function() {
        $('#frmResetPassword').formValidation('resetForm', true);
    });

    $('#frmResetPassword').formValidation({
        message: 'El valor no es valido',
        excluded: ':disabled',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh',
        },
        fields: {
            email: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 5
                    },
                    regexp: {
                        regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
                        message: 'Ingrese un email correcto'
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
        })
        .on('success.form.fv', function (e) {
            e.preventDefault();
            action_by_ajax_with_alert('Notificación',
                '¿Estas seguro de resetear tu contraseña?',
                pathname,
                {
                    action: 'reset_password', email : $('#email').val()
                },
                function () {
                    location.reload();
                },
                'Te hemos enviado un correo con los pasos que debes seguir para cambiar tu contraseña'
            );
        });
});


