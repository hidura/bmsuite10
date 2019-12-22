$(function () {
    $("#filters").submit(function(event){
    	event.preventDefault();
    	var data = {
	        "classname": "Bills.GetSales",
	        "item_type": $("#product_type").val(),
	        "type_product": $("#produ_type").val(),
	        "category": $("#category").val(),
	        "end": $("#end").val(),
	        "from": $("#from").val()
	    };

	    console.log(data);

    	sugelico.postServerCall(data, function(data, status) {
    	    var currentTable = $('#sales_rep_table').DataTable();
            currentTable.clear().draw();
            var total_sale=0.00;
			JSON.parse(data).forEach(function(product){
			    var amount = 0.00;
			    if (product.amount !== null){
			        amount=product.amount;
                }
			    total_sale+=(parseFloat(product.sale_amount)*parseFloat(product.price));
                currentTable.row.add([product.item_name, product.unit_name,
                    (parseFloat(amount)-product.buys_amount)+product.sale_amount,
                    product.buys_amount,
                    product.sale_amount,
                    parseFloat(amount),
                    sugelico.numberWithCommas((parseFloat(product.sale_amount)*parseFloat(product.price)).toFixed(2))]).draw( false );
            });
			$("#total").text(sugelico.numberWithCommas(total_sale));
		});
    });
});