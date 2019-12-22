
$(function () {
    $("#edit_contact_btn").click(function(event){
        event.preventDefault();
        $("#edit_contact_btn").prop( "disabled", true );

        var data = {
            "classname": "ManContact.Handle",
            "contact_name": $("#contact_name").val(),
            "lastname": $("#lastname").val(),
            "email": $("#contact_email").val(),
            "telephone": $("#contact_tel").val(),
            "_address": $("#contact_address").val(),
            "code":$(this).attr("data-id")
        }
        console.log(data);
        sugelico.postServerCall(data, function(data, status){
            console.log(data);
            if (JSON.parse(data).code) {
                window.location.reload();
            } else{
                $("#edit_contact_btn").prop( "disabled", false);
            }
        });

    });
    // GET ALL CONTACTS
    var getAllContactsCallback = function(data, status) {
        var currentTable;
        var editDeleteBtnTemplate = '<button action="edit" class="btn btn-success edit_contact left" data-id="\{id\}" data-toggle="modal" data-target="#edit_contact"><i class="glyphicon glyphicon-pencil"></i></button>' +
                                    '<button class="btn btn-default delete_contact" data-id="\{id\}" data-toggle="modal" data-target="#delete_contact"><i class="glyphicon glyphicon-remove"></i></button>';
        
        if ($('#contacts_table').val() == "") {
            currentTable = $('#contacts_table').DataTable();

            JSON.parse(data).reverse();

            JSON.parse(data).forEach(function(contact){
                currentTable.row.add([
                    contact.contact_name + " " + contact.lastname,
                    contact.email,
                    contact.telephone,
                    contact._address,
                    editDeleteBtnTemplate.replace("\{id\}", contact.code).replace("\{id\}", contact.code)
                ]).draw( false );
            });
            $("[data-id]").click(function (event) {
                if ($(this).attr("action")==="edit"){
                    editProduct(this);
                }
            });
        }
    };

    var data = {
        "classname": "ManContact.Get",
        "contact_name": ""
    };

    sugelico.getServerCall(data, getAllContactsCallback);

    // ADD CONTACT
    $("#add_contact").submit(function(event){
        event.preventDefault();
        $("#add_contact_btn").prop( "disabled", true );

        var data = {
            "classname": "ManContact.create",
            "contact_name": $("#contact_name").val(),
            "lastname": $("#lastname").val(),
            "email": $("#contact_email").val(),
            "telephone": $("#contact_tel").val(),
            "_address": $("#contact_address").val()
        }

        sugelico.postServerCall(data, function(data, status){
            console.log(data);
            if (JSON.parse(data).code) {
                window.location.reload();
            } else{
                $("#add_contact_btn").prop( "disabled", false);
            }
        });

    });

});