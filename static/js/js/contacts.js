$(document).ready(function() {
	// EDIT CONTACT
    $(".edit_contact").click(function () {
        var currentContact = $(this);
        var editContactModal = $("#edit_contact");

        var callback = function(data, status){
    	    console.log(data);
            console.log(status);
            editContactModal.find("#contact_name").val("Juan Arias");
            editContactModal.find("#contact_email").val("jaun_el_real@dminio.com");
            editContactModal.find("#contact_tel").val("809-000-0000");
            editContactModal.find("#contact_address").val("Lejisimo");
        }

        sugelico.getServerCall({}, callback);

        var editContactCallback = function(data, status){
        	var form = editContactModal.find("#edit_contact_form");
            console.log(form.serialize());
        }

        $("#edit_contact_btn").click(function(){
            sugelico.postServerCall({}, editContactCallback);
        });
    });


    $(".delete_contact").click(function () {
        var currentUser = $(this);
        var deleteContactModal = $("#delete_contact");

        var deleteContactCallback = function(data, status){
            console.log("eliminado");
        }

        $("#delete_contact_btn").click(function(){
            deleteContactModal.modal("hide");
            var data = {
                "classname":"Users.Handle",
                "status":13, 
                code:14
            }
            sugelico.postServerCall(data, deleteContactCallback);
        });
    });
});