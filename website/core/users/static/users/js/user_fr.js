$(function () {
    $('#id_birthdate').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        orientation: 'top bottom',
        language: 'es'
    }).on('changeDate', function (e) {
        $('#frmForm').formValidation('revalidateField', 'birthdate');
    });

    $('.select2').select2({
        placeholder: "Buscar..",
        tags: true,
        //maximumSelectionLength: 1,
        language: "es"
    });

    $('#id_username').keypress(function (e) {
        return validate_form_text('letters_numbers_spaceless', e, null);
    });

    $('#id_first_name,#id_last_name').keypress(function (e) {
        return validate_form_text('letters', e, null);
    });

    $('#id_phone,#id_dni,#id_mobile').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('#id_address').keypress(function (e) {
        return validate_form_text('numbers_letters', e, null);
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
            first_name: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 4,
                    },
                    regexp: {
                        regexp: /^[A-ZáéíóúÁÉÍÓÚñÑ\s]+$/i,
                        message: 'El primer nombre solo puede consistir en caracteres alfabéticos'
                    },
                }
            },
            last_name: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 4,
                    },
                    regexp: {
                        regexp: /^[A-ZáéíóúÁÉÍÓÚñÑ\s]+$/i,
                        message: 'El segundo apellido solo puede consistir en caracteres alfabéticos'
                    },
                }
            },
            dni: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 10,
                    },
                    digits: {},
                    regexp: {
                        regexp: /^([0-9]|(\bEX[0-9]))+$/i,
                        message: 'El número de cedula debe empezar con números y para extranjeros con EX'
                    },
                    remote: {
                        message: 'El número de cedula ya se encuentra registrado',
                        url: pathname,
                        data: function (validator, $field, value) {
                            return {
                                obj: validator.getFieldElements('dni').val(),
                                id: validator.getFieldElements('id').val(),
                                type: 'dni',
                                action: 'repeated'
                            };
                        },
                        type: 'POST'
                    },
                    callback: {
                        message: 'Cedula invalida',
                        callback: function (value, validator, $field) {
                            return validate_dni_ruc(value);
                        }
                    }
                }
            },
            email: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 5
                    },
                    remote: {
                        message: 'El email ya se encuentra registrado',
                        url: pathname,
                        data: function (validator, $field, value) {
                            return {
                                obj: validator.getFieldElements('email').val(),
                                id: validator.getFieldElements('id').val(),
                                type: 'email',
                                action: 'repeated'
                            };
                        },
                        type: 'POST'
                    },
                    regexp: {
                        regexp: /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/i,
                        message: 'El email no es correcto'
                    }
                }
            },
            username: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 4
                    },
                    remote: {
                        message: 'El username ya se encuentra registrado',
                        url: pathname,
                        data: function (validator, $field, value) {
                            return {
                                obj: validator.getFieldElements('username').val(),
                                id: validator.getFieldElements('id').val(),
                                type: 'username',
                                action: 'repeated'
                            };
                        },
                        type: 'POST'
                    }
                }
            },
            phone: {
                validators: {
                    stringLength: {
                        min: 7,
                        max: 7
                    },
                    digits: {}
                }
            },
            mobile: {
                validators: {
                    stringLength: {
                        min: 10,
                    },
                    digits: {},
                    callback: {
                        message: 'El número de celular no es válido',
                        callback: function (value, validator, $field) {
                            return value === '' || $field.intlTelInput('isValidNumber');
                        }
                    },remote: {
                        message: 'El teléfono celular ya se encuentra registrado.',
                        url: pathname,
                        data: function (validator, $field, value) {
                            return {
                                obj: validator.getFieldElements('mobile').val(),
                                id: validator.getFieldElements('id').val(),
                                type: 'phone',
                                action: 'repeated'
                            };
                        },
                        type: 'POST'
                    },

                }
            },
            gender: {
                validators: {
                    notEmpty: {
                        message: 'Seleccione un género',
                    },
                }
            },
            'groups[]': {
                validators: {
                    notEmpty: {
                        message: 'Seleccione un perfil'
                    }
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
            birthdate: {
                validators: {
                    date: {
                        format: 'YYYY-MM-DD',
                        message: 'La fecha de nacimiento no es válida'
                    }
                }
            },
            image: {
                validators: {
                    file: {
                        extension: 'jpeg,jpg,png',
                        type: 'image/jpeg,image/png',
                        maxFiles: 1,
                        message: 'Introduce una imagen válida'
                    }
                }
            },
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
