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
                    var buttons = '<a rel="details" data-toggle="tooltip" title="Buscar Inventario" class="btn btn-success btn-xs btn-flat"><i class="fa fa-search" aria-hidden="true"></i></a> ';
                    buttons+='<a rel="delete" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [4,5,6],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    return '$'+data;
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
                data: {action: 'details', id: id},
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
