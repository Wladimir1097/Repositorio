$(function () {

    $('#id_name').keypress(function (e) {
        return validate_form_text('letters',e,null);
    });

    $('#id_code').keypress(function (e) {
        return validate_form_text('letters_numbers_spaceless',e,null);
    }).keyup(function () {
        var value = $(this).val();
        $(this).val(value.toUpperCase());
    });

    $('#id_guarantee').TouchSpin({
        min: 0,
        max: 100,
        stepinterval: 1,
        maxboostedstep: 100,
        prefix: 'Años'
    }).on('change touchspin.on.min touchspin.on.max', function () {
        $('#frmForm').formValidation('revalidateField', 'guarantee');
    }).keypress(function (e) {
        return validate_form_text('numbers',e,null);
    });

    $('#id_cost').TouchSpin({
        min: 0.00,
        max: 1000000,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        prefix: '$'
    }).on('change touchspin.on.min touchspin.on.max', function () {
        $('#frmForm').formValidation('revalidateField', 'cost');
    }).keypress(function (e) {
         return validate_decimals($(this),e);
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
                        min: 4
                    }
                }
            },
            cost: {
                validators: {
                    notEmpty: {},
                    numeric: {decimalSeparator: '.'}
                }
            },
            code: {
                validators: {
                    notEmpty: {},
                    stringLength: {
                        min: 12
                    },
                    remote: {
                        message: 'La serie ya se encuentra registrada',
                        url: pathname,
                        data: function (validator, $field, value) {
                            return {
                                obj: validator.getFieldElements('code').val(),
                                id: validator.getFieldElements('id').val(),
                                type: 'code',
                                action: 'repeated'
                            }
                        },
                        type: 'POST'
                    }
                }
            },
            guarantee: {
                validators: {
                    notEmpty: {},
                    digits: {}
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
