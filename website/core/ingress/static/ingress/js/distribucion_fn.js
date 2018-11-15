var tblDistr;
$(function () {

    $('#data tbody').on('click', 'a[rel="distribucion"]', function () {
        $('.tooltip').remove();
        var td = $('#data').DataTable().cell($(this).closest('td, li')).index(),
            rows = table.row(td.row).data(), id = rows[0];
        tblDistr = $('#tblDistr').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {action: 'details', id: id, type: 'distribucion'},
                dataSrc: ""
            },
            columns: [
                {data: "id"},
                {data: "name"},
                {data: "cant"},
                {data: "cant_dev"},
                {data: "state"},
            ],
            columnDefs: [
                {
                    targets: [1],
                    class: 'text-center'
                },
                {
                    targets: [2],
                    class: 'text-center',
                    'render': function (data, type, row) {
                        return '<span class="badge bg-green-active">' + row.cant + '</span>';
                    }
                },
                {
                    targets: [3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.state) {
                            if (row.cant === 0) {
                                return 'Distribuido';
                            }
                            return '<input type="text" class="form-control input-sm" name="cant_dev" value="0">';
                        }
                        real = parseInt(row.c) - parseInt(row.cant);
                        return '<span class="badge bg-light-blue-active">' + real + '</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.state) {
                            if (row.cant === 0) {
                                return 'Distribuido';
                            }
                            return '<input type="checkbox" class="check" value="" name="chk_dispatch">';
                        }
                        return '<i class="fa fa-check" aria-hidden="true"></i>';

                    }
                },
            ],
            rowCallback: function (row, data, index) {
                row = $(row).closest('tr');
                row.find("input[name='cant_dev']").TouchSpin({
                    min: 0,
                    max: parseInt(data.cant),
                    step: 1
                });

                row.find('input[name="cant_dev"]').keypress(function (e) {
                    return validate_form_text('numbers', e, null);
                });
            },
        });
        $('#btnDistr').prop('disabled', true);
        $('#MyModalDistr').modal('show');
    });

    $('input[name="cant_dev"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    function check_devolve() {
        var enable = tblDistr.rows().data().filter(function (value, index) {
            return value.state === true;
        }).length === 0;
        $('#btnDistr').prop('disabled', enable);
    }

    $('#tblDistr tbody').on('change', 'input[name="cant_dev"]', function () {
        var td = tblDistr.cell($(this).closest('td, li')).index(),
            row = tblDistr.row(td.row).data();
        row.cant_dev = parseInt($(this).val());
    });

    $('#tblDistr tbody').on('change', 'input[type="checkbox"]', function () {
        var td = tblDistr.cell($(this).closest('td, li')).index(),
            row = tblDistr.row(td.row).data();
        row.state = this.checked;

        if (this.checked) {
            tblDistr.rows(td.row).nodes().to$().addClass('color-check');
        }
        else {
            tblDistr.rows(td.row).nodes().to$().removeClass('color-check');
        }
        check_devolve();
    });

    $('#btnDistr').on('click', function () {
        $('#btnDistr').prop('disabled', true);
        console.log(JSON.stringify(tblDistr.data().toArray()));
        action_by_ajax_with_alert('Notificación', '¿Esta seguro de aplicar la distribucion a estos materiales?',
            pathname, {
                items: JSON.stringify(tblDistr.data().toArray()),
                action: 'distr_products'
            },
            function () {
                tblDistr.ajax.reload(null, false);
                table.ajax.reload(null, false);
            },
            'Se ha realizado con exito la distribucion'
        );

    });

    $('#MyModalDistr').on('hidden.bs.modal', function () {
        table.ajax.reload(null, false);
    });
});
