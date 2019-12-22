/**
 * Created by hidura on 5/10/2017.
 */

var profile =loadProfile();

function create(target) {
    var frm=$(document.getElementById("formulary")).serializeObject();
    frm.classname="Requisition.create";

    success=function (result,status,xhr) {
        console.log(result);
        $("#code").val(result.code);
        $("#status").prop("checked", true);
        $("#requester").val(result.requested_by)
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

    frm.classname="Requisition.Handle";
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
                                "<label id='product_type_lbl'>Código</label>" +
                                "<input id='code' name='code' class='form-control' />" +
                            "</div>" +
                        "</div>" +
                "</form>" +

                "<div class='form-group'>" +
                    "<div class='col-md-3'><button class='btn btn-info'><i class='fa fa-search' " +
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
    openDialog("Busqueda de requisiciones", msg, buttons, "large");



}

function loadBills(target) {
    var frm=$(document.getElementById("bill_fnd")).serializeObject();
    frm.classname="Requisition.Get";

    success=function (result,status,xhr) {
        console.log(result);
        $.each(result, function (index, field) {
            var tr = document.createElement("tr");
            var btn="<button class='btn btn-info' bill='"+field.code+"' onClick='loadBillInfo(this);'><i class='fa fa-edit'></i></button>";
            $(tr).append($("<td />").val(field.code).html(field.code));
            $(tr).append($("<td />").val(field.requested_by).html(field.requested_by));
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
    frm.classname="Requisition.Get";
    frm.code=$(target).attr("bill");

    success=function (result,status,xhr) {
        $.each(result, function (index, field) {
            $("#code").val(field.code);
            $("#description").val(field.description);
            $("#requester").val(field.requested_by);
            $("#status").prop("selected", false);
            if (field.status==11){
                $("#status").prop("selected", true);
            }
            $("#date").val(field.created.split(" ")[0]);
            $(".bootbox-close-button").click();

        });
        var frm={};
        frm.classname="Requisition.getitem2Quote";
        frm.bill=$(target).attr("bill");
        success=function (result,status,xhr) {

            $.each(result, function (index, field) {
                var btn="";

                if (profile.type===71) {
                    btn+="<td class='no-print'><button class='btn btn-info' product='"+field.product_code+"' " +
                      "onClick='acceptItem(this);'><i class='fa fa-check-circle-o'></i></button>" +
                      "</td><td class='no-print'><button class='btn btn-danger' product='"+field.product_code+"' " +
                      "onClick='rejectItem(this);'><i class='fa fa-trash-o'></i></button></td>";
                }
                if (profile.type===74){
                    btn+="<td class='no-print'><button class='btn btn-info' product='"+field.product_code+"' " +
                      "onClick='acceptItem(this);'><i class='fa fa-check-circle-o'></i></button>" +
                      "</td><td class='no-print'><button class='btn btn-danger' product='"+field.product_code+"' " +
                      "onClick='rejectItem(this);'><i class='fa fa-trash-o'></i></button></td>";
                    btn+="<td class='no-print'><button class='btn btn-success' product='"+field.product_code+"' " +
                    "onClick='approveItem(this);'><i class='fa fa-truck'></i></button>";
                }
                var tr = document.createElement("tr");
                $(tr).append($("<td>").html(field.product_code));
                $(tr).append($("<td>").html(field.product));
                $(tr).append($("<td>").html(field.amount));
                $(tr).append($("<td />").val(field.unit).html(field.unit));
                $(tr).append(btn);
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
                    frm.classname="Requisition.additem2Quote";
                    frm.bill=$("#code").val();
                    frm.amount=$("#amount").val();
                    frm.product=$("#product").val();

                    success=function (result,status,xhr) {
                        var tr = document.createElement("tr");
                        var product = $("#product").val();
                        $(tr).append($("<td>").html($("#product option[value='"+product+"']").text()));
                        $(tr).append(($("<td>").html($("#amount").val())));
                        $("#products_tbd").append(tr);
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
        openDialog("Productos en la Requicisión.", result, buttons, "large");
        $("#equivalence").parent().parent().hide();
        $("#subtotal_item").parent().hide();
        $("#tax_item").parent().hide();
        $("#other_costs_item").parent().hide();
        $("#discount_item").parent().hide();
        $("#total_item").parent().hide();
        $("#cur_amount_div").parent().hide();
        $("#buy_unit").parent().hide();
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


function acceptItem(target) {
    var frm={};
    frm.classname="Requisition.chngStatusProd";
    frm.bill=$("#code").val();
    frm.product=$(target)[0].getAttribute("product");
    frm.newStatus=19;
    success=function (result,status,xhr) {
        console.log(result);
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);
}



function rejectItem(target) {
    var frm={};
    frm.classname="Requisition.chngStatusProd";
    frm.bill=$("#code").val();
    frm.product=$(target)[0].getAttribute("product");
    frm.newStatus=20;
    success=function (result,status,xhr) {
        console.log(result);
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);
}

function approveItem(target) {
    var frm={};
    frm.classname="Requisition.chngStatusProd";
    frm.bill=$("#code").val();
    frm.product=$(target)[0].getAttribute("product");
    frm.newStatus=19;
    success=function (result,status,xhr) {
        console.log(result);
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);
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