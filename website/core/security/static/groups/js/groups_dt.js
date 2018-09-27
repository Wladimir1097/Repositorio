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
                    var buttons = '<a href="'+pathname+'?action=edit&id='+row[0]+'" data-toggle="tooltip" title="Editar registro" class="btn btn-warning btn-xs btn-flat"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></a> ';
                    buttons+='<a rel="delete" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a> ';
                    buttons+='<a rel="load_modules" data-toggle="tooltip" title="Consultar modulos" class="btn bg-blue btn-xs btn-flat"><i class="fa fa-search" aria-hidden="true"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [2],
                class: 'text-center',
                render: function (data, type, row) {
                    return '<span class="badge">'+data+'</span>'
                }
            },
        ],
    });
}

$(function () {

    load_data();

    $('#data tbody').on('click', 'a[rel="load_modules"]', function () {
        $('.tooltip').remove();
        var td = $('#data').DataTable().cell($(this).closest('td, li')).index(),
            rows = table.row(td.row).data(), id=rows[0];
        $('#tblModules').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {action: 'load_modules', id: id},
                dataSrc: ""
            },
            columnDefs: [
                {
                    targets: [2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="'+row[2]+'" width="20px" height="20px">';
                    }
                },
                {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<i class="'+row[1]+'" aria-hidden="true"></i>';
                    }
                },
                {
                    targets: [4,5,6],
                    class: 'text-center',
                    orderable: false,
                    data: null,
                    render: function (data, type, row) {
                        if(row){
                            return '<i class="fa fa-check" aria-hidden="true"></i>';
                        }
                        return '<i class="fa fa-times" aria-hidden="true"></i>';
                    }
                },

            ]
        });
        $('#MyModalModules').modal('show');
    });

});
