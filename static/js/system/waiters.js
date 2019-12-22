/**
 * Created by diegohidalgo on 11/28/16.
 */
function add(target){
    var frm=$(document.getElementById("formulary")).serializeObject();
    frm.classname="TableArea.create";

    success=function (result,status,xhr) {
        $("#code").val(result.code);
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);

}
//Save Area
function saveArea(target) {
    var params={};
    params.classname="TableArea.setUserArea";
    params.usercode=$("#waiter").val();
    params.area=$(target).val();
    success=function (result,status,xhr) {
        alert("Usuario enlazado!");
        $(target).prop("selected",true);
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", params,success, error, false);
}

//Load all areas.
function loadUsers() {
    var params={};
    params.classname="login.getUsersBy";
    params.usrtype=73;
    success=function (result,status,xhr) {

        console.log(result);
        $("#waiter").empty();
        $.each(result, function (index, field) {
            var option = document.createElement("option");
            $(option).val(field.code).html(field.name);
            $("#waiter").append(option)
        })
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", params,success, error, false);
}
//Edif area
function edit(target){
    //Calling the loadByCode function
    loadByCode($(target).parent().parent().children()[0].textContent);//Sending the id of the area.
}

//Load By Code
function loadByCode(code){
    if (code!=undefined && code!=null){
        var params={};
        params.classname="TableArea.Get";
        params.code=code;
        success=function (result,status,xhr) {
            $.each(result, function (index, field) {
                $("#code").val(field.code);
                $("#area_name").val(field.area_name);
                $("#description").val(field.description);
                $("#status").prop("checked", false);
                if (field.status==11){
                    $("#status").prop("checked", true);

                }

            });

        };
        error = function (xhr,status,error){
            console.log(error);
        };
        serverCall("post", params,success, error, false);
    }

}
//Default
function setByDefault() {
    code = getParameterByName("code");
    console.log(code);
    if (code!=null){
        loadByCode(code);
    }
}