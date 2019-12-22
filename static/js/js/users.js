$(document).ready(function() {
    // Edit user
    $(".edit_user").click(function () {
        var currentUser = $(this);
        var editUserModal = $("#edit_user");

        var callback = function (data, status) {
            console.log(data);
            console.log(status);
            editUserModal.find("#user").val("Juan Perez");
            editUserModal.find("#emailaddress").val("juan.arias@gmail.com");
            editUserModal.find("#password").val("El_real");
            editUserModal.find("#repassword").val("El_real");
            editUserModal.find("#type").val("75").trigger("change");
            editUserModal.find("#waiter_code").val("092020");
        }

        sugelico.getServerCall({}, callback);

        var editUserCallback = function(data, status){
            var form = editUserModal.find("#edit_user_form");
            console.log(form.serialize());
        }

        $("#edit_user_btn").click(function(){
            var form = editUserModal.find("#edit_user_form");
            console.log(form.serialize());
            sugelico.postServerCall({}, editUserCallback);
        });
    });


    $(".delete_user").click(function () {
        var currentUser = $(this).data("id");
        var deleteUserModal = $("#delete_user");

        var deleteUserCallback = function(data, status){
            console.log("eliminado");
        }

        $("#delete_user_btn").click(function(){
            deleteUserModal.modal("hide");
            var data = {
                "classname":"Users.Handle",
                "status":13, 
                "code": currentUser
            }
            sugelico.postServerCall(data, deleteUserCallback);
        });
    });
});