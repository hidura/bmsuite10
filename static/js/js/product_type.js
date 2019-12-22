$(document).ready(function() {
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