$(function () {

    $('#id_name').keypress(function (e) {
        return validate_form_text('letters',e,null);
    });

    $('#frmForm').formValidation({
        message: 'El valor no es valido',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            name: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 4, max: 10
                    },
                    /*regexp: {
                        regexp: /^[A-ZáéíóúÁÉÍÓÚñÑ\s]+$/i,
                        message: 'Los nombres solo puede consistir en caracteres alfabéticos'
                    },*/
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
            icon: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 4, max: 10
                    },
                    /*regexp: {
                        regexp: /^[A-ZáéíóúÁÉÍÓÚñÑ\s]+$/i,
                        message: 'El icono solo puede consistir en caracteres alfabéticos'
                    },*/
                    remote: {
                       message: 'El icono ya se encuentra registrado',
                        url: pathname,
                        data: function (validator, $field, value) {
                            return {
                                obj: validator.getFieldElements('icon').val(),
                                id: validator.getFieldElements('id').val(),
                                type: 'icon',
                                action: 'repeated'
                            }
                        },
                        type: 'POST'
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