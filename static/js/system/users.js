/**
 * Created by hidura on 5/7/2016.
 */
function create(target) {
    var params={};
    params.classname="login.create";

    success=function (result,status,xhr) {
        $("#code").val(result.code);
        $("#status").prop("checked", true);
    };

    error = function (xhr,status,error){
        console.log(error);
    };

    serverCall("post", params,success, error, false);

}
function saveInfo() {
    var params={};
    params.classname="login.Handle";
    params.username=$("#emailaddress").val();
    params.contact=$("#contact").val();

    if ($("#password").val().toString()!=$("#reppassword").val().toString()){
        bootbox.alert("Contraseñas distintas");
    }else{
        if($("#password").val().toString().length>0){
            params.passwd = $("#password").val();
        }
    }    
    params.usrtype=$("#type").val();
    params.code=$("#code").val();
    if ($("#waiter_code").val().toString().length>0){
        params.waiter_code = $("#waiter_code").val().toString();
    }
    success=function (result,status,xhr) {
        //Clean the fields
        $("input").val("");
        $('select option:first-child').attr("selected", "selected");
        $('input :checked').prop("checked", false);
    };

    error = function (xhr,status,error){
        console.log(error);
    };

    serverCall("post", params,success, error, false);
}

function openContact(target) {
   success=function (result,status,xhr) {
       buttons={};
       openDialog("Manejador de contactos", result,buttons, "large");
       var contact =$("#contact").val().toString();
       if (contact.length>0){
           findContact(contact)
       }
       $("#createCon").click(function () {
            createCon(this);
        });
    };

    error = function (xhr,status,error){
        console.log(error);
    };

    serverCall("get", "/resources/site/contact.html",success, error, false); 
}

function searchUser(target) {
    msg="<div class='row' >" +
            "<div class='col-md-6'>" +
                "<div class='form-group'>" +
                    "<label id='product_type_lbl'>Nombre de usuario</label>" +
                    "<div class='col-md-9'><input id='username_search' name='username_search' type='text' class='form-control' /></div>" +
                    "<div class='col-md-1'><button class='btn btn-info'><i class='fa fa-search' onClick='loadUsers(this);'></i></button></div>" +
                "</div>" +
            "</div>" +
            "<div class='col-md-10'>" +
                "<table id='user_tbl' class='table table-striped table-bordered dataTable no-footer'>" +
                    "<thead>" +
                        "<tr>" +
                            "<th>Codigo</th>" +
                            "<th>Nombre de usuario</th>" +
                            "<th>Tipo</th>" +
                            "<th></th>" +
                        "</tr>" +
                    "</thead>" +
                    "<tbody id='user_tbd'></tbody>" +
                "</table>" +
            "</div>" +
            "<div class='col-md-10' style='text-align: right'>" +
                "<button class='btn btn-danger' onClick='cancelEdit(this);'><i class='fa fa-sign-out'></i> Cerrar</button>" +
            "</div>" +
        "</div>";
    buttons={

    };
    openDialog("Busqueda de usuario", msg, buttons, "large");
    
    loadUsers();
}

function loadUsers(target) {
    success=function (result,status,xhr) {
        $("#user_tbd").empty();
        $.each(result, function (index, fields) {
            tr = document.createElement("tr");
            $(tr).append($("<td />").val(fields.code).html(fields.code));
            $(tr).append($("<td />").val(fields.username).html(fields.username));
            $(tr).append($("<td />").val(fields.tpname).html(fields.tpname));
            $(tr).append($("<td><button class='btn btn-info' onClick='loadUserData(this);'><i class='fa fa-info'></i></button></td>"));
            $("#user_tbd").append(tr);
        });
        loadTable($("#user_tbl"));
    };
    
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", "/?classname=login.Get&username="+$("#username_search").val(),success, error, false);
}

function loadUserData(target) {
    var code = $(target).parent().parent().children()[0].textContent;
    success=function (result,status,xhr) {
        $.each(result, function (index, fields) {
            $("#code").val(fields.code);
            $("#contact").val(fields.contact);
            $("#type").val(fields.usrtype);
            $("#emailaddress").val(fields.username);

            $("#status").prop("checked", false);
            if (fields.status==11){
                $("#status").prop("checked", true);
            }
        });
        $(".bootbox-close-button").click();
    };

    error = function (xhr,status,error){
        console.log(error);
    };

    serverCall("get", "/?classname=login.Get&code="+code,success, error, false);
}