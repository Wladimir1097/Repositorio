function load_data() {
    table = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        order: [[0, 'desc'], [4, 'desc']],
        ajax: {
            url: pathname,
            type: 'POST',
            data: {action: 'load'},
            dataSrc: ""
        },
        columnDefs: [
            {
                targets: [-1],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '<a href="' + pathname + '?action=pdf&id=' + row[0] + '" target="_blank"  data-toggle="tooltip" title="Imprimir Orden" class="btn btn-warning btn-xs btn-flat"><i class="fa fa-file-pdf-o" aria-hidden="true"></i></a> ';
                    buttons += '<a rel="delete" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a> ';
                    buttons += '<a href="' + pathname + '?action=edit&id=' + row[0] + '" data-toggle="tooltip" title="Editar registro" class="btn btn-yahoo btn-xs btn-flat"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></a> ';
                    buttons += '<a href="' + pathname + '?action=reuse&id=' + row[0] + '" data-toggle="tooltip" title="Reusar registro" class="btn btn-adn btn-xs btn-flat"><i class="fa fa-recycle" aria-hidden="true"></i></a> ';
                    buttons += '<a rel="details" data-toggle="tooltip" title="Buscar Detalles" class="btn btn-success btn-xs btn-flat"><i class="fa fa-search" aria-hidden="true"></i></a> ';
                    if (data === 2) {
                        buttons += '<a rel="dispatch_products" data-toggle="tooltip" title="Entregar materiales" class="btn btn-dropbox btn-xs btn-flat"><i class="fa fa-check-circle-o" aria-hidden="true"></i></a>';
                    } else {
                        buttons += '<a rel="devolution" data-toggle="tooltip" title="Devolución" class="btn btn-instagram btn-xs btn-flat"><i class="fa fa-refresh" aria-hidden="true"></i></a> ';
                    }
                    buttons += '<a rel="agg" data-toggle="tooltip" title="Adicionar Medidores y Sellos" class="btn btn-foursquare  btn-xs btn-flat"><i class="fa fa-plus-square" aria-hidden="true"></i></a> ';

                    return buttons;
                }
            }, {
                targets: [5],
                class: 'text-center',
                render: function (data, type, row) {
                    return data + '  Materiales';
                }
            }, {
                targets: ['_all'],
                class: 'text-center'
            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + data;
                }
            },
        ],
    });
}

var tblDispatch;

$(function () {

    load_data();

    $('#data tbody').on('click', 'a[rel="dispatch_products"]', function () {
        $('.tooltip').remove();
        var td = $('#data').DataTable().cell($(this).closest('td, li')).index(),
            rows = table.row(td.row).data(), id = rows[0];
        $('#sales').val(id);
        tblDispatch = $('#tblDispatch').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {action: 'details', id: id, type: 'dispatch'},
                dataSrc: ""
            },
            columns: [
                {data: "id"},
                {data: "name"},
                {data: "cant"},
                {data: "cant_ent"},
                {data: "stock"},
                {data: "cant_dis"},
                {data: "state"},
            ],
            columnDefs: [
                {
                    targets: [2, 3, 4],
                    class: 'text-center',
                },
                {
                    targets: [5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.state) {
                            if (row.stock === 0) {
                                return 'Sin Stock';
                            }
                            return '<input type="text" class="form-control input-sm" name="cant_dis" value="0">';
                        }
                        return '<i class="fa fa-check" aria-hidden="true"></i>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!row.state) {
                            if (row.stock === 0) {
                                return 'Sin Stock';
                            }
                            return '<input type="checkbox" class="check" value="" name="chk_dispatch">';
                        }
                        return '<i class="fa fa-check" aria-hidden="true"></i>';

                    }
                },
            ],
            rowCallback: function (row, data, index) {
                row = $(row).closest('tr');
                row.find("input[name='cant_dis']").TouchSpin({
                    min: 1,
                    max: parseInt(data.cant),
                    step: 1
                });
            },
        });
        $('#btnDispatch').prop('disabled', true);
        $('#MyModalDispatch').modal('show');
    });

    function check_devolve() {
        var enable = tblDispatch.rows().data().filter(function (value, index) {
            return value.state === true;
        }).length === 0;
        $('#btnDispatch').prop('disabled', enable);
    }

    $('#tblDispatch tbody').on('change', 'input[name="cant_dis"]', function () {
        var td = tblDispatch.cell($(this).closest('td, li')).index(),
            row = tblDispatch.row(td.row).data();
        row.cant_dis = parseInt($(this).val());
    });

    $('#tblDispatch tbody').on('change', 'input[type="checkbox"]', function () {
        var td = tblDispatch.cell($(this).closest('td, li')).index(),
            row = tblDispatch.row(td.row).data();
        row.state = this.checked;

        if (this.checked) {
            tblDispatch.rows(td.row).nodes().to$().addClass('color-check');
        }
        else {
            tblDispatch.rows(td.row).nodes().to$().removeClass('color-check');
        }
        check_devolve();
    });

    $('#btnDispatch').on('click', function () {
        console.log(JSON.stringify(tblDispatch.data().toArray()));
        action_by_ajax_with_alert('Notificación', '¿Esta seguro de devolver los siguientes Materiales?',
            pathname, {
                items: JSON.stringify(tblDispatch.data().toArray()),
                action: 'dispatch_products',
                sales: $('#sales').val()
            },
            function () {
                tblDispatch.ajax.reload(null, false);
                table.ajax.reload(null, false);
            },
            'Se han devueltos con exito los Materiales'
        );

    });

    $('#MyModalDispatch').on('hidden.bs.modal', function () {
        table.ajax.reload(null, false);
    });


    /*=====================================================================================*/

    $('#data tbody').on('click', 'a[rel="details"]', function () {
        $('.tooltip').remove();
        var td = $('#data').DataTable().cell($(this).closest('td, li')).index(),
            rows = table.row(td.row).data(), id = rows[0];
        $('.nav-tabs a[href="#tab7"]').tab('show');
        $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {action: 'details', id: id, type: 'products'},
                dataSrc: ""
            },
            columnDefs: [
                {
                    targets: [2, 4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [3],
                    class: 'text-center',
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data) {
                            return '<i class="fa fa-check" aria-hidden="true"></i>';
                        }
                        return '<i class="fa fa-times" aria-hidden="true"></i>';
                    }
                },
            ]
        });
        $('#tblServices').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {action: 'details', id: id, type: 'services'},
                dataSrc: ""
            },
            columnDefs: [
                {
                    targets: [2],
                    orderable: false,
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ]
        });
        $('#tblMedidor').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {action: 'details', id: id, type: 'medidor'},
                dataSrc: "",
                columns: [
                    {data: "id"},
                    {data: "numeracion"},
                ],
            },
            columnDefs: [
                {
                    targets: [1],
                    orderable: false,
                    class: 'text-center'
                },
                {
                    targets: [-1],
                    orderable: false,
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a href="' + pathname + '?action=delete&num=' + row[1] + '" data-toggle="tooltip"  title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a>';
                    }
                }
            ]
        });
        $('#tblSello').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {action: 'details', id: id, type: 'sello'},
                dataSrc: "",
                columns: [
                    {data: "id"},
                    {data: "numeracion"},
                ],
            },
            columnDefs: [
                {
                    targets: [1],
                    orderable: false,
                    class: 'text-center'
                },
                {
                    targets: [-1],
                    orderable: false,
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a href="' + pathname + '?action=delete&num=' + row[1] + '" data-toggle="tooltip"  title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a>';
                    }
                }
            ]
        });
        $('#MyModalVent').modal('show');
    });
});


