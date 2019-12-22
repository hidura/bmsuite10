$(function () {
	var gen607ReportCallback = function(data, status) {
	    console.log(data);
	    if (data.error===undefined){
            var currentTable = $('#gen607_table').DataTable();

            currentTable.clear().draw();
            data.details.forEach(function(bill){
                console.log(bill);
                if (bill.billbilltp==121){
                    currentTable.row.add([
                        bill.billpreorder,
                    (bill.billbilltp==121)?"CONTADO":"CXC",
                    bill.ptpregistred.split(" ")[0],
                    bill.client_name,
                    bill.rnc,
                    (bill.ptpncf===null || bill.ptpncf===undefined) ?"" :bill.ptpncf,
                    sugelico.numberWithCommas(parseFloat(bill.billsubtotal).toFixed(2)),
                    sugelico.numberWithCommas(parseFloat(bill.billsubtotal*.18).toFixed(2)),
                    (bill.billbilltp==121)? sugelico.numberWithCommas(parseFloat(bill.billsubtotal*.1)
                        .toFixed(2)):0.00,
                    sugelico.numberWithCommas(parseFloat(bill.billtotal).toFixed(2)),
                    bill.ptpayname
                ]).draw( false );
                }

            });
        }

	};



    $("#filters").submit(function(event){
    	event.preventDefault();
    	var data = {
	        "classname": "Accounting.get607",
	        "end_date": $("#end").val(),
            "ncf_type":$("#ncftype").val(),
	        "from_date": $("#from").val()
	    }
	    console.log(data);
    	sugelico.postServerCall(data, gen607ReportCallback);
    });
});