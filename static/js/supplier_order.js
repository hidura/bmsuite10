var products=[];
$(function () {
    //Putting the
    var now = new Date();
    var month = (now.getMonth() + 1);
    var day = now.getDate();
    if (month < 10)
        month = "0" + month;
    if (day < 10)
        day = "0" + day;
    var today = now.getFullYear() + '-' + month + '-' + day;
    $("#generated").val(today);
    $("#payalert").val(today);
    $("#expiration").val(today);

    $("#add_product").click(function (event) {

        if ($("#amount").val().length === 0) {
            alert("Debe colocar una cantidad");
            return;
        }
        var amount = parseFloat($("#amount").val());
        var discount = 0.00;


        var e = document.getElementById("product");
        var product_info = e.options[e.selectedIndex].getAttribute("data");
        var product_name = e.options[e.selectedIndex].text;
        var product_id = e.options[e.selectedIndex].value;
        var subtotal = parseFloat($("#subtotal_item").val());

        var tax = parseFloat($("#prod_tax").val());
        var discount_item = parseFloat($("#discount_item").val());
        var item_total = parseFloat($("#prod_total").val());
        var currentTable = $('#products_bill').DataTable();
        var editDeleteBtnTemplate = '<button class="btn btn-default delete_user" ' +
            'data-id="\{id\}" onClick="deleteProd(this);" data-target="#delete_product"><i ' +
            'class="fa fa-trash"></i></button>';
        products.push({
            "amount": amount, "product": product_id,"discount":discount_item,
            "total_tax": tax, "subtotal": subtotal, "total": item_total,
            "product_name":product_name
        });
        currentTable.row.add([product_name, sugelico.numberWithCommas(amount),
            sugelico.numberWithCommas(parseFloat(product_info.split(";")[0])),
            sugelico.numberWithCommas(subtotal), sugelico.numberWithCommas(discount_item),
            sugelico.numberWithCommas(tax), sugelico.numberWithCommas((item_total)),
            editDeleteBtnTemplate.replace("\{id\}", product_id)]).draw(false);

        $("#subtotal").val(sugelico.numberWithCommas( subtotal + parseFloat(sugelico.numberWithOutCommas($("#subtotal").val()))));
        $("#discount").val(sugelico.numberWithCommas(discount + parseFloat(sugelico.numberWithOutCommas($("#discount").val()))));
        $("#taxes").val(sugelico.numberWithCommas(tax + parseFloat(sugelico.numberWithOutCommas($("#taxes").val()))));
        $("#total").val(sugelico.numberWithCommas(((subtotal + tax)-discount_item) +
            parseFloat(sugelico.numberWithOutCommas($("#total").val()))));
        $("#product").val(0).trigger("change");
        $("#amount").val("");
        $("#subtotal_item").val("");
        $("#prod_tax").val("");
        $("#discount_item").val("");
        $("#prod_total").val("");

    });
    $("#add_supplier_div").on("hidden.bs.modal", function () {
        loadSupplier();
    });
    $("#paytype").change(function (e) {
       if(parseInt($("#paytype").val())>0 && parseInt($("#paytype").val())<=2 ){
           var acc_selector=$("#accounts");
           acc_selector.val(8);
           acc_selector.change();
           acc_selector.prop("readonly", true);
           $(".select2-selection").prop("disabled", true);
           $("#expiration").prop("readonly", false);
           $("#total_paid").prop("readonly", true);
       }else{
           var acc_selector=$("#accounts");
           acc_selector.val(0);
           acc_selector.change();
           acc_selector.prop("readonly", false);
           $(".select2-selection").prop("disabled", false);
           $("#expiration").prop("readonly", true);
           $("#total_paid").prop("readonly", false);
       }
    });
});

function saveBill(target) {


    var date = new Date;
    var data= {
        supplier:$("#supplier").val(),
        ncf:$("#ncf").val(),
        recive_time:date.getHours()+":"+date.getMinutes()+":"+date.getSeconds(),
        reference:$("#reference").val(),
        generated:$("#generated").val(),
        receive_date:$("#generated").val(),
        expires:$("#expiration").val(),
        payalert:$("#payalert").val(),
        paytype:$("#paytype").val(),
        subtotal:$("#subtotal").val(),
        total:$("#total").val(),
        other_costs:$("#other_costs").val(),
        discount:$("#discount").val(),
        credit:$("#credit:checked").length > 0,
        taxes:$("#taxes").val(),
        warehouse:$("#warehouse").val(),
        buy_name:$("#supplier").val()+$("#generated").val().replace('/',''),
        "classname":"BuyOrder.create",
        "products":JSON.stringify(products)
    };

    var success = function (data, status) {
        if (JSON.parse(data).code!=undefined){
            document.getElementById("formulary").reset();
            var currentTable = $('#products_bill').DataTable();
            products=[];
            currentTable.clear().draw();
        }
    };
    $.ajax({
            url: sugelico.route+'add_order',
            data: JSON.stringify(data),
            processData: false,
            contentType: 'application/json',
            type: 'POST',
            success: success
        }
    );

}


function loadSupplier(targetsup) {
    var getClientCallBack = function (data, status) {

        if (data) {
            var category_options = '<option value="0">Seleccione un Suplidor</option>';

            JSON.parse(data).forEach(function (client) {
                category_options += '<option value="' + client.code + '" ' +
                    ' >' + client.sup_name + '</option>';
            });

            $("#supplier").html(category_options);
            $("#supplier").val(0).trigger("change");
        }
    };


    sugelico.postServerCall({
        "classname": "supplier.Get",
        "sup_name": ""
    }, getClientCallBack);
}


function new_supplier(targetBtn) {
    $(targetBtn)[0].disabled = true;
    var getClientCallBack = function (data, status) {
        $("#add_supplier_div").modal("toggle");
        loadSupplier();
    };

    formData = new FormData(document.getElementById("supplier_form"));
    sugelico.postFormServerCall(formData, getClientCallBack, 'addnewsupplier');
}