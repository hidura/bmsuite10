/**
 * Created by hidura on 8/5/2016.
 */
function loadMerma() {
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
    frm.classname="Accounting.create_merma";

    success=function (result,status,xhr) {
        $("#code").val(result.code);
        $("#status").prop("checked", true);
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);
}


function saveMerma(target) {
    var frm=$(document.getElementById("formulary")).serializeObject();
    if ($("#status").is(":checked")){
        frm.status=11;
    }else{
        frm.status=12;
    }

    frm.classname="Accounting.merma_Handle";
    success=function (result,status,xhr) {
        console.log(result);
        document.getElementById("formulary").reset();
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);

}

function openBill(target) {
        msg="<div class='row' >" +
                "<form id='bill_fnd' class='form'>" +
                        "<div class='form-group'>" +
                            "<div class='col-md-5'>" +
                                "<label id='product_type_lbl'>Suplidor</label>" +
                                "<select id='supplier_search' name='supplier' class='form-control' >" +
                                    "<option value='0' readonly>---Seleccione---</option>"+
                                "</select>" +
                            "</div>" +
                            "<div class='col-md-5'>" +
                                "<label id='product_type_lbl'>Factura</label>" +
                                "<select id='bill' name='bill' class='form-control' >" +
                                    "<option value='0' readonly>---Seleccione---</option>"+
                                "</select>" +
                            "</div>" +
                        "</div>" +
                        "<div class='form-group'>" +
                            "<div class='col-md-5'>" +
                                "<label id='product_type_lbl'>Desde</label>" +
                                "<input id='from' name='from' class='form-control' type='date'/>" +
                            "</div>" +
                            "<div class='col-md-5'>" +
                                "<label id='product_type_lbl'>Hasta</label>" +
                                "<input id='to' name='to' class='form-control' type='date'/>" +
                            "</div>" +
                        "</div>" +
                "</form>" +

                "<div class='form-group'>" +
                    "<div class='col-md-1'><br/><button class='btn btn-info'><i class='fa fa-search' " +
            "onClick='loadBills(this); return false;'></i></button></div>" +
                "</div>"+
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
    openDialog("Busqueda de facturas", msg, buttons, "large");

    getSupplier($("#supplier_search"));
    loadBills();


}

