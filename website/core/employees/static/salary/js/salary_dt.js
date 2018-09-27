var table;
$(function () {
    table = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        columnDefs: [
            {orderable: false, targets: [-1]}
        ]
    });

    $("#id_year").datepicker({
        format: "yyyy",
        autoclose: true,
        minViewMode: "years",
        orientation: "down bottom"
    }).on('changeDate', function (e) {
        search_payroll();
    });

    $('#id_month').change(function () {
        search_payroll();
    });

    function search_payroll() {

        $('#btnRemoveSalary').prop('disabled', true);

        table = $('#data').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {
                    action: 'search_salaries',
                    month: $('#id_month').val(),
                    year: $('#id_year').val()
                },
                dataSrc: ""
            },
            columnDefs: [
                {
                    targets: [4, 5, 7, 8],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data;
                    }
                },
                {
                    targets: [6],
                    class: 'text-center'
                }
            ],
            rowCallback: function (row, data, index) {
                $('#btnRemoveSalary').prop('disabled', false);
            },
        });
    }

    $('#btnRemoveSalary').on('click', function () {
        $('.tooltip').remove();
        var month = $("#id_month option:selected").text(), year = $('#id_year').val();
        action_by_ajax_with_alert('Notificación',
            '¿Estas seguro de eliminar el siguiente registro de sueldos?',
            pathname,
            {year: year, month: $('#id_month').val(), action: 'delete'},
            function () {
                location.reload();
            },
            'Sueldos eliminados correctamente'
        );
    });

});
