$(document).ready(function() { 
	// EDIT SUPPLIER
    $(".edit_supplier").click(function () {
        var currentSupplierGroup = $(this);
        var editSupplierModal = $("#edit_supplier");

        var callback = function(data, status){
        	console.log(data);
            console.log(status);
            editSupplierModal.find("#supplier_name").val("Juan Arias");
            editSupplierModal.find("#supplier_email").val("jaun_el_real@dminio.com");
            editSupplierModal.find("#supplier_tel").val("809-000-0000");
            editSupplierModal.find("#supplier_address").val("Lejisimo");
        }

        sugelico.getServerCall({}, callback);

        var editSupplierCallback = function(data, status){
			var form = editSupplierModal.find("#edit_supplier_form");
            console.log(form.serialize());
        }

        $("#edit_supplier_btn").click(function(){
            sugelico.postServerCall({}, editSupplierCallback);
        });
    });

    $(".delete_supplier").click(function () {
        var currentUser = $(this);
        var deleteSupplierModal = $("#delete_supplier");

        var deleteSupplierCallback = function(data, status){
            console.log("eliminado");
        }

        $("#delete_supplier_btn").click(function(){
            deleteSupplierModal.modal("hide");
            var data = {
                "classname":"Users.Handle",
                "status":13, 
                code:14
            }
            sugelico.postServerCall(data, deleteSupplierCallback);
        });
    });
});