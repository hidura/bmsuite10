/**
 * Created by hidura on 3/3/2017.
 */
function create(target) {
    var frm=$(document.getElementById("formulary")).serializeObject();
    frm.classname="WareHouse.create";

    success=function (result,status,xhr) {

        $("#code").val(result.code);
        $("#status").prop("checked", true);
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);
}

function search_warehouse(target) {

    var table="<div class='row'>" +


            "</div>" +


            "<table id='items_tbl' class='table table-bordered'>" +
            "<thead>" +
            "<tr>" +
            "<th>Codigo</th>" +
            "<th>Nombre</th>" +
            "<th>Descripción</th>" +
            "<th></th>" +
            "</tr>" +
            "</thead>" +
            "<tbody id='item_tbd'></tbody>" +
            "</table>";
        buttons={

        };
        openDialog("Busqueda de almacenes", table, buttons, 'large');
        var params={};
        params.classname="WareHouse.Get";
        params.description="";

        success=function (result,status,xhr) {
            console.log(result);
            $("#item_tbd").empty();
            $.each(result, function (index, field) {
                tr = document.createElement("tr");
                $(tr).append($('<td />').val(field.code).html(field.code));
                $(tr).append($('<td />').val(field.warehouse_name).html(field.warehouse_name));
                $(tr).append($('<td />').val(field.description).html(field.description));
                $(tr).append($('<td />').html("<button onClick='edit(this);' warehouse='"+field.code+"' class='btn btn-info'><i class='fa fa-edit'></i></button>"));

                $("#item_tbd").append(tr)
            });
        };
        error = function (xhr,status,error){
            console.log(error);
        };
        serverCall("post", params,success, error, false);
}

function edit(target) {
    var params={};
        params.classname="WareHouse.Get";
        params.code=$(target).parent().parent().children()[0].textContent;

        success=function (result,status,xhr) {
            $.each(result, function (index, field) {
                $("#description").val(field.description);
                $("#code").val(field.code);
                $("#warehouse_name").val(field.warehouse_name);
                $("#warehouse_charge").val(field.warehouse_charge);
            });
            $(".bootbox-close-button").click();
        };
        error = function (xhr,status,error){
            console.log(error);
        };
        serverCall("post", params,success, error, false);

}

function saveWare(target) {
    var frm=$(document.getElementById("formulary")).serializeObject();
    if ($("#status").is(":checked")){
        frm.status=11;
    }else{
        frm.status=12;
    }

    frm.classname="WareHouse.Handle";
    success=function (result,status,xhr) {
        console.log(result);
        document.getElementById("formulary").reset();
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
                    frm.code=$("#code").val();
                    frm.classname="WareHouse.addProduct2Warehouse";


                    success=function (result,status,xhr) {
                        console.log(result);
                        var tr = document.createElement("tr");
                        var product = $("#product").val();
                        $(tr).append(($("<td>").html(result.code)));
                        $(tr).append($("<td>").html($("#product option[value='"+product+"']").text()));
                        $(tr).append(($("<td>").html($("#amount").val())));
                        var btn="<tr>" +
                         "<button class='btn btn-danger' onClick='delItem(this);'>" +
                         "<i class='fa fa-trash-o'></i></button></tr>";
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
        $("#subtotal_item").attr("readonly", "true");
        $("#tax_item").attr("readonly", "true");
        $("#other_costs_item").attr("readonly", "true");
        $("#discount_item").attr("readonly", "true");
        $("#total_item").attr("readonly", "true");
        //$("#cur_amount_div").slideDown("fast");

        //getTypes($("#doc_type")[0], 9);

        url=new connection().url+"?classname=Items.Get&wrap_to=select2";
        var select = $("#product");
        select.removeAttr("onChange");
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


function delItem(btn_target) {

    $(btn_target).parent().parent().remove()

}

function addName(target) {
    $("#sign_receive").html($(target).val());

}