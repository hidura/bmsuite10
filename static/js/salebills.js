var products=[];

$(function () {
    //LOAD all Categories
	var getCategoryCallBack = function (data, status) {
		if(data){
            var category_options = '<option value="0">Seleccione un producto</option>';

            data.forEach(function(product){
                category_options += '<option value="'+ product.code +'" ' +
                    'data="'+product.subtotal+';'
                    +product.tax+'">'+ product.item_name+'</option>';
            });

            $("#product").html(category_options);
        }
	};

	var data = {
        "classname": "Items.Get"
    };

	sugelico.postServerCall(data, getCategoryCallBack);

	var getNCFTypesCallBack = function (data, status) {
		if(data){
            var category_options = '<option value="0">Seleccione un Tipo de NCF</option>';
            data.forEach(function(ncftype){
                category_options += '<option value="'+ ncftype._type+'" ' +
                    '>'+ ncftype.name+'</option>';
            });

            $("#ncftype").html(category_options);
        }
	};


	sugelico.postServerCall({
        "classname": "Accounts.getNCFTypes",
        "name":""
    }, getNCFTypesCallBack);


	var getPayTypesCallBack = function (data, status) {
	    if(data){
            var category_options = '<option value="0">Seleccione un Tipo de pago</option>';

            data.forEach(function(paytype){
                category_options += '<option value="'+ paytype.code +'" ' +
                    '>'+ paytype.tpname+'</option>';
            });

            $("#paytype").html(category_options);
        }
	};


	sugelico.postServerCall({
        "classname": "Types.Get",
        "level":11
    }, getPayTypesCallBack);


	var getClientCallBack = function (data, status) {
	    if(data){
            var category_options = '<option value="0">Seleccione un Cliente</option>';

            data.forEach(function(client){
                category_options += '<option value="'+ client.code +'" ' +
                    '>'+ client.cl_name+'</option>';
            });

            $("#client").html(category_options);
            $("#client").val(1).trigger("change");
        }
	};


	sugelico.postServerCall({
        "classname": "Clients.Get",
        "cl_name":""
    }, getClientCallBack);


    $("#save_bill").click(function (event) {
        if($("#client").val()==0){
            alert("Debe elegir un cliente");
            return;
        }

        if($("#paytype").val()==0){
            alert("Debe elegir un tipo de pago");
            return;
        }
        var pt=$("#paytype").val();
        var paytype={};
        paytype[pt]=sugelico.numberWithOutCommas($("#total").text());
        var data={
            "classname":"Bills.closeAccount",
            "client":$("#client").val(),
            "ncf_type":$("#ncftype").val(),
            "paytype":$("#paytype").val(),
            "order_type":101,
            "client_name_pre":$("#client option:selected").text(),
            "billtype":112,
            "subtotal":sugelico.numberWithOutCommas($("#subtotal").text()),
            "tax":sugelico.numberWithOutCommas($("#tax").text()),
            "total":sugelico.numberWithOutCommas($("#total").text()),
            "discount":sugelico.numberWithOutCommas($("#total_discount").text()),
            "products":products,
            "preorder":0,
            "billtp_extra":0,
            "paytypelst":paytype,
            "waiter":sugelico.getCookie("loginkey")
        };
        $("#subtotal_print").text(sugelico.numberWithOutCommas($("#subtotal").text()));
        $("#tax_print").text(sugelico.numberWithOutCommas($("#tax").text()));
        $("#disc_print").text(sugelico.numberWithOutCommas($("#discount").text()));
        $("#total_print").text(sugelico.numberWithOutCommas($("#total").text()));
        $("#products_tbd_print").html($("#products_tbd").clone().html());
        var saveAcccount = function (data, status) {
            console.log(data);
            $("#subtotal_print").text(sugelico.numberWithOutCommas($("#subtotal").text()));
            $("#tax_print").text(sugelico.numberWithOutCommas($("#tax").text()));
            $("#disc_print").text(sugelico.numberWithOutCommas($("#discount").text()));
            $("#total_print").text(sugelico.numberWithOutCommas($("#total").text()));
            $("#products_tbd_print").append($("products_tbd").clone());
            $("#ncf").text(data.ncf);
            $("#rnc").text(data.rnc);
            $("#client_name_print").text(data.client);
            var newDate = new Date();
            $("#date").text(newDate.toDateString());
            $("#exp_date").text(data.ncf_exp);
            $("#ncf_type").text(data.ncf_title);
            $("#billcode").text(data.billcode);
            alert("Dale a imprimir para exportar a PDF.");
        };


        $.ajax({
            url: sugelico.route,
            data: JSON.stringify(data),
            processData: false,
            contentType: 'application/json',
            type: 'POST',
            success: saveAcccount
        }
        );

    });


	$("#add_product").click(function (event) {

        if($("#amount").val().length===0)
        {
            alert("Debe colocar una cantidad");
            return;
        }
        var amount=parseFloat($("#amount").val());
        var discount=0.00;
        if($("#discount").val().length>0)
        {
            discount=parseFloat($("#discount").val());
        }

        var e = document.getElementById("product");
        var product_info = e.options[e.selectedIndex].getAttribute("data");
        var product_name = e.options[e.selectedIndex].text;
        var product_id = e.options[e.selectedIndex].value;
        var final_subtotal=parseFloat(product_info.split(";")[0])*amount;
        var real_discount=(final_subtotal*(discount/100));
        var subtotal=(final_subtotal-real_discount);

        var tax=subtotal*parseFloat(product_info.split(";")[1])/100;
        var currentTable = $('#products_bill').DataTable();
        var editDeleteBtnTemplate = '<button class="no-print btn btn-default delete_user" ' +
            'data-id="\{id\}" data-target="#delete_product"><i ' +
            'class="glyphicon glyphicon-remove"></i></button>';
        products.push({"product":product_id, "amount":amount, "term":"","notes":"","portion":"",
        "tax":tax,"subtotal":subtotal,"total":sugelico.numberWithCommas((subtotal+tax))})
        currentTable.row.add([product_name,sugelico.numberWithCommas(amount),
            sugelico.numberWithCommas(parseFloat(product_info.split(";")[0]).toFixed(2)),
        sugelico.numberWithCommas(subtotal.toFixed(2)),sugelico.numberWithCommas(real_discount),
            sugelico.numberWithCommas(tax.toFixed(2)),sugelico.numberWithCommas((subtotal+tax).toFixed(2)),
            editDeleteBtnTemplate.replace("\{id\}", product_id)]).draw( false );
        console.log(products);
        $("#product").val(0).trigger("change");
        $("#amount").val("");
        $("#discount").val("");
        var gen_subtotal=subtotal+parseFloat(sugelico.numberWithOutCommas($("#subtotal").text()));

        $("#subtotal").text(sugelico.numberWithCommas(gen_subtotal.toFixed(2)));

        $("#tax").text(sugelico.numberWithCommas((tax+parseFloat(sugelico.numberWithOutCommas($("#tax").text()))).toFixed(2)));
        $("#total_discount").text(sugelico.numberWithCommas((real_discount+parseFloat(sugelico.numberWithOutCommas($("#total_discount").text()))).toFixed(2)));
        $("#total").text(sugelico.numberWithCommas(((subtotal+tax)+parseFloat(sugelico.numberWithOutCommas($("#total").text()))).toFixed(2)));
    });
});

