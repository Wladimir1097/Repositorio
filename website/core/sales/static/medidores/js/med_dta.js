function load_data() {
    table = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        order: [[0, 'desc'], [1, 'desc']],
        deferRender: true,
        ajax: {
            url: pathname,
            type: 'POST',
            data: {action: 'load'},
            dataSrc: ""
        },
        columnDefs: [
            {
                targets: [2],
                class: 'text-center',
                'render': function (data, type, row) {
                    return '<span class="badge bg-green-active">' + data + '</span>';
                }
            },
            {
                targets: [3],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<span class="badge bg-light-blue-active">' + data + '</span>';
                }
            },
            {

                targets: [-1],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    var buttons = '<a rel="delete" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a> ';
                    buttons += '<a rel="details" data-toggle="tooltip" title="Buscar Detalles" class="btn btn-success btn-xs btn-flat"><i class="fa fa-search" aria-hidden="true"></i></a> ';
                    return buttons;
                }
            }
        ],
    });
}

$(function () {
    load_data();

    /*=====================================================================================*/

    $('#data tbody').on('click', 'a[rel="details"]', function () {
        $('.tooltip').remove();
        var td = $('#data').DataTable().cell($(this).closest('td, li')).index(),
            rows = table.row(td.row).data(), id = rows[0];
        $('.nav-tabs a[href="#tab_1"]').tab('show');
        $('#tblMedidor').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {action: 'details', id: id, type: 'medidor'},
                dataSrc: ""
            },
            columnDefs: [
                {
                    targets: '_all',
                    class: 'text-center',
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row[3]) {
                            return 'ProEnergy';
                        }
                        return 'Wagner';
                    }
                },
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
                dataSrc: ""
            },
            columnDefs: [
                {
                    targets: '_all',
                    class: 'text-center',
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row[2]) {
                            return 'ProEnergy';
                        }
                        return 'Wagner';
                    }
                },
            ]
        });
        $('#MyModal').modal('show');
    });
});
