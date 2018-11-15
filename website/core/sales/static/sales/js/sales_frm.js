var tblSearchProducts, tblProducts;
var tblSearchServices, tblServices;


var billing = {
    details: {
        cli: "",
        date_joined: "",
        date_delivery: "",
        subtotal: 0.00,
        iva: 0.00,
        dscto: 0.00,
        total: 0.00,
        type: 1,
        products: [],
        services: [],
    },
    add_products: function (item) {
        billing.details.products.push(item);
        this.load_products();
    },
    add_services: function (item) {
        billing.details.services.push(item);
        this.load_products();
    },
    get_produts: function () {
        var subtotal = 0.00, dscto = 0.00;
        $.each(this.details.products, function (i, item) {
            item.pos = i;
            item.subtotal = item.cant * item.cost;
            item.deduction = item.subtotal * (item.dscto / 100);
            dscto += item.deduction;
            subtotal += item.subtotal;
        });

        /*=====================================================*/

        $.each(this.details.services, function (i, item) {
            item.pos = i;
            subtotal += item.cost;
        });

        /*=====================================================*/

        billing.details.dscto = dscto;
        billing.details.subtotal = subtotal;
        //billing.details.iva = (billing.details.subtotal-dscto) * iva;
        billing.details.iva = 0;
        billing.details.total = billing.details.subtotal + billing.details.iva;

        $('#subtotal').html('$' + billing.details.subtotal.toFixed(2));
        $('#dsctos').html('$' + billing.details.dscto.toFixed(2));
        $('#iva').html('$' + billing.details.iva.toFixed(2));
        $('#total').html('$' + billing.details.total.toFixed(2));

        console.clear();
        console.log(billing.details);
    },
    load_products: function () {
        this.get_produts();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ordering: false,
            bPaginate: false,
            lengthChange: false,
            data: this.details.products,
            columns: [
                {data: "pos"},
                {data: "id"},
                {data: "name"},
                {data: "stock"},
                {data: "cant"},
                {data: "cost"},
                {data: "subtotal"},
                {data: "option"},
            ],
            columnDefs: [
                {visible: false, targets: [0]},
                {
                    targets: ['_all'],
                    class: 'text-center',
                },
                {
                    targets: [3],
                    render: function (data, type, row) {
                        return '<b>' + data + '</b>';
                    }
                },
                {
                    targets: [4],
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-sm" autocomplete="off" name="cant" autocomplete="off" value="' + data + '">';
                    }
                },
                {
                    targets: [5, 6],
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    data: null,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                row = $(row).closest('tr');

                row.find("input[name='dscto']").TouchSpin({
                    min: 0,
                    max: 100,
                });

                row.find("input[name='cant']").TouchSpin({
                    min: 1,
                    max: data.stock
                });

                row.find('input[name="cant"]').keypress(function (e) {
                    return validate_form_text('numbers', e, null);
                });

            },
            initComplete: function (settings, json) {

            }
        });
        tblServices = $('#tblServices').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ordering: false,
            data: this.details.services,
            columns: [
                {data: "pos"},
                {data: "id"},
                {data: "name"},
                {data: "cost"},
                {data: "option"},
            ],
            columnDefs: [
                {visible: false, targets: [0]},
                {
                    targets: [3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data.toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    data: null,
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fa fa-trash" aria-hidden="true"></i></a>';
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
    },
    get_produts_ids: function () {
        var data = [];
        $.each(this.details.products, function (i, item) {
            data.push(item.id);
        });
        return data;
    },
    get_services_ids: function () {
        var data = [];
        $.each(this.details.services, function (i, item) {
            data.push(item.id);
        });
        return data;
    },
    exists_products: function () {
        return this.details.products.length > 0;
    }
};

$(function () {

    /*=============================================================================================*/

    $('#tblProducts tbody').on('change', 'input[name="cost"]', function () {
        var row = tblProducts.row($(this).parents('tr')).data();
        billing.details.products[row.pos].cost = $(this).val();
        billing.get_produts();
        var nRow = $(this).parents('tr')[0];
        $('td:eq(6)', nRow).html(billing.details.products[row.pos].subtotal.toFixed(2));
    });

    $('#tblProducts tbody').on('change', 'input[name="cant"]', function () {
        var row = tblProducts.row($(this).parents('tr')).data();
        billing.details.products[row.pos].cant = parseInt($(this).val());
        //billing.load_products();
        billing.get_produts();
        var nRow = $(this).parents('tr')[0];
        $('td:eq(5)', nRow).html(billing.details.products[row.pos].subtotal.toFixed(2));
    });
    /*=============================================================================================*/

    $('#id_date_joined').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        orientation: 'bottom bottom',
        language: 'es',
        setDate: new Date()
    })
        .on('changeDate', function (e) {
            $("#id_date_delivery").datepicker('setStartDate', $(this).val());
            $('#id_date_delivery').datepicker('setDate', $(this).val());
            $('#frmSales').formValidation('revalidateField', 'date_delivery');
        })

    $('#id_date_delivery').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        orientation: 'bottom bottom',
        language: 'es',
    }).on('changeDate', function (e) {
        $('#frmSales').formValidation('revalidateField', 'date_joined');
        $('#frmSales').formValidation('revalidateField', 'date_delivery');
    });

    /*=============================================================================================*/

    $('#id_cli').on('change', function () {
        $.ajax({
            dataType: 'JSON',
            type: 'POST',
            url: pathname,
            data: {
                id: $(this).val(), action: 'get_client'
            },
            success: function (data) {
                $('#pdni').val(data.dni);
                $('#pphone').val(data.phone);
                $('#pemail').val(data.email);
                $('#paddress').val(data.address);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                error_message(errorThrown + ' ' + textStatus);
            }
        })
    });

    $('#id_cli').change();

    $('#id_date_joined').change();

    /*=============================================================================================*/

    $('#id_type').on('change', function () {
        $('#pnlDelivery').hide();
        $('[href="#tab2"]').closest('li').show();
        if ($(this).val() === '2') {
            $('#pnlDelivery').show();
            $("#id_date_delivery").datepicker('setStartDate', $('#id_date_joined').val());
            $('[href="#tab2"]').closest('li').hide();
        }
    });

    /*=============================================================================================*/

    $('#btnRemoveProducts').on('click', function () {
        if (billing.details.products.length === 0) {
            return false;
        }
        action_alert('Notificación', '¿Estas seguro de eliminar todo el detalle de materiales?', function () {
            billing.details.products = [];
            billing.load_products();
        });
    });

    $('#btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {action: 'search_products', items: JSON.stringify(billing.get_produts_ids())},
                dataSrc: ""
            },
            columnDefs: [
                {
                    targets: [-1],
                    orderable: false,
                    data: null,
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="add" class="btn btn-primary btn-xs btn-flat"><i class="fa fa-plus" aria-hidden="true"></i></a>'
                    }
                },
                {
                    targets: [2],
                    class: 'text-center',
                },
                {
                    targets: [3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data;
                    }
                }
            ]
        });
        $('#myModalProducts').modal('show');
    });

    $('#tblSearchProducts tbody').on('click', 'a[rel="add"]', function () {
        var row = tblSearchProducts.row($(this).parents('tr')).data();
        var date_now = moment().format('YYYY-MM-DD');
        var item = {
            'pos': 0, 'id': row[0], 'name': row[1], 'cant': 1, 'deduction': 0.00,
            'cost': parseFloat(row[3]), 'dscto': 0, 'stock': parseInt(row[2]),
            'subtotal': 0.00, 'option': 0
        };
        billing.add_products(item);
        tblSearchProducts.row($(this).parents('tr')).remove().draw();
    });

    $('#tblProducts tbody').on('click', 'a[rel="remove"]', function () {
        var row = tblProducts.row($(this).parents('tr')).data();
        action_alert('Notificación', '¿Estas seguro de eliminar la siguiente fila de materiales?', function () {
            billing.details.products.splice(row.pos, 1);
            billing.load_products();
        });
    });

    /*=============================================================================================*/

    $('#btnSearchServices').on('click', function () {
        tblSearchServices = $('#tblSearchServices').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {action: 'search_services', items: JSON.stringify(billing.get_services_ids())},
                dataSrc: ""
            },
            columnDefs: [
                {
                    targets: [-1],
                    orderable: false,
                    data: null,
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="add" class="btn btn-primary btn-xs btn-flat"><i class="fa fa-plus" aria-hidden="true"></i></a>'
                    }
                },
                {
                    targets: [2],
                    class: 'text-center',
                },
                {
                    targets: [3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data;
                    }
                }
            ]
        });
        $('#myModalServices').modal('show');
    });

    $('#tblSearchServices tbody').on('click', 'a[rel="add"]', function () {
        var row = tblSearchServices.row($(this).parents('tr')).data();
        var item = {
            'pos': 0, 'id': row[0], 'name': row[1], 'cost': parseFloat(row[2]), 'option': 0
        };
        billing.add_services(item);
        tblSearchServices.row($(this).parents('tr')).remove().draw();
    });

    $('#tblServices tbody').on('click', 'a[rel="remove"]', function () {
        var row = tblServices.row($(this).parents('tr')).data();
        action_alert('Notificación', '¿Estas seguro de eliminar la siguiente fila de servicios?', function () {
            billing.details.services.splice(row.pos, 1);
            billing.load_products();
        });
    });

    $('#btnRemoveServices').on('click', function () {
        if (billing.details.services.length === 0) {
            return false;
        }
        action_alert('Notificación', '¿Estas seguro de eliminar todo el detalle de servicios?', function () {
            billing.details.services = [];
            billing.load_products();
        });
    });

    /*=============================================================================================*/

    $('#frmSales').formValidation({
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
            date_delivery: {
                validators: {
                    date: {
                        format: 'YYYY-MM-DD',
                        message: 'La fecha de entrega no es válida'
                    }
                }
            },
            cli: {
                validators: {
                    notEmpty: {
                        message: 'Selecciona una cliente'
                    },
                }
            }
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

            billing.details.cli = $('#id_cli').val();
            billing.details.date_joined = $('#id_date_joined').val();
            billing.details.date_delivery = $('#id_date_delivery').val();
            billing.details.type = parseInt($('#id_type').val());

            if (!billing.exists_products()) {
                error_message('Debe agregar un item al menos al detalle de la distribucion');
                return false;
            }
            var modo = getParameterByName('action');
            var pk = getParameterByName('id');
            if (modo == 'new') {
                pk = 0
            }
            var msg = billing.details.type === 1 ? 'Registro ingresado correctamente' : 'Pedido registrado correctamente';
            action_by_ajax_with_alert('Notificación',
                '¿Estas seguro de guardar la siguiente Distribucion?',
                pathname,
                {
                    //'action': $('#action').val(),
                    'action':modo,
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
