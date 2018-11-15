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
                    if (!row[8]) {
                        var buttons = '<a href="' + pathname + '?action=edit&id=' + row[0] + '" data-toggle="tooltip" title="Editar registro" class="btn btn-yahoo btn-xs btn-flat"><i class="fa fa-pencil-square-o" aria-hidden="true"></i></a> ';
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
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + data;
                }
            },
            {
                targets: [3],
                class: 'text-center',
                render: function (data, type, row) {
                    return data + '  Materiales';
                }
            }
        ],
    });
}
var now = new Date();
    var jsDate = now.getDate() + '-' + (now.getMonth() + 1) + '-' + now.getFullYear();

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
            ],
            dom: 'Blfrtip',
            buttons: [
                {
                    extend: 'excelHtml5',
                    text: 'Descargar Excel <i class="fa fa-file-excel-o"></i>',
                    titleAttr: 'Excel',
                    className: 'btn btn-primary btn-flat btn-sm'
                },
                {
                    extend: 'pdfHtml5',
                    text: 'Descargar Pdf <i class="fa fa-file-pdf-o"></i>',
                    titleAttr: 'PDF',
                    className: 'btn btn-primary btn-flat btn-sm',
                    title: '',
                    orientation: 'portrait',
                    pageSize: 'A4',
                    download: 'open',
                    customize: function (doc) {
                        doc.styles = {
                            header: {
                                fontSize: 18,
                                bold: true,
                                alignment: 'center'
                            },
                            subheader: {
                                fontSize: 13,
                                bold: true
                            },
                            quote: {
                                italics: true
                            },
                            small: {
                                fontSize: 8
                            },
                            tableHeader: {
                                bold: true,
                                fontSize: 11,
                                color: 'white',
                                fillColor: '#2d4154',
                                alignment: 'center'
                            },
                            tableBodyOdd: {
                                fontSize: 10,
                                alignment: 'center'
                            },
                            tableBodyEven: {
                                fontSize: 10,
                                alignment: 'center'
                            }
                        };
                        doc.content.splice(0, 0, {
                            margin: [0, 0, 0, 12],
                            alignment: 'center',
                            fit: [125, 125],
                            image: icon_base64
                        });
                        doc.content.splice(1, 0, {
                            text: '',
                            style: 'header',
                        });
                        doc.content.splice(2, 0, {
                            alignment: 'right',
                            text: '' + jsDate,
                            style: 'subheader'
                        });
                        doc.content.splice(3, 0, {
                            alignment: 'center',
                            text: ('Reporte de Ingreso General').toUpperCase(),
                            style: 'subheader'
                        });
                        doc.content[4].table.widths = ['5%', '40%', '20%', '10%', '20%'];
                        doc.content[4].margin = [25, 35, 0, 0];
                        doc.content[4].layout = {};
                        doc['footer'] = (function (page, pages) {
                            return {
                                columns: [
                                    {
                                        alignment: 'left',
                                        text: ['Fecha de creación: ', {text: jsDate.toString()}]
                                    },
                                    {
                                        alignment: 'right',
                                        text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                    }
                                ],
                                margin: 20
                            }
                        });
                    }
                }
            ]
        });
        $('#MyModalInventory').modal('show');
    });
});
