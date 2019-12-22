$(function () {

    // GET ALL AREAS
    var getAllAreasCallback = function(data, status) {
        var currentTable;
        var editDeleteBtnTemplate = '<button class="btn btn-success edit_area left" data-id="\{id\}" ' +
            'data-toggle="modal" data-target="#edit_area"><i class="fa fa-pencil"></i></button>' +
                                    '<button class="btn btn-default delete_area" data-id="\{id\}" data-toggle="modal" ' +
            'data-target="#delete_delete"><i class="fa fa-trash"></i></button>';
        
        if ($('#areas_table').val() == "") {
            currentTable = $('#areas_table').DataTable();
        }

        JSON.parse(data).forEach(function(area){
            currentTable.row.add([
                area.area_name,
                area.description,
                area.status_name,
                editDeleteBtnTemplate.replace("\{id\}", area.code).replace("\{id\}", area.code)
            ]).draw( false );
        });

        // $('#modules_table tbody').on('click', 'button.edit_module', function () {
        //     editModuleBtnClicked($(this));
        // });

        // $('#modules_table tbody').on('click', 'button.delete_module', function () {
        //     deleteModuleBtnClicked($(this));
        // } );
    }

    var data = {
        "classname": "TableArea.Get",
        "area_name": ""
    }

    sugelico.getServerCall(data, getAllAreasCallback);
});