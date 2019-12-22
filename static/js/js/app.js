var sugelico = {
        postServerCall: function(data, callback, url) {
            $.post(data.path, data, callback);
        },
        getServerCall: function(data, callback) {
            $.get("https://api.themoviedb.org/3/movie/now_playing?api_key=2e3b7da57fde28d9090394f6a2f0cd56&page=1", data, callback);
        },
    numberWithCommas:function (x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
        activateTableWithDataTable: function(table_name, tableTitle, printableColumns){
            $(table_name).DataTable({
                "language": {
                    "lengthMenu": "Mostrar _MENU_ registros por página",
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
        }
    }

$(document).ready(function() {

    $("select").select2();

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
    
    
});