function loadBills(target) {
    var frm=$(document.getElementById("bill_fnd")).serializeObject();
    frm.classname="Accounting.Get";

    success=function (result,status,xhr) {
        console.log(result);
        $.each(result, function (index, field) {
            var tr = document.createElement("tr");
            var btn="<button class='btn btn-info' bill='"+field.code+"' onClick='loadBillInfo(this);'><i class='fa fa-edit'></i></button>";
            $(tr).append($("<td />").val(field.code).html(field.code));
            $(tr).append($("<td />").val(field.sup_name).html(field.sup_name));
            $(tr).append($("<td />").val(field.total).html(field.total));
            $(tr).append($("<td />").val(field.status).html(field.status));
            $(tr).append(btn);
            $("#user_tbd").append(tr);
        });
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);

}
function loadBillInfo(target) {
    var frm={};
    frm.classname="Accounting.Get";
    frm.code=$(target).attr("bill");

    success=function (result,status,xhr) {
        $.each(result, function (index, field) {
            $("#code").val(field.code);
            $("#supplier").val(field.supplier);
            $("#subtotal").val(field.subtotal);
            $("#description").val(field.description);
            $("#status").prop("selected", false);
            if (field.status==11){
                $("#status").prop("selected", true);
            }
            $("#total").val(field.total);
            $("#other_costs").val(field.other_costs);
            $("#discount").val(field.discount);
            $("#total_tax").val(field.total_tax);
            $("#ncf").val(field.ncf);
            $("#paytype").val(field.paytype);
            $("#date").val(field.generated.split(" ")[0]);
            $("#expiration").val(field.expires.split(" ")[0]);
            $("#payalert").val(field.payalert.split(" ")[0]);
            $(".bootbox-close-button").click();

        });
        var frm={};
        frm.classname="Accounting.getItem2Bill";
        frm.bill=$(target).attr("bill");
        success=function (result,status,xhr) {
          $.each(result, function (index, field) {
              var tr = document.createElement("tr");
              $(tr).append($("<td>").html(field.item_name));
              $(tr).append($("<td>").html(field.amount));
              $(tr).append($("<td>").html((field.total-field.tax)));
              $(tr).append($("<td>").html(field.tax));
              $(tr).append($("<td>").html(field.total));
              $("#products_tbd").append(tr);
          })
        };
        error = function (xhr,status,error){
            console.log(error);
        };
        serverCall("post", frm,success, error, false);
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);
}
function addItems(target) {
    success=function (result,status,xhr) {
        buttons={
            success:{
                label: "Salvar",
                className: "btn-success",
                callback: function () {
                    var frm=$(document.getElementById("addItem_frm")).serializeObject();
                    //same equivalence that the recipe.
                    frm.classname="Accounting.merma_addProd";
                    frm.code=$("#code").val();
                    frm.unit=$("#equivalence").attr("unit");

                    success=function (result,status,xhr) {
                        console.log(result);
                        var tr = document.createElement("tr");
                        var product = $("#product").val();
                        $(tr).append(($("<td>").html(result.code)));

                        $(tr).append($("<td>").html($("#product option[value='"+product+"']").text()));
                        $(tr).append(($("<td>").html($("#amount").val())));
                        $(tr).append(($("<td>").html($("#subtotal_item").val())));
                        $(tr).append(($("<td>").html($("#tax_item").val())));
                        $(tr).append(($("<td>").html($("#total_item").val())));

                        $("#products_tbd").append(tr)
                        document.getElementById("addItem_frm").reset();
                    };
                    error = function (xhr,status,error){
                        console.log(error);
                    };
                    serverCall("post", frm,success, error, false);
                    return false;
                }
            }
        };
        openDialog("Productos en la factura.", result, buttons, "large");
        $("#subtotal_item").attr("readonly", "true");
        $("#tax_item").attr("readonly", "true");
        $("#other_costs_item").attr("readonly", "true");
        $("#discount_item").attr("readonly", "true");
        $("#total_item").attr("readonly", "true");
        $("#cur_amount_div").slideDown("fast");
        getTypes($("#doc_type")[0], 9);

        url=new connection().url+"?classname=Items.Get&wrap_to=select2";
        var select = $("#product");
        select.parents('.bootbox').removeAttr('tabindex');
        select.select2({
                placeholder: "Colocar nombre del producto",
                minimumInputLength: 1,
                ajax: { // instead of writing the function to execute the request we use Select2's convenient helper
                    url: new connection().url+"?classname=Items.Get&wrap_to=select2",
                    dataType: 'json',
                    quietMillis: 250,
                    data: function (term, page) {
                        return {
                            item_name: term.term, // search term
                        };
                    },
                    results: function (data, page) { // parse the results into the format expected by Select2.
                        // since we are using custom formatting functions we do not need to alter the remote JSON data
                        return { results: data.items };
                    },
                    cache: true
                },

                id: function(bond){ console.log(bond); return bond.id; },
                text:function(bond){ return bond.text+"-"+bond.tpname; }
                //escapeMarkup: function (m) { return m; } // we do not want to escape markup since we are displaying html in results
        });

    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", "/?md=additem_bill",success, error, "text/html");
}

function buy_unit_chg(target) {
    var url = new connection().url+"/?classname=General.getEquivalence&from_eq="+$(target).val();
    success=function (result,status,xhr) {
        console.log(result);
        var current_amount = parseFloat($("#cur_amount").val());
        $("#cur_amount").val(current_amount/result[0].amount);
    };

    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", url,success, error, "text/html");
}

function selProduct(target) {
    success=function (result,status,xhr) {
        console.log(result);
        if (result[0]!=undefined){
            $("#equivalence").val(result[0].unit+":"+result[0].unit_name);
            $("#equivalence").attr("unit",result[0].unit);
        }else{
            $("#equivalence").val("517:Unidad");
            $("#equivalence").attr("unit",517);
        }
        /*
        Loading the current amount.
         */
        success=function (result,status,xhr) {

            $("#cur_amount").val(result[0].amount);
        };
        error = function (xhr,status,error){
            console.log(error);
        };
        serverCall("get", "/?classname=Items.Get&code="+$("#product").val(),success, error, false);
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", "/?classname=Items.getItemRecipe&recipe="+$("#product").val(),success, error, false);
}
function addName(target) {
    $("#sign_receive").html($(target).val());
}