/**
 * Created by hidura on 4/4/2016.
 */

function delete_order(event){
    
    var x = event.which || event.keyCode;
    if(x==13){
        foundflag=false;
        $("[name='position']").each(function (index, element) {
            
            if($(element).text()==$("#position_del").val()){
                foundflag=true;
                next_element=$(element).parent().parent().parent().next();
                target=$(element).parent().parent().parent().parent();
                ordercode=$(target).find("[name='ordercode']").val();
                
                params="?code=setDonePlate&plates="+ordercode;
                success=function (result,status,xhr) {
                    $(target).remove();
                    $("#position_del").val("");
                    $("#position_del").focus();
                };
                error=function(xhr,status,error){
                    console.log(error)
                };
                serverCall("get", params, success, error);
            }

        });
        if (!foundflag){
            alert("Posición: "+$("#position_del").val());

        }
    }
}

function getOrders() {
    params="?classname=Bills.getProductOrdered&prdstatus=32";
    success=function (result,status,xhr) {
        $.each(result, function (index, element) {
            tr = document.createElement("tr");
            $(tr).append($('<td />').val(result.table).html("<strong>MESA: "+element.table+"</strong>"));
            $(tr).append($('<td />').val(result.table).html("<strong>Orden: "+element.code+"</strong>"));
            $(tr).append($('<td />').val(result.table).html("<strong>Mesero: "+element.waiter+"</strong>"));
            $("#items_tbd").append(tr);

            $.each(element.products, function (index, field) {
                tr = document.createElement("tr");
                $(tr).append($('<td />').val(field.code).html(field.code));
                $(tr).append($('<td />').val(field.name).html(field.name));
                $(tr).append($('<td />').val(field.subtotal).html(parseFloat(field.subtotal).toLocaleString('en-US', {minimumFractionDigits: 2})));
                $(tr).append($('<td />').val(field.tax).html(parseFloat(field.tax).toLocaleString('en-US', {minimumFractionDigits: 2})));
                $(tr).append($('<td />').val(field.discount).html(parseFloat(field.discount).toLocaleString('en-US', {minimumFractionDigits: 2})));
                $(tr).append($('<td />').val(field.total).html(parseFloat(field.total).toLocaleString('en-US', {minimumFractionDigits: 2})));
                $(tr).append($('<td />').val(field.waiter).html(field.waiter));
                $(tr).append($('<td />').html("<button onClick='deleteProd(this); return false;' class='btn btn-danger'><i class='fa fa-trash'></i></button>"));
                $("#items_tbd").append(tr);
            });
        });
    };
    error=function(xhr,status,error){
        console.log(error)
    };
    serverCall("get", params, success, error);

}
function deleteProd(target) {
    params="?classname=Bills.delProdOrdered&code="+$(target).parent().parent().children()[0].textContent;
    success=function (result,status,xhr) {
        $(target).parent().parent().remove();
    };
    error=function(xhr,status,error){
        console.log(error)
    };
    serverCall("get", params, success, error);
}