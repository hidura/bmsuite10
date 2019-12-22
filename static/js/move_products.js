var warehouse_from=0;
var warehouse_to=0;
var products=[];
$(function () {
    var data = {
        "classname": "WareHouse.Get",
        "description": ""
    };

    sugelico.postServerCall(data, function (data, status) {
        var warehouse_from = '';
        var warehouse_to = '';

        JSON.parse(data).forEach(function (warehouse) {
            warehouse_from += '<button onClick="setFrom(this);" data-id="' + warehouse.code + '" class="btn btn-danger"' +
                '>' + warehouse.warehouse_name + '</button>';
            warehouse_to += '<button onClick="setTo(this);" data-id="' + warehouse.code + '" class="btn btn-danger"' +
                '>' + warehouse.warehouse_name + '</button>';
        });


        $("#store_from").html(warehouse_from);
        $("#store_to").html(warehouse_to);
    });
    var getCategoryCallBack = function (data, status) {
        if (data) {
            var category_options = '<option value="0">Seleccione un producto</option>';
            JSON.parse(data).forEach(function (product) {
                category_options += '<option value="' + product.code + '" ' +
                    'data="' + product.subtotal + ';'
                    + product.tax + '">' + product.item_name + '</option>';
            });

            $("#product").html(category_options);
        }
    };

    var data = {
        "classname": "Items.Get"
    };

    sugelico.postServerCall(data, getCategoryCallBack);

    $("#add_product").click(function (event) {

        if ($("#amount").val().length === 0) {
            alert("Debe colocar una cantidad");
            return;
        }


        var e = document.getElementById("product");
        var product_name = e.options[e.selectedIndex].text;
        var product_id = e.options[e.selectedIndex].value;

        var currentTable = $('#products_bill').DataTable();
        var editDeleteBtnTemplate = '<button class="btn btn-default delete_user" ' +
            'data-id="\{id\}" data-target="#delete_product" onClick="deletedata(this);"><i ' +
            'class="glyphicon glyphicon-remove"></i></button>';
        products.push({"amount": $("#amount").val(), "product": product_id, "item_name": product_name});
        currentTable.row.add([product_name, sugelico.numberWithCommas($("#amount").val()),
            editDeleteBtnTemplate.replace("\{id\}", product_id)]).draw(false);
        $("#product").val(0).trigger("change");
        $("#amount").val("0");

    });
});
function setFrom(target) {
    warehouse_from = $(target).attr("data-id");
    $("#store_from").children().prop('enabled', true);
    $(target).prop('disabled', true);
}

function setTo(target) {
    warehouse_to = $(target).attr("data-id");
    $("#store_to").children().find("button").prop('enabled', true);
    $(target).prop('disabled', true);
}


function deletedata(target) {
    var currentTable = $('#products_bill').DataTable();

    products.forEach(function (prod_info) {
        if (prod_info.product_id===parseInt($(target).attr("data-id"))){
            delete products[products.indexOf(prod_info)]
        }
    });
       currentTable
        .row( $(target).parents('tr') )
        .remove()
        .draw();

    console.log(products);

}

function addMovement(target) {
    var data={
        classname:"WareHouse.addMovement"
    };
    var saveFNC=function(data){
        $("#code").val(JSON.parse(data).code);
    };
    sugelico.postServerCall(data, saveFNC);
}

function saveMovement(target) {
    $(target).prop('disabled', true);

    var data={
        classname:"WareHouse.RegisterMove",
        code:$("#code").val(),
        send_date:$("#date").val(),
        from_warehouse:warehouse_from,
        to_warehouse:warehouse_to,
        products:JSON.stringify(products),
        notes:$("#notes").val(),
        transport:$("#transport").val()
    };
    var saveFNC=function(data){
        $("#code").val("");
        $("#date").val("");
        $("#notes").val("");
        $("#transport").val("");
        products=[];
        var currentTable = $('#products_bill').DataTable();
        currentTable.clear().draw();

        $("button").prop('enabled', true);
    };
    sugelico.postServerCall(data, saveFNC);
}