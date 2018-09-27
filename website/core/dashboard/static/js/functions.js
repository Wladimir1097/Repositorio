function validate_dni_ruc(dni) {
    /* alert(dni); */

    if (dni === '9999999999999'){
        return true;
    }

    var expr = dni.substr(0, 2);
    if (expr === "EX" | expr === "ex") {
        return true;
    }


    var suma = 0;
    var residuo = 0;
    var pri = false;
    var pub = false;
    var nat = false;
    var dniProvincias = 22;
    var modulo = 11;

    /* Verifico que el campo no contenga letras */
    var ok = 1;
    for (i = 0; i < dni.length && ok == 1; i++) {
        var n = parseInt(dni.charAt(i));
        if (isNaN(n)) ok = 0;
    }
    if (ok == 0) {
        //alert("No puede ingresar caracteres en el número");
        return false;
    }

    if (dni.length < 10) {
        //alert('El número ingresado no es válido');
        return false;
    }

    /* Los primeros dos digitos corresponden al codigo de la provincia */
    provincia = dni.substr(0, 2);
    if (provincia < 1 || provincia > dniProvincias) {
        //alert('El código de la provincia (dos primeros dígitos) es inválido');
        return false;
    }

    /* Aqui almacenamos los digitos de la dni en variables. */
    d1 = dni.substr(0, 1);
    d2 = dni.substr(1, 1);
    d3 = dni.substr(2, 1);
    d4 = dni.substr(3, 1);
    d5 = dni.substr(4, 1);
    d6 = dni.substr(5, 1);
    d7 = dni.substr(6, 1);
    d8 = dni.substr(7, 1);
    d9 = dni.substr(8, 1);
    d10 = dni.substr(9, 1);

    /* El tercer digito es: */
    /* 9 para sociedades privadas y extranjeros   */
    /* 6 para sociedades publicas */
    /* menor que 6 (0,1,2,3,4,5) para personas naturales */

    if (d3 == 7 || d3 == 8) {
        //alert('El tercer dígito ingresado es inválido');
        return false;
    }

    /* Solo para personas naturales (modulo 10) */
    if (d3 < 6) {
        nat = true;
        p1 = d1 * 2;
        if (p1 >= 10) p1 -= 9;
        p2 = d2 * 1;
        if (p2 >= 10) p2 -= 9;
        p3 = d3 * 2;
        if (p3 >= 10) p3 -= 9;
        p4 = d4 * 1;
        if (p4 >= 10) p4 -= 9;
        p5 = d5 * 2;
        if (p5 >= 10) p5 -= 9;
        p6 = d6 * 1;
        if (p6 >= 10) p6 -= 9;
        p7 = d7 * 2;
        if (p7 >= 10) p7 -= 9;
        p8 = d8 * 1;
        if (p8 >= 10) p8 -= 9;
        p9 = d9 * 2;
        if (p9 >= 10) p9 -= 9;
        modulo = 10;
    }

    /* Solo para sociedades publicas (modulo 11) */
    /* Aqui el digito verficador esta en la posicion 9, en las otras 2 en la pos. 10 */
    else if (d3 == 6) {
        pub = true;
        p1 = d1 * 3;
        p2 = d2 * 2;
        p3 = d3 * 7;
        p4 = d4 * 6;
        p5 = d5 * 5;
        p6 = d6 * 4;
        p7 = d7 * 3;
        p8 = d8 * 2;
        p9 = 0;
    }

    /* Solo para entidades privadas (modulo 11) */
    else if (d3 == 9) {
        pri = true;
        p1 = d1 * 4;
        p2 = d2 * 3;
        p3 = d3 * 2;
        p4 = d4 * 7;
        p5 = d5 * 6;
        p6 = d6 * 5;
        p7 = d7 * 4;
        p8 = d8 * 3;
        p9 = d9 * 2;
    }

    suma = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8 + p9;
    residuo = suma % modulo;

    /* Si residuo=0, dig.ver.=0, caso contrario 10 - residuo*/
    digitoVerificador = residuo == 0 ? 0 : modulo - residuo;

    /* ahora comparamos el elemento de la posicion 10 con el dig. ver.*/
    if (pub == true) {
        if (digitoVerificador != d9) {
            //alert('El ruc de la empresa del sector público es incorrecto.');
            return false;
        }
        /* El ruc de las empresas del sector publico terminan con 0001*/
        if (dni.substr(9, 4) != '0001') {
            //alert('El ruc de la empresa del sector público debe terminar con 0001');
            return false;
        }
    }
    else if (pri == true) {
        if (digitoVerificador != d10) {
            //alert('El ruc de la empresa del sector privado es incorrecto.');
            return false;
        }
        if (dni.substr(10, 3) != '001') {
            //alert('El ruc de la empresa del sector privado debe terminar con 001');
            return false;
        }
    }

    else if (nat == true) {
        if (digitoVerificador != d10) {
            //alert('El número de cédula de la persona natural es incorrecto.');
            return false;
        }
        if (dni.length > 10 && dni.substr(10, 3) != '001') {
            //alert('El ruc de la persona natural debe terminar con 001');
            return false;
        }
    }
    return true;
}
function message(text) {
    $.LoadingOverlay("show", {
        image: "",
        fontawesome: "fa fa-spinner fa-spin",
        custom: $("<div>", {
            css: {
                'font-family': "'Source Sans Pro', 'Helvetica Neue', Helvetica, Arial, sans-serif'",
                'font-size': '16px',
                'font-weight': '600',
                'margin-top': '5px'
            },
            text: text
        })
    });
    setTimeout(function () {
        $.LoadingOverlay("hide");
    }, 750);
}
function message_url(text, url) {
    $.LoadingOverlay("show", {
        image: "",
        fontawesome: "fa fa-refresh fa-spin",
        custom: $("<div>", {
            css: {
                'font-family': "'Source Sans Pro', 'Helvetica Neue', Helvetica, Arial, sans-serif'",
                'font-size': '16px',
                'font-weight': '600',
                'margin-top': '5px'
            },
            text: text
        })
    });
    setTimeout(function () {
        $.LoadingOverlay("hide");
        window.location = url;
    }, 750);
}
/*=========================================================*/
function load_image(src) {
    $.confirm({
        theme: 'modern',
        type: 'blue',
        title: 'Visualización de foto',
        icon: 'fa fa-file-image-o',
        content: '<img class="img-responsive img-thumbnail center-block" src="' + src + '" style="height: 300px;">',
        autoClose: 'cancelAction|8000',
        buttons: {
            cancelAction: {
                text: "Salir",
                btnClass: 'btn-red',
                action: function () {

                }
            }
        }
    });
}
function get_message_action_by_id(id) {
    var number = parseInt(id);
    return number === 0 ? 'Registro guardado' :'Registro actualizado';
}
function action_by_ajax(url,parameters,callback) {
    $.ajax({
        url: url,
        data: parameters,
        method: 'POST',
        success: function (data) {
            if (data.resp) {
                callback();
                return false;
            }
            error_message(data.error);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            error_message(errorThrown + ' ' + textStatus);
        }
    });
}
function action_by_ajax_with_alert(title,content,url,parameters,callback,message) {
    $.confirm({
        theme: 'modern',
        type: 'blue',
        title: title,
        icon: 'fa fa-info-circle',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: "btn-primary",
        buttons: {
            info: {
                text: "Aceptar",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url,
                        data: parameters,
                        method: 'POST',
                        /*contentType:false,
                        processData:false,
                        cache:false,*/
                        success: function (data) {
                            if (data.resp) {
                                guarded_message(message,callback);
                                return false;
                            }
                            error_message(data.error);
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                            error_message(errorThrown + ' ' + textStatus);
                        }
                    });
                }
            },
            danger: {
                text: "Cancelar",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    });
}
function action_by_ajax_formdata_with_alert(title,content,url,parameters,callback,message) {
    $.confirm({
        theme: 'modern',
        type: 'blue',
        title: title,
        icon: 'fa fa-info-circle',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: "btn-primary",
        buttons: {
            info: {
                text: "Aceptar",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url,
                        data: parameters,
                        method: 'POST',
                        contentType:false,
                        processData:false,
                        cache:false,
                        success: function (data) {
                            if (data.resp) {
                                guarded_message(message,callback);
                                return false;
                            }
                            error_message(data.error);
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                            error_message(errorThrown + ' ' + textStatus);
                        }
                    });
                }
            },
            danger: {
                text: "Cancelar",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    });
}
function delete_registry_by_id(url,parameters,callback) {
    $.confirm({
        theme: 'modern',
        type: 'blue',
        title: 'Confirmación de Eliminación',
        icon: 'fa fa-info-circle',
        content: '¿Esta seguro de eliminar el siguiente registro?',
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: "btn-primary",
        buttons: {
            info: {
                text: "Aceptar",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url,
                        data: parameters,
                        method: 'POST',
                        success: function (data) {
                            if (data.resp) {
                                deleted_message(callback);
                                return false;
                            }
                            error_message(data.error);
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                           error_message(errorThrown + ' ' + textStatus);
                        }
                    });
                }
            },
            danger: {
                text: "Cancelar",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    });
}
function save_registry_by_submit(e, message, callback) {
    var $form = $(e.target);
    var $fv = $form.data('formValidation');
    $.confirm({
        theme: 'modern',
        type: 'blue',
        title: 'Confirmación de Acción',
        icon: 'fa fa-info-circle',
        content: '¿Esta seguro de realizar la siguiente?',
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: "btn-primary",
        buttons: {
            info: {
                text: "Aceptar",
                btnClass: 'btn-primary',
                action: function () {
                    $form.ajaxSubmit({
                        url: $form.attr('action'),
                        dataType: 'json',
                        success: function (data, statusText, xhr, $form) {
                            if (data.resp) {
                                guarded_message(message,callback);
                                return false;
                            }
                            error_message(data.error);
                        },
                        error: function (jqXHR, textStatus, errorThrown) {
                            error_message(errorThrown + ' ' + textStatus);
                        }
                    });
                }
            },
            danger: {
                text: "Cancelar",
                btnClass: 'btn-red',
                action: function () {
                    $fv.disableSubmitButtons(false);
                }
            },
        }
    });
}
function deleted_message(callback) {
    $.confirm({
        theme: 'modern',
        type: 'blue',
        title: 'Notificación',
        icon: 'fa fa-info-circle',
        content: 'Registro eliminado correctamente',
        autoClose: 'cancelAction|8000',
        buttons: {
            cancelAction: {
                btnClass: 'btn-red',
                text: "Salir",
                action: function () {
                    callback();
                }
            }
        }
    });
}
function error_message(message) {

    if(typeof(message) === "object") {
        var errors = '<ul style="list-style: square;">';
        $.each(message, function( index, item ) {
            errors+='<li>'+item+'</li>';
        });
        errors+='</ul>';
        message = errors;
    }

    $.confirm({
        theme: 'modern',
        type: 'blue',
        title: 'Advertencia',
        icon: 'fa fa-exclamation-triangle',
        content: message,
        autoClose: 'cancelAction|8000',
        buttons: {
            cancelAction: {
                text: "Salir",
                btnClass: 'btn-red',
                action: function () {

                }
            }
        }
    });
}
function guarded_message(message,callback) {
    $.confirm({
        theme: 'modern',
        type: 'blue',
        title: 'Notificación',
        icon: 'fa fa-info-circle',
        content: message,
        autoClose: 'cancelAction|8000',
        buttons: {
            cancelAction: {
                text: "Salir",
                btnClass: 'btn-red',
                action: function () {
                    callback();
                }
            }
        }
    });
}
function get_query_by_ajax(url, parameters) {
    var objs;
    $.ajax({
        url: url,
        type: 'POST',
        dataType: "json",
        async: false,
        data: parameters,
        success: function (request) {
             objs = request;
        },
        error: function (jqXHR, textStatus, errorThrown) {
            error_message(errorThrown + ' ' + textStatus);
        }
    });
    console.clear();
    return objs;
}
function action_alert(title,content,callback) {
    $.confirm({
        theme: 'modern',
        type: 'blue',
        title: title,
        icon: 'fa fa-info-circle',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: "btn-primary",
        buttons: {
            info: {
                text: "Aceptar",
                btnClass: 'btn-primary',
                action: function () {
                   callback();
                }
            },
            danger: {
                text: "Cancelar",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    });
}
function validate_form_text(type, event, regex) {

    var key = event.keyCode || event.which;
    var numbers = (key > 47 && key < 58) || key === 8;
    var numbers_spaceless = (key > 47 && key < 58);
    var letters = !((key!==32) && (key<65) || (key>90) && (key<97) || (key>122 && key !== 241 && key !== 209 && key !== 225 && key !== 233 && key !== 237 && key !== 243 && key !== 250 && key !== 193 && key !== 201 && key !== 205 && key !== 211 && key !== 218))|| key === 8;
    var letters_spaceless = !((key<65) || (key>90) && (key<97) || (key>122 && key !== 241 && key !== 209 && key !== 225 && key !== 233 && key !== 237 && key !== 243 && key !== 250 && key !== 193 && key !== 201 && key !== 205 && key !== 211 && key !== 218))|| key === 8;
    var decimals = ((key > 47 && key < 58) || key === 8 || key === 46);

    if (type === 'numbers') {
        return numbers;
    }
    else if (type === 'letters') {
        return letters;
    }
    else if (type === 'numbers_letters') {
        return numbers || letters;
    }
    else if (type === 'letters_spaceless') {
        return letters_spaceless;
    }
    else if (type === 'letters_numbers_spaceless') {
        return letters_spaceless || numbers_spaceless;
    }
    else if (type === 'decimals') {
        return decimals;
    }
    else if (type === 'regex') {
        return regex;
    }
    return true;
}
function isNumber(n) {
    return !isNaN(parseFloat(n)) && isFinite(n);
}
function validate_decimals(el, evt) {
    var charCode = (evt.which) ? evt.which : event.keyCode;
    var number = el.val().split('.');

    if (charCode !== 46 && charCode > 31 && (charCode < 48 || charCode > 57)) {
        return false;
    }

    else if (number.length > 1 && charCode === 46) {
        return false;
    }

    else if(el.val().length === 0 && charCode === 46){
        return false;
    }

    return true;
}
function count_days(startdate, enddate) {
    if (startdate !== "" & enddate !== "") {
        var d1 = startdate.split("-");
        var dat1 = new Date(d1[0], d1[1], d1[2]);
        var d2 = enddate.split("-");
        var dat2 = new Date(d2[0], d2[1], d2[2]);
        if (d1 <= d2) {
            var difference = Math.floor((Date.parse(startdate) - Date.parse(enddate)) / 86400000);
            difference = difference < 0 ? difference * -1 : difference;
            return difference;
        }
    }
    return 0;
}
