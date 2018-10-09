var tblAdicion;

$(function () {

    $('#data tbody').on('click', 'a[rel="agg"]', function () {
        $('.tooltip').remove();
        var td = $('#data').DataTable().cell($(this).closest('td, li')).index(),
            rows = table.row(td.row).data(), id = rows[0];
        tblAdicion = $('#tblAdicion').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {action: 'details', id: id, type: 'adicion'},
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
                    class: 'text-center',
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
                            return '<input type="text" class="form-control input-sm" name="cant_dev" value="0">';
                        }
                        return '<span class="badge bg-light-blue-active">' + row.cant_dev + '</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.state) {
                            return '<input type="checkbox" class="check" value="" name="chk_dispatch">';
                        }
                        return '<i class="fa fa-check" aria-hidden="true"></i>';

                    }
                },
            ],
            rowCallback: function (row, data, index) {
                row = $(row).closest('tr');
                row.find("input[name='cant_dev']").TouchSpin({
                    min: 1,
                    max:99999999999,
                    step: 1
                });
                row.find('input[name="cant_dev"]').keypress(function (e) {
                    return validate_form_text('numbers', e, null);
                });
            },
        });
        $('#btnAdicion').prop('disabled',true);
        $('#MyModalAdicion').modal('show');
    });

    function check_devolve() {
        var enable = tblAdicion.rows().data().filter(function (value, index) {
            return value.state === true;
        }).length === 0;
        $('#btnAdicion').prop('disabled', enable);
    }

    $('#tblAdicion tbody').on('change', 'input[name="cant_dev"]', function () {
        var td = tblAdicion.cell($(this).closest('td, li')).index(),
            row = tblAdicion.row(td.row).data();
        row.cant_dev = parseInt($(this).val());
    });

    $('#tblAdicion tbody').on('change', 'input[type="checkbox"]', function () {
        var td = tblAdicion.cell($(this).closest('td, li')).index(),
            row = tblAdicion.row(td.row).data();
        row.state = this.checked;

        if (this.checked) {
            tblAdicion.rows(td.row).nodes().to$().addClass('color-check');
        }
        else {
            tblAdicion.rows(td.row).nodes().to$().removeClass('color-check');
        }
        check_devolve();
    });

    $('#btnAdicion').on('click', function () {
        console.log(JSON.stringify(tblAdicion.data().toArray()));
        action_by_ajax_with_alert('Notificación','¿Esta seguro de ingresar estas numeraciones?',
            pathname, {
                items: JSON.stringify(tblAdicion.data().toArray()),
                action: 'ingress_prod'
            },
            function () {
                tblAdicion.ajax.reload(null, false);
                table.ajax.reload(null, false);
            },
            'Se ha realizado con exito el ingreso'
        );

    });

    $('#MyModalAdicion').on('hidden.bs.modal', function () {
        table.ajax.reload(null, false);
    });
});
