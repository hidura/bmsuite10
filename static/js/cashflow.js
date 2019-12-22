$(function () {

    $("#filters").submit(function(event){
    	event.preventDefault();
    	var end =$("#end").val();
    	var from =$("#from").val();


    	var data = {
	        "classname": "Bills.getBills",
	        "end": $("#end").val(),
	        "from": $("#from").val()
	    }

    	sugelico.postServerCall(data, function(data, status) {

            if (data.error===undefined){
				var currentTable = $('#cashflow_table').DataTable();

                currentTable.clear().draw();
                var total=0.00;
                var subtotal=0.00;
                var tax=0.00;
                console.log(data);
				JSON.parse(data).forEach(function(bill){
					currentTable.row.add([
						bill.billcode,
						bill.paytpname,
						new JulianDate().julian(bill.billdate).getDate().toLocaleDateString("en-US"),
						bill.billtime,
						bill.billsubtotal,
						bill.billtax,
						bill.billtotal
					]).draw( false );
					subtotal+=bill.billsubtotal;
					tax+=bill.billtax;
					total+=bill.billtotal;
				});
				$("#subtotal").text(sugelico.numberWithCommas(subtotal.toFixed(2)));
				$("#tax").text(sugelico.numberWithCommas(tax.toFixed(2)));
				$("#total").text(sugelico.numberWithCommas(total.toFixed(2)));

			}
		});
    });
});