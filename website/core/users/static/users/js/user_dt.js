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
                    var buttons = '<a href="'+pathname+'?action=edit&id='+row[7]+'" data-toggle="tooltip" title="Editar registro" class="btn btn-warning btn-xs btn-flat"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></a> ';
                    buttons+='<a rel="delete" data-toggle="tooltip" title="Eliminar registro" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a> ';
                    buttons+='<a rel="access_users" class="btn bg-navy btn-xs btn-flat"  data-toggle="tooltip" title="Accesos"><i class="fa fa-user-secret" aria-hidden="true"></i></a> ';
                    buttons+='<a rel="login" class="btn btn-dropbox btn-xs btn-flat" data-toggle="tooltip" title="Loguearse"><i class="fa fa-globe" aria-hidden="true"></i></a> ';
                    buttons+='<a rel="reset_password" class="btn btn-tumblr btn-xs btn-flat" data-toggle="tooltip" title="Resetear clave"><i class="fa fa-unlock-alt" aria-hidden="true"></i></a> ';
                    buttons+='<a rel="profile" class="btn btn-success btn-xs btn-flat" data-toggle="tooltip" title="Grupos"><i class="fa fa-users" aria-hidden="true"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [5],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                    if (data){
                        return '<i class="fa fa-check" aria-hidden="true"></i>';
                    }
                    return '<i class="fa fa-times" aria-hidden="true"></i>';
                }
            },
            {
                targets: [6],
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

    $('#data tbody').on('click', 'a[rel]', function () {
        var td = table.cell($(this).closest('td, li')).index(),
            row = table.row(td.row).data(),
            rel = $(this).attr('rel'),
            id = row[0];
        var content = "";
        switch (rel) {
            case 'reset_password':
                action_by_ajax_with_alert('Notificación',
                    '¿Estas seguro de resetear la clave por el dni?',
                    pathname, {id: id, action: rel},
                    function () {
                        table.ajax.reload();
                    },
                    'Cambio de clave exitoso'
                    );
                break;
            case 'login':
                action_by_ajax_with_alert('Notificación',
                    '¿Estas seguro de entrar al sistema con el siguiente usuario?',
                    pathname, {id: id, action: rel},
                    function () {
                        location.href = '/dashboard/';
                    },
                    'Ingreso al sistema correcto, ahora el sistema se reseteara'
                    );
                break;
            case 'access_users':
                $('#tblAccessUsers').DataTable({
                    destroy: true,
                    responsive: true,
                    autoWidth: false,
                    ajax: {
                        url: pathname,
                        type: 'POST',
                        data: {id: id, action: rel},
                        dataSrc: ""
                    },
                    columnDefs: [
                        {orderable: false, targets: ['_all']}
                    ]
                });
                $('#MyModalAccessUsers').modal('show');
                break;
            case 'profile':
                $('#tblProfiles').DataTable({
                    destroy: true,
                    responsive: true,
                    autoWidth: false,
                    ajax: {
                        url: pathname,
                        type: 'POST',
                        data: {id: id, action: 'get_profiles'},
                        dataSrc: ""
                    },
                });
                $('#MyModalProfile').modal('show');
                break;
        }
    });
});
