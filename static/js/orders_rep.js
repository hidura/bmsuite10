$("#filters").click(function(event){
	sugelico.getServerCall("classname=Bills.getProdsHistPreorder&preorder="+$("#order").val(), function(data, status) {
		console.log(data);
		var result=JSON.parse(data);
		$("#paytype").text(result.paytype);
		$("#subtotal").text("Monto de los productos: "+parseFloat(result.subtotal).toLocaleString('en-US', {minimumFractionDigits: 2}));
		$("#item_tbd").empty();

		JSON.parse(result.prods).forEach(function (index, field) {
				tr = document.createElement("tr");
				$(tr).append($('<td style="width: 30px"/>').val(field.Name).html(field.Name));
				$(tr).append($('<td style="width: 50px"/>').val(field.client_name).html(field.client_name));
				$(tr).append($('<td />').val(field.waiter).html(field.waiter));
				$(tr).append($('<td />').val(field.date).html(field.date));
				$(tr).append($('<td />').val(field.hour).html(field.hour));
				status="Producto Servido";
				if(field.status===30){
					status="Producto Borrado";
				}
				if(field.status===31){
					status="Producto en proceso";
				}
				$(tr).append($('<td />').val(field.status).html(status));

				$("#item_tbd").append(tr)  ;
		})
	});
});