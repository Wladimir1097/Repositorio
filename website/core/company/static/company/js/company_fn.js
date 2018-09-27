$(function () {

    $('#id_name,#proprietor').keypress(function (e) {
        return validate_form_text('letters',e,null);
    });

    $('#id_ruc,#id_mobile,#id_phone').keypress(function (e) {
        return validate_form_text('numbers',e,null);
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
            name: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 4,
                    },
                }
            },
            proprietor: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 4,
                    },
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
                    }
                }
            },
            phone: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 7,
                    },
                    digits: {}
                }
            },
            address: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 4,
                    }
                }
            },
            mission: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 4,
                    }
                }
            },
            vision: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 4,
                    }
                }
            },
            about_us: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 4,
                    }
                }
            },
            icon: {
                notEmpty: {},
                validators: {
                    file: {
                        extension: 'jpeg,jpg,png',
                        type: 'image/jpeg,image/png',
                        maxFiles: 1,
                        message: 'Introduce una imagen válida'
                    }
                }
            },
            ruc: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 13,
                    },
                    digits: {},
                    callback: {
                        message: 'Ruc inválido',
                        callback: function (value, validator, $field) {
                            return validate_dni_ruc(value);
                        }
                    }
                }
            },
            schedule: {
                validators: {
                    notEmpty: {},
                }
            },

        }
    })
        .on('err.validator.fv', function (e, data) {
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
