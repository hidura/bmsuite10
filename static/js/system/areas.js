
/**
 * Created by hidura on 4/28/2016.
 */
//Create newArea
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
function save(target) {
    var params=$(document.getElementById("formulary")).serializeObject();
    params.classname="TableArea.Handle";
    success=function (result,status,xhr) {
        loadTable();
        document.getElementById("formulary").reset();
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", params,success, error, false);
}

//Load all areas.
function loadTable() {
    var params={};
    params.classname="TableArea.Get";
    params.area_name="";
    success=function (result,status,xhr) {
        $("#areas_tbl").empty();
        $.each(result, function (index, field) {
            tr = document.createElement("tr");
            $(tr).append($('<td />').val(field.code).html(field.code));
            $(tr).append($('<td />').val(field.area_name).html(field.area_name));
            $(tr).append($('<td />').val(field.code).html(field.description));
            $(tr).append($('<td />').val(field.status).html(field.status_name));
            $(tr).append($('<td />').html("<button onClick='edit(this);' class='btn btn-info'><i class='fa fa-edit'></i></button>"));
            $("#areas_tbl").append(tr)
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