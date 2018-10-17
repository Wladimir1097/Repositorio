$(function () {

    $('#id_ruc,#id_phone').keypress(function (e) {
        return validate_form_text('numbers',e,null);
    });

    $('#id_name').keypress(function (e) {
        return validate_form_text('letters',e,null);
    });

    $('#frmForm').formValidation({
        message: 'This value is not valid',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        excluded: ':disabled',
        fields: {
            ruc: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 13,
                    },
                    digits: {},
                    callback: {
                        message: 'Ruc invalido',
                        callback: function (value, validator, $field) {
                            return validate_dni_ruc(value);
                        }
                    }
                }
            },
            email: {
                validators: {
                    stringLength: {
                        min: 5
                    },
                    regexp: {
                        regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
                        message: 'El email no es correcto'
                    }
                }
            },
            mobile: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 10,
                    },
                    digits: {},
                    callback: {
                        message: 'El número de celular no es válido',
                        callback: function (value, validator, $field) {
                            return value === '' || $field.intlTelInput('isValidNumber');
                        }
                    },
                }
            },
            address: {
                validators: {
                    stringLength: {
                        min: 4,
                    }
                }
            }
        }
    }).on('err.validator.fv', function (e, data) {
        data.element
            .data('fv.messages')
            .find('.help-block[data-fv-for="' + data.field + '"]').hide()
            .filter('[data-fv-validator="' + data.validator + '"]').show();
    }).on('success.field.fv', function(e, data) {
            var $parent = data.element.parents('.form-group');
            $parent.removeClass('has-success');
            data.element.data('fv.icon').hide();
        })
        .on('success.form.fv', function (e) {
            e.preventDefault();
           var message = get_message_action_by_id(parseInt($('#id').val()));
            save_registry_by_submit(e,message,function () {
                location.href = pathname;
            });
        });
});
