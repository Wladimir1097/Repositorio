function load_data() {
    table = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
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
                    var buttons = '<a href="'+pathname+'?action=edit&id='+row[0]+'" data-toggle="tooltip" title="Editar registro" class="btn btn-warning btn-xs btn-flat"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></a> ';
                    buttons+='<a rel="delete" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [1],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    return '<img src="'+data+'" style="width: 25px; height: 25px;">'
                }
            },
        ],
    });
}

$(function () {
    load_data();
});
