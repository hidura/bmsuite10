$(document).ready(function() {
	// EDIT MODULE GROUP
    $(".edit_module_group").click(function () {
        var currentModuleGroup = $(this);
        var editModuleGroupModal = $("#edit_module_group");

        var callback = function (data, status) {
            console.log(data);
            console.log(status);
            editModuleGroupModal.find("#module_group_name").val("JProductos");
        }

        sugelico.getServerCall({}, callback);

		var editModuleGroupCallback = function(data, status){
            var form = editModuleGroupModal.find("#edit_user_form");
            console.log(form.serialize());
        }

        $("#edit_module_group_btn").click(function(){
            sugelico.postServerCall({}, editModuleGroupCallback);
        });
    });

    $(".delete_module_group").click(function () {
        var currentUser = $(this);
        var deleteModuleGroupModal = $("#delete_module_group");

        var deleteModuleGroupCallback = function(data, status){
            console.log("eliminado");
        }

        $("#delete_module_group_btn").click(function(){
            deleteModuleGroupModal.modal("hide");
            var data = {
                "classname":"Users.Handle",
                "status":13, 
                code:14
            }
            sugelico.postServerCall(data, deleteModuleGroupCallback);
        });
    });
});