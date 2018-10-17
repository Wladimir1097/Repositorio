$(function () {

    $('#id_cost').TouchSpin({
        min: 0.01,
        max: 1000000,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        prefix: '$'
    }).on('change touchspin.on.min touchspin.on.max', function () {
        $('#id_price').trigger("touchspin.updatesettings", { min: parseFloat($(this).val()) } );
        $('#frmForm').formValidation('revalidateField', 'cost');
    });

    $('#id_price').TouchSpin({
        min: 0.01,
        max: 1000000,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        prefix: '$'
    }).on('change touchspin.on.min touchspin.on.max', function () {
         $('#frmForm').formValidation('revalidateField', 'price');
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
            price: {
                validators: {
                    notEmpty: {},
                    numeric: {decimalSeparator: '.'}
                }
            },
            cat: {
                validators: {
                    notEmpty: {
                        message: 'Selecciona una categoria'
                    },
                }
            },
            brand: {
                validators: {
                    notEmpty: {
                        message: 'Selecciona una marca'
                    },
                }
            },
            image: {
                validators: {
                    file: {
                        extension: 'jpeg,jpg,png',
                        type: 'image/jpeg,image/png',
                        maxFiles: 1,
                        message: 'Introduzca una imagen válida'
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
