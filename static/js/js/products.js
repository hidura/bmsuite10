$(document).ready(function() {
    // EDIT PRODUCT
    $(".edit_product").click(function () {
        var currentPruduct = $(this);
        var editProductModal = $("#edit_product");

        var callback = function(data, status){
            console.log(data);
            console.log(status);
            editProductModal.find("#item_name").val("Advil");
            editProductModal.find("#amount").val("12");
            editProductModal.find("#item_type").val("72").trigger("change");
            editProductModal.find("#product_cat").val("71").trigger("change");
        }

        sugelico.getServerCall({}, callback);

        var editProductCallback = function(data, status){
            var form = editProductModal.find("#edit_product_form");
            console.log(form.serialize());
        }

        $("#edit_product_btn").click(function(){
            sugelico.postServerCall({}, editProductCallback);
        });
    });

    $(".delete_product").click(function () {
        var currentUser = $(this);
        var deleteProductModal = $("#delete_product");

        var deleteProductCallback = function(data, status){
            console.log("eliminado");
        }

        $("#delete_product_btn").click(function(){
            deleteProductModal.modal("hide");
            var data = {
                "classname":"Users.Handle",
                "status":13, 
                code:14
            }
            sugelico.postServerCall(data, deleteProductCallback);
        });
    });

    // Filter by type and category
    $("#filter_product_report").click(function(event) {
        event.preventDefault();
        var data = {
            "product_type": $("#product_type").val(),
            "product_cat": $("#product_cat").val()
        }

        var callback = function(data, status){
            console.log(data);
        }

        sugelico.getServerCall(data, callback);

    });
});