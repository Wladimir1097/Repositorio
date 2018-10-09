function load_data() {
    table = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
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
                    if (!row[8]) {
                        var buttons = '<a href="' + pathname + '?action=edit&id=' + row[0] + '" data-toggle="tooltip" title="Editar registro" class="btn btn-warning btn-xs btn-flat"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></a> ';
                    } else {
                        var buttons = '<a href="' + pathname + '?action=pdf&id=' + row[0] + '" target="_blank"  data-toggle="tooltip" title="Imprimir Orden" class="btn btn-warning btn-xs btn-flat"><i class="fa fa-file-pdf-o" aria-hidden="true"></i></a> ';
                    }
                    buttons += '<a rel="details" data-toggle="tooltip" title="Buscar Inventario" class="btn btn-success btn-xs btn-flat"><i class="fa fa-search" aria-hidden="true"></i></a> ';
                    buttons += '<a rel="delete" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a>';
                    buttons += '<a rel="distribucion" data-toggle="tooltip" title="Distribucion" class="btn btn-instagram btn-xs btn-flat"><i class="fa fa-refresh" aria-hidden="true"></i></a> ';
                    return buttons;
                }
            },
            {
                targets: [5],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + data;
                }
            },
            {
                targets: [3],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    return data + '  Materiales';
                }
            }
        ],
    });
}

$(function () {
    load_data();

    $('#data tbody').on('click', 'a[rel="details"]', function () {
        $('.tooltip').remove();
        var td = $('#data').DataTable().cell($(this).closest('td, li')).index(),
            rows = table.row(td.row).data(),
            id = rows[0];
        $('#tblCompDetails').DataTable({
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
                    targets: [3],
                    class: 'text-center'
                },
                {
                    targets: [2, 4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data;
                    }
                }
            ]
        });
        $('#MyModalInventory').modal('show');
    });
});
