$(document).ready(function() {
    // EDIT PRINTERS
    $(".edit_printer").click(function () {
        var currentPrinter = $(this);
        var editPrinterModal = $("#edit_printer");

        var callback = function(data, status){
            console.log(data);
            console.log(status);
            editPrinterModal.find("#brand").val("Printer 1");
            editPrinterModal.find("#model").val("CJSK-23a32-DD");
            editPrinterModal.find("#papersize").val("Activa");
            editPrinterModal.find("#thermal").val("1").trigger("change");
            editPrinterModal.find("#autocut").val("0").trigger("change");
            editPrinterModal.find("#path").val("72.wd.23.2323");
        }

        sugelico.getServerCall({}, callback);

        var editPrinterCallback = function(data, status){
            var form = editPrinterModal.find("#edit_printer_form");
            console.log(form.serialize());
        }

        $("#edit_printer_btn").click(function(){
            sugelico.postServerCall({}, editPrinterCallback);
        });
    });

    $(".delete_printer").click(function () {
        var currentPruductType = $(this);
        var deletePrinterModal = $("#delete_printer");

        var deletePrinterCallback = function(data, status){
            console.log("eliminado");
        }

        $("#delete_printer_btn").click(function(){
            deletePrinterModal.modal("hide");
            var data = {
                "classname":"Users.Handle",
                "status":13, 
                code:14
            }
            sugelico.postServerCall(data, deletePrinterCallback);
        });
    });
});