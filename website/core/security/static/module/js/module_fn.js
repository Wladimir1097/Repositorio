$(function () {

    $('input[name="dropdown"]').on('change', function () {
        var combobox = $('#id_type');
        combobox.prop('disabled', !this.checked);
        if (!this.checked) {
            combobox.selectpicker('val', '');
        }
        combobox.selectpicker('refresh');
    });

    $('#frmForm').formValidation({
        message: 'El valor no es valido',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            url: {
                validators: {
                    notEmpty: {},
                    stringLength: {min: 4},
                    remote: {
                        message: 'URL ya registrada',
                        url: pathname,
                        data: function (validator, $field, value) {
                            return {
                                obj: validator.getFieldElements('url').val(),
                                id: validator.getFieldElements('id').val(),
                                type: 'url',
                                action: 'repeated'
                            }
                        },
                        type: 'POST'
                    }
                }
            },
            name: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 4
                    },
                }
            },
            icon: {
                validators: {
                }
            },
            description: {
                validators: {}
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
            type: {
                validators: {

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