var prd_name="";
var prd_code=0;
var products=[];
$(document).ready(function() {

    $("#supplier").change(function (e) {
        $("#prod_loader").show();
        var getClientCallBack = function (data, status) {
            if(data){
                var category_options = '<option value="0">Seleccione un Producto</option>';

                JSON.parse(data).forEach(function(product){
                    category_options += '<option value="'+ product.code +'" ' +
                        '>'+ product.item_name+'</option>';
                });

                $("#product").html(category_options);

                $("#prod_loader").hide();
            }
        };


        sugelico.postServerCall({"supplier":$("#supplier").val()
        }, getClientCallBack,"/getProductsBy");
    });
    $(".add_product").click(function (e) {
        prd_name=$(this).attr("data-target");
        prd_code=$(this).attr("data-id");
        var htmlStr="" +
            "<div class='col-lg-12'>" +
                "<div class='form-group'>" +
                    "<label for='sug_amount'>Cantidad</label>" +
                    "<input type='number' class='form-control' id='sug_amount' name='sug_amount'/>" +
                "</div>" +
                "<div class='form-group'>" +
                    "<label for='sug_amount'>Notas</label>" +
                    "<input type='text' class='form-control' id='sug_notes' value=' ' name='sug_notes'/>" +
                "</div>" +
                "<div class='form-group'>" +
                "<label for='supplier'>Suplidor</label>\n" +
                "<select class='form-control' id='sug_supplier' name='sug_supplier' >\n" +
                    "<option value='0'>Seleccione un suplidor</option>\n" +
                "</select>" +
                "</div>" +
            "</div>";
        var buttons={cancel: {
                label: 'Cerrar',
                className: 'btn-danger'
            },
            accept: {
                label: 'Aceptar',
                className: 'btn-primary',
                callback: function(){
                    if(!valHeader()){
                        return;
                    }
                    if (parseInt($("#sug_supplier").val())==0){
                        alert("Debe elegir un suplidor");
                        return;
                    }
                    if (parseInt($("#sug_amount").val())==0){
                        alert("Debe colocar una cantidad");
                        return;
                    }
                    var dataUpld={
                        "product":prd_code,
                        "product_name":prd_name,
                        "amount":$("#sug_amount").val(),
                        "supplier":$("#sug_supplier").val(),
                        "warehouse":$("#warehouse").val(),
                        "supplier_name":$("#sug_supplier option:selected").text(),
                        "notes":$("#sug_notes").val(),
                        "wh_name":$("#warehouse option:selected").text()
                    };
                    products.push(dataUpld);

                    var tr = document.createElement("tr");
                    $(tr).append($('<td />').val(0).html(dataUpld["product_name"]));
                    $(tr).append($('<td />').val(0).html(dataUpld["amount"]));
                    $(tr).append($('<td />').val(dataUpld["supplier"]).
                    html(dataUpld["supplier_name"]));
                    $(tr).append($('<td />').val(0).html(dataUpld["notes"]));
                    $(tr).append($('<td />').val(dataUpld["warehouse"]).
                    html(dataUpld["wh_name"]));
                    $(tr).append($('<td />').html("<button onClick='delItemRec(this); return false;' " +
                        "data-id='"+(products.length+1)+"' class='btn btn-danger'>" +
                        "<i class='fa fa-trash'></i></button>"));
                    $("#products_tbd").append(tr);
                }
            }
        };
        var afterload=function(){
            var getClientCallBack = function (data, status) {
            if(data){
                    var category_options = '<option value="0">Seleccione un Suplidor</option>';

                    JSON.parse(data).forEach(function(product){
                        category_options += '<option value="'+ product.code +'" ' +
                            '>'+ product.sup_name+'</option>';
                    });

                    $("#sug_supplier").html(category_options);

                    $("#prod_loader").hide();
                }
            };


            sugelico.postServerCall({"sup_name":""
            }, getClientCallBack,"/getSuppliersBy");
        };
        sugelico.openDialog("Confirmar cantidad", htmlStr, buttons, "large", afterload)
    });
    
    $("#add_product").click(function () {
        if(!valHeader()){
            return;
        }
        if(parseInt($("#product").val())==0){

            alert("Debe elegir un producto");
            return;
        }
        if (parseInt($("#supplier").val())==0){
            alert("Debe elegir un suplidor");
            return;
        }
        var dataUpld={
            "product":$("#product").val(),
            "prod_name":$("#product option:selected").text(),
            "amount":$("#amount").val(),
            "supplier":$("#supplier").val(),
            "warehouse":$("#warehouse").val(),
            "supplier_name":$("#supplier option:selected").text(),
            "product_name":$("#product option:selected").text(),
            "notes":$("#notes_item").val(),
            "wh_name":$("#warehouse option:selected").text()
            };
        products.push(dataUpld);
        $("#product").val(0);
        $("#product").change();
        $("#amount").val("0");
        $("#notes_item").val("");

        var tr = document.createElement("tr");
        $(tr).append($('<td />').val(0).html(dataUpld["product_name"]));
        $(tr).append($('<td />').val(0).html(dataUpld["amount"]));
        $(tr).append($('<td />').val(dataUpld["supplier"]).
        html(dataUpld["supplier_name"]));
        $(tr).append($('<td />').val(0).html(dataUpld["notes"]));
        $(tr).append($('<td />').val(dataUpld["warehouse"]).
        html(dataUpld["wh_name"]));
        $(tr).append($('<td />').html("<button onClick='delItemRec(this); return false;' " +
            "data-id='"+(products.length+1)+"' class='btn btn-danger'>" +
            "<i class='fa fa-trash'></i></button>"));
        $("#products_tbd").append(tr);
    })





});

function delItemRec(target){
    delete products[parseInt($(target).attr("data-id"))];
    $(target).parent().parent().remove();
}

function valHeader() {
    var state=true;
    if(parseInt($("#warehouse").val())==0){
        state=false;
        alert("Debe elegir un almacen de envío");
    }
    return state;
}

function saveBill(target) {
    var data ={
        "warehouse":$("#warehouse").val(),
        "buy_name":$("#order_name").val(),
        "receive_date":$("#date").val(),
        "recive_time":$("#hour").val(),
        "products":products
    };
    $.ajax({
        dataType: "json",
        type: "POST",
        url: '/add_order',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (resp) {
            console.log(resp);
            alert("Orden salvada exitosamente");
            window.location.reload();
        },error:function () {
            alert("Ha ocurrido un error al salvar la orden");
        }
    });
}