/**
 * Created by hidura on 5/17/2016.
 */
function create(target) {
    var frm=$(document.getElementById("formulary")).serializeObject();
    frm.classname="Accounting.create";
    
    success=function (result,status,xhr) {
        $("#code").val(result.code);
        $("#status").prop("checked", true);
        $("#username").html($("#person_name")[0].textContent);

    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);
}

function newSupplier(target) {
    success=function (result,status,xhr) {
        buttons={
            success:{
                label: "Salvar",
                className: "btn-success",
                callback: function () {
                    saveSupplier();
                }
            }
        };
        openDialog("Suplidores", result, buttons, "large");
        getTypes($("#doc_type")[0], 9);
        
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", "/?md=supplier_aux",success, error, "text/html");
}

function saveBill(target) {
    if ($("#subtotal").val().length<=0){
        alert("Debe colocar el subtotal, sino tiene coloque 0");
        return;
    }
    if ($("#tax").val().length<=0){
        alert("Debe colocar el impuesto, sino tiene coloque 0");
        return;
    }
    if ($("#other_costs").val().length<=0){
        alert("Debe colocar los otros costos, sino tiene coloque 0");
        return;
    }
    if ($("#discount").val().length<=0){
        alert("Debe colocar el descuento, sino tiene coloque 0");
        return;
    }
    if ($("#total").val().length<=0){
        alert("Debe colocar el descuento, sino tiene coloque 0");
        return;
    }
    if ($("#code").val().length<=0){
        alert("Debe colocar el codigo de la factura, sino tiene codigo, presione 'Nuevo'");
        return;
    }

    var frm=$(document.getElementById("formulary")).serializeObject();


    frm.classname="Accounting.Handle";
    success=function (result,status,xhr) {
        console.log(result);
        document.getElementById("formulary").reset();
        $("#products_tbd").empty();
        $("#username").html("");
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
                            "<div class='col-md-8'>" +
                                "<label id='product_type_lbl'>Suplidor</label>" +
                                "<select id='supplier_search' name='supplier' class='form-control' >" +
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

                "<div class='form-group'><br/>" +
                    "<div class='col-md-1'><button class='btn btn-info' onClick='loadBills(this); return false;'><i class='fa fa-search' ></i></button></div>" +
                "</div>"+
            "<div>" +
                "<div class='col-md-10'>" +
                    "<table id='user_tbl' class='table table-striped table-bordered dataTable no-footer'>" +
                        "<thead>" +
                            "<tr>" +
                                "<th>Codigo</th>" +
                                "<th>Suplidor</th>" +
                                "<th>Total</th>" +
                                "<th>Estado</th>" +
                                "<th></th>" +
                            "</tr>" +
                        "</thead>" +
                        "<tbody id='user_tbd'></tbody>" +
                    "</table>" +
                "</div>" +
                "</div>"+
            "<div class='col-md-10' style='text-align: right'>" +
                "<button class='btn btn-danger' onClick='cancelEdit(this);'><i class='fa fa-sign-out'></i> Cerrar</button>" +
            "</div>" +
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
            $("#tax").val(field.total_tax);
            $("#ncf").val(field.ncf);
            $("#paytype").val(field.paytype);
            $("#date").val(field.generated.split(" ")[0]);
            $("#expiration").val(field.expires.split(" ")[0]);
            $("#payalert").val(field.payalert.split(" ")[0]);
            $(".bootbox-close-button").click();
            loadItems($(target).attr("bill"));
            $("#username").html($("#person_name")[0].textContent);
        });


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
                    if($("#subtotal_item").val().length<=0){
                        alert("Debe colocar un subtotal del item");
                        return;
                    }
                    if($("#tax_item").val().length<=0){
                        alert("Debe colocar el impuesto del item, sino tiene coloque un 0");
                        return;
                    }
                    if($("#other_costs_item").val().length<=0){
                        alert("Debe colocar los otros costos del item, sino tiene coloque un 0");
                        return;
                    }
                    if($("#discount_item").val().length<=0){
                        alert("Debe colocar el descuento del item, sino tiene coloque un 0");
                        return;
                    }

                    var frm=$(document.getElementById("addItem_frm")).serializeObject();
                    //same equivalence that the recipe.
                    frm.classname="Accounting.addItem2Bill";
                    frm.bill=$("#code").val();
                    frm.unit=$("#equivalence").attr("unit");

                    success=function (result,status,xhr) {
                        console.log(result);
                        var tr = document.createElement("tr");
                        var product = $("#product").val();
                        //$(tr).append(($("<td>").html(result.code)));
                        var btn="<button class='btn btn-danger' bill='"+result.code+"' onClick='delItem(this);'><i class='fa fa-trash-o'></i></button>";
                        var buyunit=$("#buy_unit").val();
                        $(tr).append(($("<td>").html($("#amount").val())));
                        $(tr).append(($("<td>").html($("#buy_unit option[value='"+buyunit+"']").text())));
                        $(tr).append($("<td>").html($("#product option[value='"+product+"']").text()));
                        $(tr).append(($("<td>").html($("#subtotal_item").val())));
                        $(tr).append(($("<td>").html($("#tax_item").val())));
                        $(tr).append(($("<td>").html($("#total_item").val())));
                        $(tr).append(btn);
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
        openDialog("Productos en la factura.", result, buttons, "large");
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
        
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", "/?classname=Items.getItemRecipe&recipe="+$("#product").val(),success, error, false);
}

function add2Total(target, total_field) {
    var field_target = $("#"+total_field);
    var total =0.0;
    var totallst = [$("#subtotal_item").val(), $("#tax_item").val(), $("#other_costs_item").val()];
    $.each(totallst, function (index, value) {
        console.log(value, value.length);
        if( value.length > 0 ) {
            total+=parseFloat(value);
        }
    });
    field_target.val(parseFloat(total));

}

function disc2Total(target, total_field) {
    var field_target = $("#"+total_field);
    var total =field_target.val();
    var target_amount= $(target).val();
    field_target.val(parseFloat(total)-parseFloat(target_amount));
}

function delItem(target) {
    success=function (result,status,xhr) {
        console.log(result);
        loadItems($("#code").val());
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", "/?classname=Accounting.delItem2Bill&code="+$(target).attr("item_bill"),success, error, false);

}

function loadItems(bill) {
    var frm={};
    frm.classname="Accounting.getItem2Bill";
    frm.bill=bill;
    success=function (result,status,xhr) {
        console.log(result);
        $("#products_tbd").empty();
        $.each(result, function (index, field) {
            var tr = document.createElement("tr");
            var btn="<td class='no-print'><button class='btn btn-danger' item_bill='"+field.code+"' onClick='delItem(this);'><i class='fa fa-trash-o'></i></button></td>";
            if (field.status==13){
                $(tr).append($("<td>").html("-"+field.amount));
            }else {
                $(tr).append($("<td>").html(field.amount));
            }
            $(tr).append($("<td>").html(field.unit_name));

            $(tr).append($("<td>").html(field.item_name));
            $(tr).append($("<td>").html((field.total-field.tax)));
            $(tr).append($("<td>").html(field.tax));
            $(tr).append($("<td>").html(field.total));
            if (field.status!=13) {
                $(tr).append(btn);
            }
            $("#products_tbd").append(tr);
        })
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);
}