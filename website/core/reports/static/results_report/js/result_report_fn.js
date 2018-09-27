function generate_report() {
    var $month = $('#month').val();
    var $filter = $('#filter').val();

    var data = {
        filter: $filter,
        year: $('#year').val(),
        month: $month,
        start_date: $('#start_date').val(),
        end_date: $('#end_date').val()
    };

    var $report_text = "";

    if ($month === "" && $filter === '3') {
        $filter = '2';
    }

    var now = new Date();
    var jsDate = now.getDate() + '-' + (now.getMonth() + 1) + '-' + now.getFullYear();

    switch ($filter) {
        case '1':
            $report_text += 'Desde ' + $("#start_date").val() + ' hasta ' + $("#end_date").val();
            break;
        case '2':
            $report_text += 'del Año ' + $("#year").val();
            break;
        case '3':
            $report_text += 'del Año ' + $("#year").val();
            $report_text += ' y del mes de ' + $("#month option:selected").text().toUpperCase();
            break;
    }

    $('#data').DataTable({
        destroy: true,
        responsive: true,
        autoWidth: false,
        searching: false,
        lengthChange: false,
        paging: false,
        ordering: false,
        info: false,
        ajax: {
            url: pathname,
            type: 'POST',
            data: data,
            dataSrc: ""
        },
        columnDefs: [
            {
                targets: [0, 1, 2, 3, 4],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + data;
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
                targets: 6,
                bSortable: false,
                data: null,
                class: 'text-center',
                render: function (data, type, row) {
                    if (data[6] === 1) {
                        return '<span class="label label-primary">Ganancia</span>';
                    }
                    else if (data[6] === 2) {
                        return '<span class="label label-warning">No hubo ni perdidas ni ganancias</span>';
                    }
                    else if (data[6] === 3) {
                        return '<span class="label label-danger">Perdida</span>';
                    }
                }
            },
        ],
        rowCallback: function (row, data, index) {
            graph_report(data);
        },
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fa fa-file-excel-o"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-sm'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="fa fa-file-pdf-o"></i>',
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
                        text: '' + jsDate,
                        style: 'subheader'
                    });
                    doc.content.splice(3, 0, {
                        alignment: 'center',
                        text: ('Reporte de Ganacias y Perdidas ' + $report_text).toUpperCase(),
                        style: 'subheader'
                    });
                    doc.content[4].table.widths = ['15%', '15%', '15%', '15%', '15%', '25%'];
                    doc.content[4].margin = [0, 35, 0, 0];
                    doc.content[4].layout = {}
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

function graph_report(data) {
    Highcharts.chart('graphic', {
        title: {
            text: 'Resultados'
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            categories: ['Compras','Gastos','Compras','Ventas','Pedidos']
        },
        series: [{
            type: 'column',
            colorByPoint: true,
            data: [parseFloat(data[0]),parseFloat(data[1]),parseFloat(data[2]),parseFloat(data[3]), parseFloat(data[4])],
            showInLegend: false
        }]
    });
    $('#graphic').show();
}

$(function () {
    $('#filter').change(function () {
        var filter = $(this).val();
        $('#f_start_date').hide();
        $('#f_end_date').hide();
        $('#f_year').hide();
        $('#f_month').hide();
        table.clear().draw();
        if (filter) {
            switch (filter) {
                case '1':
                    $('#f_start_date').show();
                    $('#f_end_date').show();
                    generate_report();
                    break;
                case '2':
                    $('#f_year').show();
                    generate_report();
                    break;
                case '3':
                    $('#f_year').show();
                    $('#f_month').show();
                    generate_report();
                    break;
            }
        }
    });

    $("#year").datepicker({
        format: "yyyy",
        autoclose: true,
        minViewMode: "years",
        orientation: "down bottom"
    }).on('changeDate', function (e) {
        generate_report();
    });

    $("#start_date").datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        orientation: "down bottom"
    }).on('changeDate', function (e) {
        generate_report();
    });

    $("#end_date").datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        orientation: "down bottom"
    }).on('changeDate', function (e) {
        generate_report();
    });

    $('#month').on('change', function () {
        generate_report();
    });
});
