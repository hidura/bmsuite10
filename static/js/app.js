var types={};

var sugelico = {
    route:"/",
    type:types,
    postServerCall: function(data, callback, route) {
        if (route===undefined  || route===null){
            route="/";
        }
        $.ajax({
                url: route,
                data: JSON.stringify(data),
                contentType: "application/json",
                type: 'POST',
                success: callback
            }
        );
    },
    postSyncServerCall: function(data, callback) {
        $.ajax({
                url: sugelico.route,
                data:  JSON.stringify(data),
                contentType: "application/json",
                type: 'POST',
                success: callback
            }
        );
    },
    postFormServerCall: function(data, callback, route) {
        if (route===undefined){
            route="";
        }
        $.ajax({
                url: sugelico.route+route,
                data: data,
                processData: false,
                contentType: false,
                type: 'POST',
                success: callback
            }
        );
    },
    getServerCall: function(data, callback) {
        $.get(sugelico.route+"?", data, callback);
    },
    openDialog:function (title, message, buttons, classname, afterload){
            /*
            This function, receives the title, the message(can be html or string), and the buttons.
             */

            if (classname==undefined){
                    classname="medium"
                }
                bootbox.dialog({
                        title: title,
                        message: message,
                        buttons: buttons,
                        size: classname
                    }
                );
                if (afterload!==undefined){
                    afterload()
                }

        },
    getTypes:function(target, type) {
        success=function (result,status,xhr) {
            if (target != null){
                JSON.parse(result).forEach(function (field, index) {
                    $(target).append($('<option />').val(field.code).html(field.tpname));
                });

            }
            $(target).select2({
                    height: "40px"
            });
        };
        error = function (xhr,status,error){
            console.log(error);
        };
        sugelico.getServerCall("classname=Types.Get&level="+type,success, error);
    },
    activateTableWithDataTable: function(table_name, tableTitle, printableColumns){
        $(table_name).DataTable({
            "language": {
                "lengthMenu": "Mostrar _MENU_ registros por pagina",
                "zeroRecords": "No se encontraron registros. Verificar que el text esta bien escrito.",
                "info": "Mostrando pagina _PAGE_ of _PAGES_",
                "infoEmpty": "No hay registros disponibles.",
                "infoFiltered": "(De _MAX_ registros existentes.)",
                "search": "Buscar",
                "paginate": {
                    "first": "Primero",
                    "last": "Último",
                    "next": "Siguiente",
                    "previous": "Anterior"
                }
            },
            dom: 'B<"clear">lfrtip',
            buttons: {
                name: 'primary',
                buttons: [ 
                    'copy', 'csv', 'excel',
                    {
                        extend: 'pdf',
                        title: tableTitle,
                        text: 'PDF',
                        exportOptions: {
                            columns: printableColumns
                        }
                    },
                    {
                        extend: 'print',
                        title: tableTitle,
                        text: 'Print',
                        autoPrint: true,
                        exportOptions: {
                            columns: printableColumns
                        }
                    }
                ]
            }

        });
    },
    getCookie:function(cname)
{
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
},
    activateTableWithDataTableWithoutBtns: function(table_name){
        $(table_name).DataTable({
            "language": {
                "lengthMenu": "Mostrar _MENU_ por página",
                "zeroRecords": "No se encontraron registros. Verificar que el text está bien escrito.",
                "info": "Mostrando página _PAGE_ of _PAGES_",
                "infoEmpty": "No hay registros disponibles.",
                "infoFiltered": "(De _MAX_ registros existentes.)",
                "search": "Buscar",
                "paginate": {
                    "first": "Primero",
                    "last": "Último",
                    "next": "Siguiente",
                    "previous": "Anterior"
                }
            }
        });
    },
    addInputDateSupport: function(){
        $(".date").each(function(index, input){
            $(input).datepicker({
              dateFormat: "dd/mm/yy",
              altFormat: "dd/mm/yy"
            });
        });
    },
    webservices:{user_get:"login.Get"},
    numberWithCommas:function (x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
    numberWithOutCommas:function (x) {
        return x.toString().replace(",", "");
    },

    getParameterByName:function(name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(location.search);
        return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    },

    loadCategories:function(target, type) {
        var catype="";
        if (type!==undefined){
            catype+='&cat_type='+type;
        }
        $.ajax({
            url: '/?classname=Categories.Get'+catype,
            type: 'get',
            processData: false,
            contentType: false,
            success: function (data) {
                $(target).empty().append("<option value='0'>Seleccione uno</option>");

                JSON.parse(data).forEach(function(piece, index){
                    $(target).append($("<option/>").val(piece.code).html(piece.cat_name));
                });
            }
        });
    },
    getSelectedValue:function (select) {
            var result = {};
            var options = select && select.options;
            var opt;

            for (var i=0, iLen=options.length; i<iLen; i++) {
                opt = options[i];

                if (opt.selected) {
                    result[opt.value] = opt.text;
                }
            }
            return result;
    }
};

$(document).ready(function() {

    $("select").select2({
            height: "40px"
    });

    sugelico.activateTableWithDataTable("#users_table", "Sugelico - Listado de usuarios", [0,1,2,3]);
    sugelico.activateTableWithDataTable("#module_group_table", "Sugelico - Grupos de módulos", [0,1]);
    sugelico.activateTableWithDataTable("#modules_table", "Sugelico - Módulos", [0,1,2]);
	sugelico.activateTableWithDataTable("#contacts_table", "Sugelico - Listado de contactos", [0,1,2,3]);
    sugelico.activateTableWithDataTable("#products_table", "Sugelico - Listado de productos", [0,1,2,3]);
    sugelico.activateTableWithDataTable("#orders_table", "Sugelico - Orden de compra", [0,1,2,3,4,5]);
    sugelico.activateTableWithDataTable("#suppliers_table", "Sugelico - Listado de suplidores", [0,1,2,3]);
    sugelico.activateTableWithDataTable("#product_types_table", "Sugelico - Listado de tipo de productos", [0,1,2,3]);
    sugelico.activateTableWithDataTable("#category_types_table", "Sugelico - Listado de tipo de categorias", [0,1,2]);
    sugelico.activateTableWithDataTable("#printers_table", "Sugelico - Listado de tipo de categorias", [0,1,2,3,4,5]);
    sugelico.activateTableWithDataTable("#categories_table", "Sugelico - Listado de categorias", [0,1,2,3,4,5,6,7,8]);
    sugelico.activateTableWithDataTable("#areas_table", "Sugelico - Listado de areas", [0,1,2]);
    sugelico.activateTableWithDataTable("#units_table", "Sugelico - Listado de unidades", [0,1,2]);
    sugelico.activateTableWithDataTable("#cashflow_table", "Sugelico - Cashflow Report", [0,1,2,3,4,5,6]);
    sugelico.activateTableWithDataTable("#sales_rep_table", "Sugelico - Sales Report", [0,1,2]);
    sugelico.activateTableWithDataTable("#gen606_table", "Sugelico - 606 Report", [0,1,2]);
    sugelico.activateTableWithDataTable("#gen607_table", "Sugelico - 607 Report", [0,1,2]);

    sugelico.activateTableWithDataTableWithoutBtns("#products_by_category_table");
    sugelico.activateTableWithDataTableWithoutBtns("#products_by_category_table2");


    sugelico.addInputDateSupport();
    
});
