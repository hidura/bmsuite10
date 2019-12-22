$(document).ready(function() {
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