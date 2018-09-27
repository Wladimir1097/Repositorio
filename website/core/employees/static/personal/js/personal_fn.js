$(function () {

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
                        min: 4
                    },
                    remote: {
                        message: 'El nombre ya se encuentra registrado',
                        url: pathname,
                        data: function (validator, $field, value) {
                            return {
                                obj: validator.getFieldElements('name').val(),
                                id: validator.getFieldElements('id').val(),
                                type: 'name',
                                action: 'repeated'
                            }
                        },
                        type: 'POST'
                    }
                }
            },
            ruc: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 10,
                    },
                    digits: {},
                    remote: {
                        message: 'El ruc ya se encuentra registrado',
                        url: pathname,
                        data: function (validator, $field, value) {
                            return {
                                obj: validator.getFieldElements('ruc').val(),
                                id: validator.getFieldElements('id').val(),
                                type: 'ruc',
                                action: 'repeated'
                            };
                        },
                        type: 'POST'
                    },
                    callback: {
                        message: 'Ruc o Cedula invalida',
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
            mobile: {
                validators: {
                    stringLength: {
                        min: 10,
                    },
                    digits: {},
                    callback: {
                        message: 'El teléfono no es válido',
                        callback: function (value, validator, $field) {
                            return value === '' || $field.intlTelInput('isValidNumber');
                        }
                    },
                    remote: {
                        message: 'El teléfono celular ya se encuentra registrado',
                        url: pathname,
                        data: function (validator, $field, value) {
                            return {
                                obj: validator.getFieldElements('mobile').val(),
                                id: validator.getFieldElements('id').val(),
                                type: 'mobile',
                                action: 'repeated'
                            };
                        },
                        type: 'POST'
                    },
                }
            },
            address: {
                validators: {
                    stringLength: {
                        min: 4,
                    }
                }
            },
            avatar: {
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
            save_registry_by_submit(e, message, function () {
                location.href = pathname;
            });
        });
});
