$(document).ready(function() {


    // GET ALL PRODUCT TYPES
    var data = {
        "classname": "Types.Get",
        "level": 4
    }

    sugelico.getServerCall(data, function(data, status){
        var currentTable;
        var editDeleteBtnTemplate = '<button class="btn btn-success edit_product_type left" data-id="\{id\}" ' +
            'data-toggle="modal" data-target="#edit_product_type"><i class="fa fa-pencil"></i></button>' +
                                    '<button class="btn btn-default delete_product_type" data-id="\{id\}" ' +
            'data-toggle="modal" data-target="#delete_product_type"><i class="fa fa-trash"></i></button>';
        
        if ($('#product_types_table').val() == "") {
            currentTable = $('#product_types_table').DataTable();

            JSON.parse(data).forEach(function(product_type){
                currentTable.row.add([
                    product_type.code,
                    product_type.tpname,
                    editDeleteBtnTemplate.replace("\{id\}", product_type.code).replace("\{id\}", product_type.code)
                ]).draw( false );
            });
        }
    });



    // EDIT PRODUCT TYPE
    $(".edit_product_type").click(function () {
        var currentPruductType = $(this);
        var editProductTypeModal = $("#edit_product_type");

        var callback = function(data, status){
            console.log(data);
            console.log(status);
            editProductTypeModal.find("#name").val("Printer 1");
            editProductTypeModal.find("#code").val("CJSK-23a32-DD");
            editProductTypeModal.find("#status").val("Activa");
            editProductTypeModal.find("#printer_path").val("72").trigger("change");
        }

        sugelico.getServerCall({}, callback);

        var editProductTypeCallback = function(data, status){
            var form = editProductTypeModal.find("#edit_product_type_form");
            console.log(form.serialize());
        }

        $("#edit_product_type_btn").click(function(){
            sugelico.postServerCall({}, editProductCallback);
        });
    });

    $(".delete_product_type").click(function () {
        var currentPruductType = $(this);
        var deleteProductTypeModal = $("#delete_product_type");

        var deleteProductCallback = function(data, status){
            console.log("eliminado");
        }

        $("#delete_product_type_btn").click(function(){
            deleteProductTypeModal.modal("hide");
            var data = {
                "classname":"Users.Handle",
                "status":13, 
                code:14
            }
            sugelico.postServerCall(data, deleteProductCallback);
        });
    });
});