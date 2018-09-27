$(function () {

    $('#id_date_joined').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        orientation: 'bottom bottom',
        language: 'es'
    }).on('changeDate', function (e) {
        $('#frmForm').formValidation('revalidateField', 'date_joined');
    });

    $('#id_cost').TouchSpin({
        min: 0.01,
        max: 1000000,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        prefix: '$'
    }).on('change touchspin.on.min touchspin.on.max', function () {
        $('#frmForm').formValidation('revalidateField', 'cost');
    });

    $('#frmForm').formValidation({
        message: 'El valor no es valido',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            details: {
                validators: {
                    stringLength: {
                        min: 4
                    }
                }
            },
            date_joined: {
                validators: {
                    date: {
                        format: 'YYYY-MM-DD',
                        message: 'La fecha de nacimiento no es válida'
                    }
                }
            },
            cost: {
                validators: {
                    notEmpty: {},
                    numeric: {decimalSeparator: '.'}
                }
            },
            type: {
                validators: {
                    notEmpty: {
                        message: 'Selecciona un tipo de gasto'
                    }
                }
            },
            cont: {
                validators: {
                    notEmpty: {
                        message: 'Selecciona un cargo'
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