var tblReport;

function generate_report() {
    var data = {
        prod: $('#products').val()
    };

    var $report_text = "";

    var now = new Date();
    var jsDate = now.getDate() + '-' + (now.getMonth() + 1) + '-' + now.getFullYear();

    tblReport = $('#data').DataTable({
        destroy: true,
        responsive: true,
        autoWidth: false,
        ajax: {
            url: pathname,
            type: 'POST',
            data: data,
            dataSrc: ""
        },
        columnDefs: [
            {
                targets: [2],
                orderable: false,
                class: 'text-center',
                render: function (data, type, row) {
                   if(data !== '-------'){
                       return '$'+data;
                   }
                   return data;
                }
            },
            {
                targets: [3],
                class: 'text-center',
                render: function (data, type, row) {
                   return '<span class="badge">'+data+'</span>';
                }
            },
            {
                targets: [4],
                class: 'text-center'
            },
            {
                targets: [5,6],
                class: 'text-center'
            }
        ],
        dom: 'Bfrtip',
        buttons: [
            {
                extend:    'excelHtml5',
                text:      'Descargar Excel <i class="fa fa-file-excel-o"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-sm'
            },
            {
                extend:    'pdfHtml5',
                text:      'Descargar Pdf <i class="fa fa-file-pdf-o"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-success btn-flat btn-sm',
                title: '',
                orientation: 'landscape',
                pageSize: 'LEGAL',
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
                        text: '',
                        style: 'subheader'
                    });
                    doc.content.splice(3, 0, {
                        alignment: 'center',
                        text: ('Reporte de Inventario ' + $report_text).toUpperCase(),
                        style: 'subheader'
                    });
                    doc.content[4].table.widths = ['5%', '30%', '10%', '10%', '15%', '15%', '15%'];
                    doc.content[4].margin = [0, 35, 0, 0];
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
}


$(function () {

    $('#products').on('change',function () {
        generate_report();
    });

    generate_report();
});
