/**
 * Created by hidura on 8/6/2016.
 */
function create(target) {
    var frm=$(document.getElementById("formulary")).serializeObject();
    frm.classname="Types.create";
    frm.level=5;

    success=function (result,status,xhr) {
        console.log(result)
        $("#code").val(result.code);
        $("#status").prop("checked", true);
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);
}

function saveEquivalence(target) {
    var frm=$(document.getElementById("formulary")).serializeObject();
    if ($("#status").is(":checked")){
        frm.status=11;
    }else{
        frm.status=12;
    }

    frm.classname="Types.Handle";
    success=function (result,status,xhr) {
        document.getElementById("formulary").reset();
        $("#products_tbd").empty();

    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);
}

function findUnits(target) {
    msg="<div class='row' >" +

        "<div>" +
            "<div class='col-md-10'>" +
                "<table id='user_tbl' class='table table-striped table-bordered dataTable no-footer'>" +
                    "<thead>" +
                        "<tr>" +
                            "<th>Codigo</th>" +
                            "<th>Suplidor</th>" +
                            "<th>Estado</th>" +
                            "<th></th>" +
                        "</tr>" +
                    "</thead>" +
                    "<tbody id='user_tbd'></tbody>" +
                "</table>" +
            "</div>" +
        "</div>"+
    "</div>";
    buttons={

    };
    openDialog("Busqueda de Equivalencias", msg, buttons, "large");

    success=function (result,status,xhr) {
        if (target != null){
            $.each(result, function (index, field) {
                var tr = document.createElement("tr");
                $(tr).append($('<td />').val(field.code).html(field.code));
                $(tr).append($('<td />').html(field.tpname));
                $(tr).append($('<td />').html("<button " +
                    "class='btn btn-default' onClick='loadUnit(this);'><i class='fa fa-edit" +
                    "'></i></button>"));
                $("#user_tbd").append(tr);
            });
        }
    };
    error = function (xhr,status,error){
        console.log(error("error"));
    };
    serverCall("get", "/?classname=Types.Get&level=5",success, error);


}

function loadUnit(target) {
    var code = $(target).parent().parent().children()[0].textContent;
    success=function (result,status,xhr) {
        $("#code").val(result[0].code);
        $("#tpname").val(result[0].tpname);
        $(".bootbox-close-button").click();
        findEquivalences();
    };
    error = function (xhr,status,error){
        console.log(error("error"));
    };
    serverCall("get", "/?classname=Types.Get&code="+code,success, error);

}

function findEquivalences(target) {
    $("#products_tbd").empty();
    success=function (result,status,xhr) {
        $.each(result, function (index, field) {

            var tr = document.createElement("tr");
            $(tr).append($('<td />').val(field.code).html(field.code));
            $(tr).append($('<td />').html(field.name));
            $(tr).append($('<td />').html(field.tpname));
            $(tr).append($('<td />').html(field.operation));
            $(tr).append($('<td />').html(field.amount));
            $(tr).append($('<td />').html("<button " +
                "class='btn btn-danger' onClick='delEquivalence(this);'><i class='fa fa-trash-o" +
                "'></i></button>"));
            $("#products_tbd").append(tr);
        });

    };
    error = function (xhr,status,error){
        console.log(error("error"));
    };
    serverCall("get", "/?classname=General.getEquivalence&from_eq="+$("#code").val(),success, error);
}

function addEquivalence(target) {
    msg="<div class='row' >" +
                "<form id='addEquivalence_frm' class='form'>" +
                        "<div class='form-group'>" +
                            "<div class='col-md-5'>" +
                                "<label id='product_type_lbl'>Nombre</label>" +
                                "<input type='text' id='eq_name' name='eq_name' class='form-control' />" +
                            "</div>" +
                            "<div class='col-md-5'>" +
                                "<label id='product_type_lbl'>Unidad</label>" +
                                "<select id='units_eq' name='to_eq' class='form-control' >" +
                                    "<option value='0' readonly>---Seleccione---</option>"+
                                "</select>" +
                            "</div>" +
                        "</div>" +
                        "<div class='form-group'>" +
                            "<div class='col-md-5'>" +
                                "<label id='product_type_lbl'>Monto equivalente</label>" +
                                "<input id='amount' name='equivalence' class='form-control' type='number'/>" +
                            "</div>" +
                        "</div>" +
                "</form>" +
        "</div>";
    buttons={
            success:{
                label: "Salvar",
                className: "btn-success",
                callback: function () {
                    var frm=$(document.getElementById("addEquivalence_frm")).serializeObject();
                    //same equivalence that the recipe.
                    frm.classname="Accounting.addEquivalence";
                    frm.from_eq=$("#code").val();

                    success=function (result,status,xhr) {
                        findEquivalences();
                        $(".bootbox-close-button").click();
                    };
                    error = function (xhr,status,error){
                        console.log(error);
                    };
                    serverCall("post", frm,success, error, false);
                    return false;
                }
            }
    };
    openDialog("Agregar equivalencia", msg, buttons, "large");
    getTypes("#units_eq", 5);
}

function delEquivalence(target) {
    var code = $(target).parent().parent().children()[0].textContent;
    success=function (result,status,xhr) {
        $.each(result, function (index, field) {
            $(target).parent().parent().remove();
        });

    };
    error = function (xhr,status,error){
        console.log(error("error"));
    };
    serverCall("get", "/?classname=Accounting.delEquivalence&code="+code,success, error);
}