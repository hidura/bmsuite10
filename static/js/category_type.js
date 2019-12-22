$(document).ready(function() {



    // GET ALL CATEGORIES TYPES
    if ($('#category_types_table').val() == "") {
        var data = {
            "classname": "Types.Get",
            "level": 6
        }

        sugelico.getServerCall(data, function(data, status){
            var currentTable;
            var editDeleteBtnTemplate = '<button class="btn btn-success edit_category_type left" data-id="\{id\}" data-toggle="modal" data-target="#edit_category_type"><i class="glyphicon glyphicon-pencil"></i></button>' +
                                        '<button class="btn btn-default delete_category_type" data-id="\{id\}" data-toggle="modal" data-target="#delete_category_type"><i class="glyphicon glyphicon-remove"></i></button>';
            
            if ($('#category_types_table').val() == "") {
                currentTable = $('#category_types_table').DataTable();

                JSON.parse(data).forEach(function(category_type){
                    currentTable.row.add([
                        category_type.code,
                        category_type.tpname,
                        editDeleteBtnTemplate.replace("\{id\}", category_type.code).replace("\{id\}", category_type.code)
                    ]).draw( false );
                });
            }
        });
    }


    // ADD NEW CATEGORY
    $("#add_category_type").submit(function(event){
        event.preventDefault();

        var data = {
            "classname": "Types.create",
            "level": 6,
            "status": $("#status").val() || 11,
            "tpname": $("#name").val()
        }

        sugelico.postServerCall(data, function(data, status){
            if (JSON.parse(data).code) {
                window.location.reload();
            } else {
                $("#error_alert").toggle();
            }
        });

    });

    // EDIT Category TYPE
    $(".edit_category_type").click(function () {
        var currentPruductType = $(this);
        var editCategoryTypeModal = $("#edit_category_type");

        var callback = function(data, status){
            console.log(data);
            console.log(status);
            editCategoryTypeModal.find("#name").val("Printer 1");
            editCategoryTypeModal.find("#code").val("CJSK-23a32-DD");
            editCategoryTypeModal.find("#status").val("Activa");
            editCategoryTypeModal.find("#printer_path").val("72").trigger("change");
        }

        sugelico.getServerCall({}, callback);

        var editCategoryTypeCallback = function(data, status){
            var form = editCategoryTypeModal.find("#edit_category_type_form");
            console.log(form.serialize());
        }

        $("#edit_category_type_btn").click(function(){
            sugelico.postServerCall({}, editCategoryTypeCallback);
        });
    });

    $(".delete_category_type").click(function () {
        var currentPruductType = $(this);
        var deleteCategoryTypeModal = $("#delete_category_type");

        var deleteCategoryCallback = function(data, status){
            console.log("eliminado");
        }

        $("#delete_category_type_btn").click(function(){
            deleteCategoryTypeModal.modal("hide");
            var data = {
                "classname":"Users.Handle",
                "status":13, 
                code:14
            }
            sugelico.postServerCall(data, deleteCategoryCallback);
        });
    });
});