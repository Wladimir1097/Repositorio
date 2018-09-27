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
                    return '<a rel="delete" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a>';
                }
            },
            {
                targets: [6],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                   return '<a href="'+data+'" target="_blank" class="btn btn-primary btn-xs btn-flat" data-toggle="tooltip" title="Descargar Respaldo"><i class="fa fa-database" aria-hidden="true"></i></a>';
                }
            }
        ],
    });
}

$(function () {
    load_data();

    $("#btn-new").click(function () {
        action_by_ajax_with_alert('Notificación','¿Desea usted crear un nuevo backup?',pathname,{action: 'new'},function () {
            location.reload();
        }, 'Respaldo de base de datos creado correctamente');
     });
});
