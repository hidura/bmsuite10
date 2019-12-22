$(function () {


    var getNCFTypesCallBack = function (data, status) {
        var currentTable;
        if ($('#cashboxes').val() == "") {
            var editDeleteBtnTemplate = '<button action="edit" class="btn btn-success load_cashbox left" data-id="\{id\}" data-toggle="modal" data-target="#edit_module"><i class="glyphicon glyphicon-pencil"></i></button>';

            currentTable = $('#cashboxes').DataTable();
            JSON.parse(data).forEach(function(cashbox){
            var j1 = new JulianDate().julian(cashbox.open_date);

            currentTable.row.add([
                    j1.getDate(),
                    cashbox.amount_open,
                    cashbox.amount_close,
                    (cashbox.close_date>0) ? new JulianDate().julian(cashbox.close_date).getDate() : "Sin cerrar",
                    (cashbox.status===14 )?"CERRADA":"ABIERTA",
                    editDeleteBtnTemplate.replace("\{id\}", cashbox.code)
                ]).draw( false );
            $("[data-id]").click(function (event) {

                if ($(this).attr("action")==="edit"){
                    loadCashBox(this);
                }
            });
            currentTable.on( 'draw', function () {
                        $("[data-id]").click(function (event) {
                            console.log($(this).attr("action"));
                            if ($(this).attr("action")==="edit"){
                                loadCashBox(this);
                            }
                        })
                    } );

        });
        }


	};


	sugelico.postServerCall({
        "classname": "Bills.getCashBoxByUser",
        "owner":11
    }, getNCFTypesCallBack);
	$("#filters").submit(function (event) {
        event.preventDefault();
        $("#sel_cashbox").modal();
    });
});


function loadCashBox(target) {
    var getBillsCallBack = function (data, status) {
        var currentTable;

        if ($('#sales_table').val() == "") {
            var editDeleteBtnTemplate = '<button onClick="loadCashBox(this)" class="btn btn-success load_cashbox left" data-id="\{id\}" data-toggle="modal" data-target="#edit_module"><i class="glyphicon glyphicon-pencil"></i></button>';

            currentTable = $('#sales_table').DataTable();
            JSON.parse(data).forEach(function(bill){
            var j1 = new JulianDate().julian(bill.registred);
            console.log(bill);
            currentTable.row.add([
                    "","","","",
                    j1.getDate(),
                    cashbox.amount_open,
                    cashbox.amount_close,
                    (cashbox.close_date>0) ? new JulianDate().julian(cashbox.close_date).getDate() : "Sin cerrar",
                    (cashbox.status===14 )?"CERRADA":"ABIERTA",
                    editDeleteBtnTemplate.replace("\{id\}", cashbox.code)
                ]).draw( false );


        });
        }


	};


	sugelico.postServerCall({
        "classname": "Bills.getBillsInCashBox",
        "cashbox":$(target).attr("data-id")
    }, getBillsCallBack);

}