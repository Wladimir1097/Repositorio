var tblMedidores;
var tblSellos;
var bodega = ["Wagner", "ProEnergy"];
var billing = {
    details: {
        date_joined: "",
        cantmed: 0,
        cantsell: 0,
        medidores: [],
        sellos: [],
    },
    add_med: function (item) {
        billing.details.medidores.push(item);
        this.load_med();
    },
    add_sell: function (item) {
        billing.details.sellos.push(item);
        this.load_med();
    },
    get_med: function () {
        $.each(this.details.medidores, function (i, item) {
            item.pos = i;
        });

        /*=====================================================*/

        $.each(this.details.sellos, function (i, item) {
            item.pos = i;
        });

        /*=====================================================*/

        console.clear();
        console.log(billing.details);
    },
    load_med: function () {
        this.get_med();
        tblMedidores = $('#tblMedidores').DataTable({
            order: [0, 'desc'],
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.medidores,
            columns: [
                {data: "pos"},
                {data: "num1"},
                {data: "num2"},
                {data: "tiponom"},
                {data: "bod"},
                {data: "option"},
            ],
            columnDefs: [
                {visible: false, targets: [0]},
                {
                    targets: ['_all'],
                    class: 'text-center',
                },
                {
                    targets: [1, 2],
                    render: function (data, type, row) {
                        return '<b>' + data + '</b>';
                    }
                },

                {
                    targets: [4],
                    render: function (data, type, row) {
                        return '<b>' + bodega[data] + '</b>';
                    }
                },
                {
                    targets: [-1],
                    orderable: false,
                    data: null,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a>';
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
        tblSellos = $('#tblSellos').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            order: [0, 'desc'],
            ordering: false,
            data: this.details.sellos,
            columns: [
                {data: "pos"},
                {data: "num1"},
                {data: "num2"},
                {data: "bod"},
                {data: "option"},
            ],
            columnDefs: [
                {visible: false, targets: [0]},
                {
                    targets: ['_all'],
                    class: 'text-center',
                },
                {
                    targets: [1, 2],
                    render: function (data, type, row) {
                        return '<b>' + data + '</b>';
                    }
                },
                {
                    targets: [3],
                    render: function (data, type, row) {
                        return '<b>' + bodega[data] + '</b>';
                    }
                },
                {
                    targets: [-1],
                    data: null,
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a>';
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
    },
    get_med_ids: function () {
        var data = [];
        $.each(this.details.medidores, function (i, item) {
            data.push(item.id);
        });
        return data;
    },
    get_sell_ids: function () {
        var data = [];
        $.each(this.details.sellos, function (i, item) {
            data.push(item.id);
        });
        return data;
    },
    exists_med: function () {
        return this.details.medidores.length > 0;
    }
};

$(function () {
    /*=============================================================================================*/
    $('#fecha').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        orientation: 'bottom bottom',
        language: 'es',
        setDate: new Date()
    });

    /*=============================================================================================*/

    $("input[name='med']").TouchSpin({
        min: 0,
        max: 99999999999
    });
    $("input[name='med']").keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('#id_typeProd').on('change', function () {
        $('#tipo').show();
        if ($(this).val() === '2') {
            $('#tipo').hide();
        }
    });
    $('#id_typeProd2').on('change', function () {
        $('#tipo2').show();
        if ($(this).val() === '2') {
            $('#tipo2').hide();
        }
    });
    /*=============================================================================================*/

    $('#btnRemoveMed').on('click', function () {
        if (billing.details.medidores.length === 0) {
            return false;
        }
        action_alert('Notificación', '¿Estas seguro de eliminar todo el detalle de Medidores?', function () {
            billing.details.medidores = [];
            billing.load_med();
        });
    });

    $('#btn1').on('click', function () {
        var num1 = parseInt($('#med1').val());
        var num2 = parseInt($('#med2').val());
        var opcion = parseInt($('#id_typeProd').val());
        var cual = parseInt($('#id_type').val());
        var tipo = parseInt($("#tipo option:selected").val());
        var nom = $("#tipo option:selected").text();
        if (num1 > num2) {
            error_message('La numeracion final debe ser mayor a la final');
        } else {
            var item = {
                'pos': 0, 'num1': num1, 'num2': num2, 'ban': 1, 'tipo': tipo, 'tiponom': nom, 'bod': cual, 'option': 0
            };
            opcion === 1 ? billing.add_med(item) : billing.add_sell(item);
        }
        $('#med1').val("0");
        $('#med2').val("0");

    });

    $('#tblMedidores tbody').on('click', 'a[rel="remove"]', function () {
        var row = tblMedidores.row($(this).parents('tr')).data();
        action_alert('Notificación', '¿Estas seguro de eliminar la siguiente fila de medidores?', function () {
            billing.details.medidores.splice(row.pos, 1);
            billing.load_med();
        });
    });

    /*=============================================================================================*/

    $('#btn2').on('click', function () {
        var num1 = parseInt($('#med3').val());
        var opcion = parseInt($('#id_typeProd2').val());
        var cual = parseInt($('#id_type2').val());
        var tipo = parseInt($("#tipo2 option:selected").val());
        var nom = $("#tipo2 option:selected").text();
        var item = {
            'pos': 0, 'num1': num1, 'num2': 0, 'tipo': tipo, 'tiponom': nom, 'ban': 2, 'bod': cual, 'option': 0
        };
        opcion === 1 ? billing.add_med(item) : billing.add_sell(item);
        $('#med3').val("0");
    });

    $('#tblSellos tbody').on('click', 'a[rel="remove"]', function () {
        var row = tblSellos.row($(this).parents('tr')).data();
        action_alert('Notificación', '¿Estas seguro de eliminar la siguiente fila de sello?', function () {
            billing.details.sellos.splice(row.pos, 1);
            billing.load_med();
        });
    });

    $('#btnRemoveSell').on('click', function () {
        if (billing.details.sellos.length === 0) {
            return false;
        }
        action_alert('Notificación', '¿Estas seguro de eliminar todo el detalle de sellos?', function () {
            billing.details.sellos = [];
            billing.load_med();
        });
    });

    /*=============================================================================================*/

    $('#frmGestion').formValidation({
        message: 'El valor no es valido',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        excluded: [':disabled'],
        fields: {
            date_joined: {
                validators: {
                    date: {
                        format: 'YYYY-MM-DD',
                        message: 'La fecha de registro no es válida'
                    }
                }
            },
        }
    })
        .on('err.validator.fv', function (e, data) {
            data.element
                .data('fv.messages')
                .find('.help-block[data-fv-for="' + data.field + '"]').hide()
                .filter('[data-fv-validator="' + data.validator + '"]').show();
        })
        .on('err.field.fv', function (e, data) {
            var $tabPane = data.element.parents('.tab-pane'),
                tabId = $tabPane.attr('id');
            $('a[href="#' + tabId + '"][data-toggle="tab"]')
                .parent()
                .find('i')
                .removeClass('fa-check')
                .addClass('fa-times');
        })
        .on('success.field.fv', function (e, data) {

            var $parent = data.element.parents('.form-group');
            $parent.removeClass('has-success');
            data.element.data('fv.icon').hide();

            var $tabPane = data.element.parents('.tab-pane'),
                tabId = $tabPane.attr('id'),
                $icon = $('a[href="#' + tabId + '"][data-toggle="tab"]')
                    .parent()
                    .find('i')
                    .removeClass('fa-check fa-times');
            var isValidTab = data.fv.isValidContainer($tabPane);
            if (isValidTab !== null) {
                $icon.addClass(isValidTab ? 'fa-check' : 'fa-times');
            }
        })
        .on('success.form.fv', function (e) {
            e.preventDefault()
            var $form = $(e.target);
            var fv = $form.data('formValidation');
            fv.disableSubmitButtons(false);

            billing.details.date_joined = $('#fecha').val();
            billing.details.cantmed = billing.details.medidores.length;
            billing.details.cantsell = billing.details.sellos.length;


            if (!billing.exists_med()) {
                error_message('Debe agregar un item al menos al detalle de la distribucion');
                return false;
            }
            var modo = getParameterByName('action');
            var pk = getParameterByName('id');
            if (modo == 'new') {
                pk = 0
            }
            var msg = 'Registro ingresado correctamente';
            action_by_ajax_with_alert('Notificación',
                '¿Estas seguro de guardar la siguiente Distribucion?',
                pathname,
                {
                    //'action': $('#action').val(),
                    'action': modo,
                    'id': $('#id').val(),
                    'pk': pk,
                    'items': JSON.stringify(billing.details),
                },
                function () {
                    location.href = pathname;
                },
                msg
            );


        });

    function getParameterByName(name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(location.search);
        return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    }
});
