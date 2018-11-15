var tblAdicion;

$(function () {

    $('#data tbody').on('click', 'a[rel="agg"]', function () {
        $('.tooltip').remove();
        var td = $('#data').DataTable().cell($(this).closest('td, li')).index(),
            rows = table.row(td.row).data(), id = rows[0];
        $('.nav-tabs a[href="#tab_1"]').tab('show');
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
                {data: "pk"},
                {data: "id"},
                {data: "tipo"},
                {data: "num"},
                {data: "state"},
            ],
            columnDefs: [

                {visible: false, targets: [0]},
                {
                    targets: [2],
                    class: 'text-center',
                    'render': function (data, type, row) {
                        if (row.tipo) {
                            return '<span class="badge bg-green-active">' + 'Medidor' + '</span>';
                        }
                        return '<span class="badge bg-yellow-active">' + 'Sello' + '</span>';
                    }
                },
                {
                    targets: [3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge bg-light-blue-active">' + row.num + '</span>';
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
            ]
        });
        $('#btnAdicion').prop('disabled', true);
        $('#MyModalAdicion').modal('show');
    });

    function check_devolve() {
        var enable = tblAdicion.rows().data().filter(function (value, index) {
            return value.state === true;
        }).length === 0;
        $('#btnAdicion').prop('disabled', enable);
    }

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
        action_by_ajax_with_alert('Notificación', '¿Esta seguro de ingresar estas numeraciones?',
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

    $('#btnmedidor').on('click', function () {
        var num1 = parseInt($('#uno').val());
        var num2 = parseInt($('#dos').val());
        if (num2 > num1) {
            action_by_ajax_with_alert('Notificación', '¿Esta seguro de ingresar estas numeraciones?',
                pathname, {
                    items: JSON.stringify(tblAdicion.data().toArray()),
                    num1: num1,
                    num2: num2,
                    action: 'ingress_med'
                },
                function () {
                    $('#uno').val("");
                    $('#dos').val("");
                },
                'Se ha realizado con exito el ingreso'
            );
        } else {
            error_message('error en el rango');
        }


    });

    $('#btnsello').on('click', function () {
        var num1 =parseInt($('#tres').val());
        var num2 = parseInt($('#cuatro').val());
        if (num2 > num1) {
            action_by_ajax_with_alert('Notificación', '¿Esta seguro de ingresar estas numeraciones?',
                pathname, {
                    items: JSON.stringify(tblAdicion.data().toArray()),
                    num1: num1,
                    num2: num2,
                    action: 'ingress_sell'
                },
                function () {
                    $('#tres').val("");
                    $('#cuatro').val("");
                },
                'Se ha realizado con exito el ingreso'
            );
        } else {
            error_message('error en el rango');
        }


    });
});
