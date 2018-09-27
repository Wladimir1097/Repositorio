var tblDevolution;

$(function () {

    $('#data tbody').on('click', 'a[rel="devolution"]', function () {
        $('.tooltip').remove();
        var td = $('#data').DataTable().cell($(this).closest('td, li')).index(),
            rows = table.row(td.row).data(), id = rows[0];
        tblDevolution = $('#tblDevolution').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {action: 'details', id: id, type: 'devolution'},
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
                    targets: [1,2],
                    class: 'text-center',
                },
                {
                    targets: [3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.state) {
                            if(row.cant === 0){
                                return 'Ya se devolvio todo';
                            }
                            return '<input type="text" class="form-control input-sm" name="cant_dev" value="0">';
                        }
                        return '<i class="fa fa-check" aria-hidden="true"></i>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.state) {
                            if(row.cant === 0){
                                return 'Ya se devolvio todo';
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
                    min: 1,
                    max: parseInt(data.cant),
                    step: 1
                });
            },
        });
        $('#btnDevolution').prop('disabled',true);
        $('#MyModalDevolution').modal('show');
    });

    function check_devolve() {
        var enable = tblDevolution.rows().data().filter(function (value, index) {
            return value.state === true;
        }).length === 0;
        $('#btnDevolution').prop('disabled', enable);
    }

    $('#tblDevolution tbody').on('change', 'input[name="cant_dev"]', function () {
        var td = tblDevolution.cell($(this).closest('td, li')).index(),
            row = tblDevolution.row(td.row).data();
        row.cant_dev = parseInt($(this).val());
    });

    $('#tblDevolution tbody').on('change', 'input[type="checkbox"]', function () {
        var td = tblDevolution.cell($(this).closest('td, li')).index(),
            row = tblDevolution.row(td.row).data();
        row.state = this.checked;

        if (this.checked) {
            tblDevolution.rows(td.row).nodes().to$().addClass('color-check');
        }
        else {
            tblDevolution.rows(td.row).nodes().to$().removeClass('color-check');
        }
        check_devolve();
    });

    $('#btnDevolution').on('click', function () {
        console.log(JSON.stringify(tblDevolution.data().toArray()));
        action_by_ajax_with_alert('Notificación','¿Esta seguro de aplicar la devolución a estos productos?',
            pathname, {
                items: JSON.stringify(tblDevolution.data().toArray()),
                action: 'devolution_products'
            },
            function () {
                tblDevolution.ajax.reload(null, false);
                table.ajax.reload(null, false);
            },
            'Se ha realizado con exito la devolución'
        );

    });

    $('#MyModalDevolution').on('hidden.bs.modal', function () {
        table.ajax.reload(null, false);
    });
});
