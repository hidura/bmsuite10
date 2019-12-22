$(document).ready(function() {
	// EDIT MODULE
    $(".edit_module").click(function () {
        var currentModule = $(this);
        var editModuleModal = $("#edit_module");

        var callback = function (data, status) {
            console.log(data);
            console.log(status);
            editModuleModal.find("#module_name").val("Ver productos");
            editModuleModal.find("#icon").val("icon-product-list");
            editModuleModal.find("#path").val("/?md=Something");
            editModuleModal.find("#user_type").val(["71", "72"]).trigger("change");
            editModuleModal.find("#groups").val(["75", "73"]).trigger("change");
        }

        sugelico.getServerCall({}, callback);

        var editModuleCallback = function(data, status){
            var form = editModuleGroupModal.find("#edit_module_form");
            console.log(form.serialize());
        }

        $("#edit_module_btn").click(function(){
            sugelico.postServerCall({}, editModuleCallback);
        });
    });


    $(".delete_module").click(function () {
        var currentUser = $(this);
        var deleteModuleModal = $("#delete_module");

        var deleteModuleCallback = function(data, status){
            console.log("eliminado");
        }

        $("#delete_module_btn").click(function(){
            deleteModuleModal.modal("hide");
            var data = {
                "classname":"Users.Handle",
                "status":13, 
                code:14
            }
            sugelico.postServerCall(data, deleteModuleCallback);
        });
    });
});