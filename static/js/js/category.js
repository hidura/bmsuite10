$(document).ready(function() {
    // EDIT categoryS
    $(".edit_category").click(function () {
        var currentCategory = $(this);
        var editCategoryModal = $("#edit_category");

        var callback = function(data, status){
            console.log(data);
            console.log(status);
            editCategoryModal.find("#code").val("category 1");
            editCategoryModal.find("#name").val("CJSK-23a32-DD");
            editCategoryModal.find("#printer").val("Printer 1");
            editCategoryModal.find("#printer_path").val("72.wd.23.2323");
            editCategoryModal.find("#status").val("Activa");
            editCategoryModal.find("#time").val("2").trigger("change");
            editCategoryModal.find("#type").val("1").trigger("change");
            editCategoryModal.find("#product_type").val("0").trigger("change");
        }

        sugelico.getServerCall({}, callback);

        var editCategoryCallback = function(data, status){
            var form = editCategoryModal.find("#edit_category_form");
            console.log(form.serialize());
        }

        $("#edit_category_btn").click(function(){
            sugelico.postServerCall({}, editCategoryCallback);
        });
    });

    $(".delete_category").click(function () {
        var currentCategory = $(this).data("id");
        var deletecategoryModal = $("#delete_category");

        var deleteCategoryCallback = function(data, status){
            console.log("eliminado");
        }

        $("#delete_category_btn").click(function(){
            deletecategoryModal.modal("hide");
            var data = {
                "classname":"Users.Handle",
                "status":13, 
                code:14
            }
            sugelico.postServerCall(data, deleteCategoryCallback);
        });
    });
});