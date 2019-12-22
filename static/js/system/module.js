/**
 * Created by hidura on 5/8/2016.
 */
function create(target) {
    var params={};
    params.classname="login.addMenu";
    params.name=$("#module_name").val();
    params.icon=$("#icon").val();
    params.path=$("#path").val();
    
    success=function (result,status,xhr) {
        $("#code").val(result.code);
        $("#status").prop("checked", true);
        $("[name='user_type'] ").each(function (index, element) {
            if ($(element).is(":checked")){
                var params={};
                params.classname="login.addUserTypeMenu";
                params.type=$(element).val();
                params.module=$("#code").val();
                success=function (result,status,xhr) {
                    console.log(result);
                    $("input").val("");
                };
                error = function (xhr,status,error){
                    console.log(error);
                };
            
                serverCall("post", params,success, error, false);
                
            }
            
        })
    };

    error = function (xhr,status,error){
        console.log(error);
    };

    serverCall("post", params,success, error, false);


}

function findModule(target) {
    msg="<div class='row' >" +
            "<div class='col-md-6'>" +
                "<div class='form-group'>" +
                    "<label id='product_type_lbl'>Nombre del modulo</label>" +
                    "<div class='col-md-9'><input id='mdl_search' name='mdl_search' type='text' class='form-control' /></div>" +
                    "<div class='col-md-1'><button class='btn btn-info'><i class='fa fa-search' onClick='loadModule(this);'></i></button></div>" +
                "</div>" +
            "</div>" +
            "<div class='col-md-10'>" +
                "<table id='module_tbl' class='table table-striped table-bordered dataTable no-footer'>" +
                    "<thead>" +
                        "<tr>" +
                            "<th>Codigo</th>" +
                            "<th>Nombre de Modulo</th>" +
                            "<th>Icono</th>" +
                            "<th></th>" +
                        "</tr>" +
                    "</thead>" +
                    "<tbody id='module_tbd'></tbody>" +
                "</table>" +
            "</div>" +
        "</div>";
    buttons={
        
    };
    openDialog("Busqueda de modulos", msg, buttons, "large");

    loadModule();
}

function loadModule(target) {
    success=function (result,status,xhr) {
        $("#module_tbd").empty();
        $.each(result, function (index, fields) {
            tr = document.createElement("tr");
            $(tr).append($("<td />").val(fields.code).html(fields.code));
            $(tr).append($("<td />").val(fields.name).html(fields.name));
            $(tr).append($("<td />").val(fields.icon).html(fields.icon));
            $(tr).append($("<td><button class='btn btn-info' onClick='loadModuleData(this);'><i class='fa fa-info'></i></button></td>"));
            $("#module_tbd").append(tr);
        });
        loadTable($("#module_tbl"));
    };

    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", "/?classname=login.getModules&name="+$("#mdl_search").val(),success, error, false);
}

function loadModuleData(target) {
    // var code =$(target).parent().parent().textContent;
    // success=function (result,status,xhr) {
    //     $("#module_tbd").empty();
    //     $.each(result, function (index, fields) {
    //         $("#code").val(fields.code);
    //         $("#module_name").val(fields.name);
    //         $("#icon").val(fields.icon);
    //         tr = document.createElement("tr");
    //         $(tr).append($("<td />").val(fields.code).html(fields.code));
    //         $(tr).append($("<td />").val(fields.name).html(fields.name));
    //         $(tr).append($("<td />").val(fields.icon).html(fields.icon));
    //         $(tr).append($("<td><button class='btn btn-info' onClick='loadModuleData(this);'><i class='fa fa-info'></i></button></td>"));
    //         $("#module_tbd").append(tr);
    //     });
    //     loadTable($("#module_tbl"));
    // };
    //
    // error = function (xhr,status,error){
    //     console.log(error);
    // };
    // serverCall("get", "/?classname=login.getModules&code="+code,success, error, false);
}