/**
 * Created by hidura on 8/2/2016.
 */

function create(target) {
    if ($("#receive_by").val().toString().length<2){
        alert("Debe colocar el nombre de quien recibe los productos");
        return;
    }
    if ($("#description").val().toString().length<5){
        alert("Debe colocar una descripción");
        return;
    }
    var frm=$(document.getElementById("formulary")).serializeObject();
    frm.classname="Items.RegisterMove";

    success=function (result,status,xhr) {

        $("#code").val(result);
        $("#status").prop("checked", true);
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
                    frm.classname="Items.moveProduct";


                    success=function (result,status,xhr) {
                        console.log(result);
                        var tr = document.createElement("tr");
                        var product = $("#product").val();
                        $(tr).append(($("<td>").html(result.code)));
                        $(tr).append($("<td>").html($("#product option[value='"+product+"']").text()));
                        $(tr).append(($("<td>").html($("#amount").val())));

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
        //$("#cur_amount_div").slideDown("fast");

        //getTypes($("#doc_type")[0], 9);

        url=new connection().url+"?classname=Items.Get&wrap_to=select2";
        var select = $("#product");
        select.removeAttr("onChange");
        $("#buy_unit_div").slideUp("fast");
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


function addName(target) {
    $("#sign_receive").html($(target).val());

}