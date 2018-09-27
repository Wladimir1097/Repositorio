var tblSalary;
function generate_payroll() {
    tblSalary = $('#tblSalary').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: {
                action: 'generate_salaries',
                month: $('#id_month').val(),
                year: $('#id_year').val()
            },
            dataSrc: ""
        },
        columnDefs: [
             {
                targets: [6],
                class: 'text-center'
            },
            {
                targets: [4, 5,8],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [7],
                class: 'text-center',
                render: function (data, type, row) {
                    if (parseFloat(row[5]) === 0.00) {
                        return '$' + data;
                    }
                    return '<a rel="dscto" class="btn btn-xs btn-primary"><i class="fa fa-bars" aria-hidden="true"></i> Descuentos ' + data + '</a>'
                }
            }
        ]
    });
}

$(function () {

    $('#tblSalary tbody').on('click', 'a[rel="dscto"]', function () {
        $('.tooltip').remove();
        var td = $('#tblSalary').DataTable().cell($(this).closest('td, li')).index(),
            rows = tblSalary.row(td.row).data(), id = rows[0];
        $('#tblDscto').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {action: 'get_dscto_salary', id: id, month: $('#id_month').val(), year: $('#id_year').val()},
                dataSrc: ""
            },
            columnDefs: [
                {
                    targets: ['_all'],
                    class: 'text-center'
                },

            ]
        });
        $('#MyModalDscto').modal('show');
    });


    $("#id_year").datepicker({
        format: "yyyy",
        autoclose: true,
        minViewMode: "years",
        orientation: "down bottom"
    }).on('changeDate', function (e) {
        $('#frmForm').formValidation('revalidateField', 'year');
        $('#frmForm').formValidation('revalidateField', 'month');
        generate_payroll();
    });

    $('#id_month').change(function () {
        $('#frmForm').formValidation('revalidateField', 'month');
        $('#frmForm').formValidation('revalidateField', 'year');
        generate_payroll();
    });

    $('#reset').on('click', function () {
        var year = $('#id_year').val();
        $('#frmForm').formValidation('resetForm', true);
        $('#id_month').selectpicker('refresh').selectpicker('val', '');
        $('#id_year').val(year);
        tableSalary.clear().draw();
    });

    $('#frmForm').formValidation({
        message: 'This value is not valid',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            year: {
                validators: {
                    notEmpty: {},
                    digits: {},
                    remote: {
                        message: 'Ya se encuentra registrado este rol de sueldo con este año y mes',
                        url: pathname,
                        data: function (validator, $field, value) {
                            return {
                                id: validator.getFieldElements('id').val(),
                                month: validator.getFieldElements('month').val(),
                                year: validator.getFieldElements('year').val(),
                                action: 'repeated'
                            };
                        },
                        type: 'POST'
                    }
                }
            },
            month: {
                validators: {
                    notEmpty: {
                        message: 'Seleccione un mes'
                    },
                    remote: {
                        message: 'Ya se encuentra registrado este rol de sueldo con este año y mes',
                        url: pathname,
                        data: function (validator, $field, value) {
                            return {
                                id: validator.getFieldElements('id').val(),
                                month: validator.getFieldElements('month').val(),
                                year: validator.getFieldElements('year').val(),
                                action: 'repeated'
                            };
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
        })
        .on('success.field.fv', function (e, data) {
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
