/**
 * Created by hidura on 8/26/2016.
 */
function loadPreparation() {
    var merma = getParameterByName("merma");
    if (merma.toString().length>0){
        console.log(merma);
    }
    success=function (result,status,xhr) {

        $("#sign_madeby").html(result.name);
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", "/?classname=login.getProfile",success, error, false);
}

function create(target) {
    var frm=$(document.getElementById("formulary")).serializeObject();
    frm.classname="Bills.create_preparation";

    success=function (result,status,xhr) {
        console.log(result);
        $("#code").val(result.code);
        $("#status").prop("checked", true);
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);
}


function savePrep(target) {
    var frm=$(document.getElementById("formulary")).serializeObject();
    if ($("#status").is(":checked")){
        frm.status=11;
    }else{
        frm.status=12;
    }

    frm.classname="Bills.prep_Handle";
    success=function (result,status,xhr) {
        console.log(result);
        document.getElementById("formulary").reset();
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);

}


function openPreparation(target) {
    var table="" +
        "<div class='row'>" +
            "<div class='col-md-5'>	" +
                "<div class='col-lg-9'>" +
                    "<span class='control-label' id='input_lbl'>Insumo</span>" +
                    "<select id='input_sel' name='input_sel' style='width:100%' class='form-control'>" +
                    ""+
                    "</select>" +
                "</div>" +
            "</div>" +
            "<div class='form-group col-md-3'>" +
                "<div class='form-group'>" +
                    "<span class='control-label' id='amount_lbl'>Cantidad</span>" +
                    "<input type='number' id='ins_amount' name='amount' class='form-control'/>" +
                "</div>" +
            "</div>" +
            "<div class='form-group col-md-3'>" +
                "<span class='control-label' id='amount_lbl'>Servicios</span>" +
                "<input type='number' id='ins_services' name='services' class='form-control'/>" +
            "</div>" +
            "<div class='col-md-1'><br/>" +
                    "<button class='btn btn-primary' onClick='savePreparation(this); return false;'>" +
                        "<i class='fa fa-save'></i>" +
                    "</button>" +
                "</div>" +
            "<div class='col-md-10'>" +
                "<table class='table table-responsive'>" +
                    "<thead>" +
                        "<tr>" +

                            "<th>Codigo</th>" +
                            "<th>Nombre</th>" +
                            "<th>Cantidad</th>" +
                            "<th>Servicios</th>" +
                        "</tr>" +
                    "</thead>" +
                    "<tbody id='recipe_items'></tbody>"+
                "</table>" +

            "</div>" +
        "</div>";
    buttons={

    };
    openDialog("Crear Receta", table, buttons, "large");
    $("#input_sel").select2();
    getTypes($("#unit"),5);
    loadProducts();
    loadPrepProducts();
}

function savePreparation(target) {
    if (parseInt($("#code"))==0){
        var frm={};
        frm.classname="Bills.prepProduct";
        frm.product = $("#input_sel").val();
        frm.amount = $("#ins_amount").val();
        frm.services=$("#ins_services").val();
        frm.description="";
        success=function (result,status,xhr) {
            loadPrepProducts();
        };
        error = function (xhr,status,error){
            console.log(error);
        };
        serverCall("post", frm,success, error, false);
    }

}

function loadPrepProducts() {
    var frm={};
    frm.classname="Bills.prepProduct";
    frm.description="";
    success=function (result,status,xhr) {
        console.log(result);
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);
}