var tblSearchProducts, tblProducts;
var billing = {
    details: {
        prov: "",
        date_joined: "",
        subtotal: 0.00,
        iva: 0.00,
        total: 0.00,
        products: [],
    },
    get_products_ids: function () {
        var prods = [];
        $.each(this.details.products, function (i, item) {
            prods.push(item.id);
        });
        return prods;
    },
    add_products: function (item) {
        billing.details.products.push(item);
        this.load_products();
    },
    get_produts: function () {
        var subtotal = 0.00;
        $.each(this.details.products, function (i, item) {

            if (item.cat === 'Equipos') {
                item.cant = billing.details.products[i].codes.length;
            }

            item.pos = i;
            item.cost = parseFloat(item.cost);
            item.subtotal = parseInt(item.cant) * item.cost;
            subtotal += item.subtotal;
        });
        billing.details.subtotal = subtotal.toFixed(2);
        //billing.details.iva = parseFloat(billing.details.subtotal * 0.12).toFixed(2);
        billing.details.iva = 0;
        billing.details.total = (parseFloat(billing.details.subtotal) + parseFloat(billing.details.iva)).toFixed(2);

        $('#subtotal').html('$' + billing.details.subtotal);
        $('#iva').html('$' + billing.details.iva);
        $('#total').html('$' + billing.details.total);

        console.clear();
        console.log(billing.details);
    },
    load_products: function () {
        this.get_produts();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.details.products,
            ordering: false,
            lengthChange: false,
            bPaginate: false,
            columns: [
                {data: "pos"},
                {data: "id"},
                {data: "name"},
                {data: "image"},
                {data: "cant"},
                {data: "cat"},
                {data: "cost"},
                {data: "subtotal"},
                {data: "option"},
            ],
            columnDefs: [
                {visible: false, targets: [0]},
                {
                    targets: [1, 5, 7, 8],
                    class: 'text-center',
                },
                {
                    targets: [3],
                    orderable: false,
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<img src="' + data + '" style="width: 25px; height: 25px;" class="img-responsive center-block">';
                    }
                },
                {
                    targets: [4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.cat === 'Equipos') {
                            return row.cant;
                        }
                        return '<input type="text" class="form-control input-sm" autocomplete="off" name="cant" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [6],
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control input-sm" autocomplete="off" name="cost" autocomplete="off" value="' + data.toFixed(2) + '">';
                    }
                },
                {
                    targets: [7],
                    render: function (data, type, row) {
                        //return parseFloat(data).toFixed(2);
                        return '<input type="text" class="form-control input-sm subt" autocomplete="off"  name="subt" autocomplete="off" readonly="readonly" value="' + parseFloat(data).toFixed(2) + '">';
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
                var row = $(row).closest('tr');

                row.find("input[name='cost']").TouchSpin({
                    min: 0.01,
                    max: 1000000,
                    step: 0.01,
                    decimals: 2,
                    boostat: 5
                });

                row.find("input[name='cant']").TouchSpin({
                    min: 1,
                    max: 10000000
                });
                row.find("input[name='subt']").TouchSpin({
                    min: 0.01,
                    max: 1000000,
                    step: 0.01,
                    decimals: 2,
                    boostat: 5
                });

                row.find('input[name="cant"]').keypress(function (e) {
                    return validate_form_text('numbers', e, null);
                });

                row.find('input[name="cost"]').keypress(function (e) {
                    return validate_decimals($(this), e);
                });

                row.find('input[name="subt"]').keypress(function (e) {
                    return validate_decimals($(this), e);
                });

                if (data.cant === 0) {
                    $('td', row).css('background-color', '#fff4e4');
                }
                else {
                    $('td', row).css('background-color', '#ffffff');
                }

            },
            initComplete: function (settings, json) {

            },

        });
    },
    exists_products: function () {
        var ok = true;
        $.each(this.details.products, function (i, item) {
            if (item.cant === 0) {
                ok = false;
            }
        });
        return ok;
    },
    save_data: function () {
        billing.details.prov = $('#id_prov').val();
        billing.details.date_joined = $('#id_date_joined').val();
    }
};

