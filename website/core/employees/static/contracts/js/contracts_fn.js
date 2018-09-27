$(function () {
    $('#id_start_date').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        orientation: 'bottom bottom',
    }).on('changeDate', function (e) {
        $('#frmForm').formValidation('revalidateField', 'start_date');
    });

    $('#id_end_date').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        orientation: 'bottom bottom',
    }).on('changeDate', function (e) {
        $('#frmForm').formValidation('revalidateField', 'end_date');
    });

    $('#id_rmu').TouchSpin({
        min: 0.01,
        max: 1000000,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        prefix: '$'
    }).on('change touchspin.on.min touchspin.on.max', function () {
        $('#frmForm').formValidation('revalidateField', 'rmu');
    });

    $('#frmForm').formValidation({
        message: 'El valor no es valido',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            start_date: {
                validators: {
                    notEmpty: {
                        message: 'La fecha de inicio es obligatoria'
                    },
                    date: {
                        format: 'YYYY-MM-DD',
                        max: 'end_date',
                        message: 'La fecha de inicio no es válida'
                    }
                }
            },
            end_date: {
                validators: {
                    notEmpty: {
                        message: 'La fecha de finalización es obligatoria'
                    },
                    date: {
                        format: 'YYYY-MM-DD',
                        min: 'start_date',
                        message: 'La fecha de finalización no es válida'
                    }
                }
            },
            pers: {
                validators: {
                    notEmpty: {
                        message: 'Selecciona un empleado'
                    }
                }
            },
            rmu: {
                validators: {
                    notEmpty: {},
                    numeric: {decimalSeparator: '.'}
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
        .on('success.field.fv', function (e, data) {
            if (data.field === 'start_date' && !data.fv.isValidField('end_date')) {
                // We need to revalidate the end date
                data.fv.revalidateField('end_date');
            }

            if (data.field === 'end_date' && !data.fv.isValidField('start_date')) {
                // We need to revalidate the start date
                data.fv.revalidateField('start_date');
            }

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
