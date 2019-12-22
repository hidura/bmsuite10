/**
 * Created by hidura on 9/24/2016.
 */
function create() {
    var frm={};
    frm.classname="Bills.openPreorder";
    frm.billtype=101;
    frm.table=1;
    frm.people_on=1;


    success=function (result,status,xhr) {
        $("#code").val(result.preorder);
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);
}
function addProduct() {
    var frm ={};
    frm.classname="Items.Get";
    frm.code=$("#input_sel").val();
    success=function (result,status,xhr) {
        var tr = document.createElement("tr");
        var product = $("#input_sel").val();
        var amount = $("#amount").val();
        var prod_name = $("#input_sel option[value='"+product+"']").text();
         var btn="<tr>" +
             "<button class='btn btn-danger' onClick='delItem(this);'>" +
             "<i class='fa fa-trash-o'></i></button></tr>";
        console.log(result)
        $(tr).append($("<td />").val(product).html(product));
        $(tr).append($("<td />").val(prod_name).html(prod_name));
        $(tr).append($("<td />").val(amount).html(amount));
        $(tr).append($("<td />").val(result[0].subtotal*amount).html(result[0].subtotal*amount));
        $(tr).append($("<td />").val(result[0].tax*amount).html(result[0].tax*amount));
        $(tr).append($("<td />").val(result[0].price*amount).html(result[0].price*amount));

        $(tr).append(btn);
        $("#products_tbd").append(tr);

    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);

}

function delItem(target) {
    $(target).parent().parent().remove()
}

function addProducts2Bill(target) {
    $("#products_tbd").children().each(function (index, element) {
        console.log(index);
        var frm={};
        frm.classname="Bills.addProd2Preorder";
        frm.preorder=$("#code").val();
        frm.Cod=$(element).children()[0].textContent;
        frm.Cnt=$(element).children()[2].textContent;
        frm.subtotal=$(element).children()[3].textContent;
        frm.tax=$(element).children()[4].textContent;
        frm.total=$(element).children()[5].textContent;

        var contentType=false;

        success=function (result,status,xhr) {
            console.log(result)
        };
        error = function (xhr,status,error){
            console.log(error);
        };
        $.ajax({
            url: new connection().url,
            type: "post",
            data: frm,
            async:false,
            contentType: contentType,
            success: success,
            error:error
        });
    });
    $("#products_tbd").empty();
}