$(function () {

    /*EVENTOS DE LA TABLA DETALLE DE PRODUCTOS
    =============================================================================================*/

    $('input[name="cant"]').keypress(function (e) {
        return validate_form_text('numbers', e, null);
    });

    $('input[name="cost"]').keypress(function (e) {
        return validate_decimals($(this), e);
    });

    $('input[name="subt"]').keypress(function (e) {
        return validate_decimals($(this), e);
    });

    $('#tblProducts tbody').on('change', 'input[name="cant"]', function () {
        var row = tblProducts.row($(this).parents('tr')).data();
        billing.details.products[row.pos].cant = $(this).val();
        billing.get_produts();
        var nRow = $(this).parents('tr')[0];
        $('td:eq(6)', nRow).html('<input type="text" class="form-control input-sm subt" autocomplete="off" name="subt" autocomplete="off" value="' + billing.details.products[row.pos].subtotal.toFixed(2) + '">');
    });
    $('#tblProducts tbody').on('change', 'input[name="subt"]', function () {
        var row = tblProducts.row($(this).parents('tr')).data();
        billing.details.products[row.pos].cost = parseFloat($(this).val())/parseInt(billing.details.products[row.pos].cant);
        billing.get_produts();
        var nRow = $(this).parents('tr')[0];
        $('td:eq(5)', nRow).html(billing.details.products[row.pos].cost.toFixed(2));
    });
    $('#tblProducts tbody').on('click', 'a[rel="remove"]', function () {
        var row = tblProducts.row($(this).parents('tr')).data();
        action_alert('Notificación', '¿Estas seguro de eliminar la siguiente fila de materiales?', function () {
            billing.details.products.splice(row.pos, 1);
            billing.load_products();
        });
    });

    $('#tblProducts tbody').on('change', 'input[name="cost"]', function () {
        var row = tblProducts.row($(this).parents('tr')).data();
        billing.details.products[row.pos].cost = $(this).val();
        billing.get_produts();
        var nRow = $(this).parents('tr')[0];
        $('td:eq(6)', nRow).html(billing.details.products[row.pos].subtotal.toFixed(2));
    });

    /*OPCIONES */

    $('#btnRemoveProducts').on('click', function () {
        if (billing.details.products.length === 0) {
            return false;
        }
        action_alert('Notificación', '¿Estas seguro de eliminar todo el detalle de materiales?', function () {
            billing.details.products = [];
            billing.load_products();
        });
    });

    $('#id_date_joined').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        orientation: 'bottom bottom',
        language: 'es'
    }).on('changeDate', function (e) {
        $('#frmIngress').formValidation('revalidateField', 'date_joined');
    });

    /*SELECCIÓN DE LOS PROVEEDORES
    =============================================================================================*/

    $('#id_prov').on('change', function () {
        $.ajax({
            dataType: 'JSON',
            type: 'POST',
            url: pathname,
            data: {
                id: $(this).val(), action: 'get_provider'
            },
            success: function (data) {
                $('#pruc').val(data.ruc);
                $('#pphone').val(data.phone);
                $('#pemail').val(data.email);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                error_message(errorThrown + ' ' + textStatus);
            }
        })
    });

    /*BÚSQUEDA DE PRODUCTOS
   =============================================================================================*/

    $('#btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                data: {action: 'search_products', prods: JSON.stringify(billing.get_products_ids())},
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
                    targets: 2,
                    orderable: false,
                    data: null,
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<img class="img-responsive center-block" src="' + data[2] + '" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: 4,
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data;
                    }
                },
                {
                    targets: 5,
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data === 0) {
                            return 'Sin Stock';
                        }
                        return data;
                    }
                },
            ],
            rowCallback: function (row, data) {
                if (data[5] === 0) {
                    $('td:eq(5)', row).css({'background-color': '#F44336', 'color': 'white'});
                }
            }
        });
        $('#myModalProducts').modal('show');
    });

    $('#tblSearchProducts tbody').on('click', 'a[rel="add"]', function () {
        var td = tblSearchProducts.cell($(this).closest('td, li')).index(),
            row = tblSearchProducts.row(td.row).data();
        var cant = row[3] === 'Equipos' ? 0 : 1;
        var item = {
            'pos': 0, 'id': row[0], 'name': row[1], 'image': row[2], 'cant': cant,
            'cat': row[3], 'cost': row[4], 'iva': 0.00,
            'subtotal': 0.00, 'total': 0.00, 'option': 0
        };
        billing.add_products(item);
        tblSearchProducts.row(td.row).remove().draw();
    });

    /*FRM INGRESO
    =============================================================================================*/

    $('#frmIngress').formValidation({
        message: 'El valor no es valido',
        icon: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            date_joined: {
                validators: {
                    date: {
                        format: 'YYYY-MM-DD',
                        message: 'La fecha de nacimiento no es válida'
                    }
                }
            },
            prov: {
                validators: {
                    notEmpty: {
                        message: 'Selecciona un proveedor'
                    },
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
        .on('success.field.fv', function (e, data) {
            var $parent = data.element.parents('.form-group');
            $parent.removeClass('has-success');
            data.element.data('fv.icon').hide();
        })
        .on('success.form.fv', function (e) {
            e.preventDefault()
            var $form = $(e.target);
            var fv = $form.data('formValidation');
            fv.disableSubmitButtons(false);

            if (!billing.exists_products()) {
                error_message('Existen Equipos sin códigos de series !!');
                return false;
            }

            if (billing.details.products.length === 0) {
                error_message('Debe al menos agregar un material para realizar una orden !!');
                return false;
            }

            billing.save_data();

            action_by_ajax_with_alert('Notificación',
                '¿Estas seguro de guardar la siguiente orden?',
                pathname,
                {
                    'action': 'new',
                    'id': 0,
                    'items': JSON.stringify(billing.details)
                },
                function () {
                    location.href = pathname;
                },
                'orden registrada correctamente'
            );

        });

});
