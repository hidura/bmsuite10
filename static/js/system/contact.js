/**
 * Created by hidura on 5/7/2016.
 */
function createCon(target) {
    var params={};
    params.classname="ManContact.create";

    success=function (result,status,xhr) {
        $("#con_code").val(result.code);
        $("#con_status").prop("checked", true);
        $("#contact").val(result.code);
        
    };

    error = function (xhr,status,error){
        console.log(error);
    };

    serverCall("post", params,success, error, false);

}

function saveCon(target) {
    var params={};
    params.classname="ManContact.Handle";
    params.code=$("#con_code").val();
    params.contact_name=$("#firstname").val();
    params.lastname=$("#lastname").val();
    params.email=$("#emailaddress").val();
    params.telephone=$("#telephone").val();
    params.cellphone=$("#cellphone").val();
    params.address=$("#address").val();
    params.country=$("#country").val();
    params.birthdate =$("#birthdate").val();
    params.idDocument=$("#document").val();
    params.doc_type=$("#doc_type").val();
    params.status=12;
    if ($("#con_status").is(":checked")){
        params.status=11;
    }
    
    success=function (result,status,xhr) {
        //Clean the fields
        $("#contact").val($("#con_code").val());
        $(".bootbox-close-button").click();
    };

    error = function (xhr,status,error){
        console.log(error);
    };

    serverCall("post", params,success, error, false);
}

function load_findContact(target) {

    $("#contact_div").slideUp("fast");
    $("#contactLst").slideDown("fast");

}

function cancelEdit(target) {
    $("#contact_div").slideDown("fast");
    $("#contactLst").slideUp("fast");

}
function search() {
    success=function (result,status,xhr) {
        //Clean the fields
        $.each(result, function (index, field) {
            var tr=document.createElement("tr");
            $(tr).append($("<td />").val(field.code).html(field.code));
            $(tr).append($("<td />").val(field.code).html(field.contact_name));
            $(tr).append($("<td />").val(field.code).html(field.lastname));
            $(tr).append($("<td />").append("<button class='btn btn-info' onClick='loadContact(this);'><i class='fa fa-info'></i></button>"));
            $("#contact_tbd").append(tr);
            
        });
        loadTable($("#contact_tbl"));
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", "/?classname=ManContact.Get&contact_name="+$("#conName").val(),success, error, false);
}

function findContact(code) {
    success=function (result,status,xhr) {
        //Clean the fields
        $.each(result, function (index, field) {
            $("#con_code").val(field.code);
            $("#contact").val(field.code);
            $("#firstname").val(field.contact_name);
            $("#lastname").val(field.lastname);
            $("#emailaddress").val(field.email);
            $("#telephone").val(field.telephone);
            $("#cellphone").val(field.cellphone);
            $("#address").val(field.address);
            $("#country").val(field.country);
            $("#birthdate").val(field.birthdate.split(" ")[0]);
            $("#document").val(field.document_id);
            $("#doc_type").val(field.doc_type);
            $("#con_status").prop("checked", false);
            if (field.status){
                $("#con_status").prop("checked", true);
            }
            cancelEdit();
        });
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    var params="/?classname=ManContact.Get&code="+code;

    serverCall("get", params,success, error, false);
}

function loadContact(target) {
    findContact($(target).parent().parent().children()[0].textContent);
    
}