var labels=[];
var values=[];
var data=[];
$(function () {

    var head = document.getElementsByTagName('head')[0];
    var script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = '/resources/site/assets/chart.js/dist/Chart.js';
    var full = window.location.host;
    //window.location.host is subdomain.domain.com
    var parts = full.split('.',2);
    var namespace = '/'+parts[0];

    var socket = io.connect(location.protocol + '//livefeed.bmsuite.io:2235' + namespace);


    if (!window.WebSocket) alert("WebSocket not supported by this browser");
    socket.on('connect', function() {
        socket.emit('getBills', {data: 'I\'m connected!'});
    });
    socket.on('my_response', function(msg) {
        data = JSON.parse(msg.data);
        $("#cashbox_area").html(data.total_earnings+data.paytypes);
    });



});
function billsLst(target) {
    var tr="";
    data.bills.forEach(function (bill) {
        if ($(target).attr("data-id")===bill.paytpname){
            tr+="<tr>" +
                    "<td>" +bill.billpreorder+"</td>" +
                    "<td>" +sugelico.numberWithCommas(bill.ptpsubtotal)+"</td>" +
                    "<td>" +sugelico.numberWithCommas(bill.ptptax)+"</td>" +
                    "<td>" +sugelico.numberWithCommas(bill.ptptotal)+"</td>" +
                    "<td>" +sugelico.numberWithCommas(bill.ptpaid)+"</td>" +
                "</tr>"
        }
    });
    var tblStr="" +
        "<div class='col-md-12'>" +
            "<table class='table table-responsive'>" +
                "<thead>" +
                    "<tr>" +
                        "<td>Codigo</td>" +
                        "<td>Subtotal</td>" +
                        "<td>Impuesto</td>" +
                        "<td>Total</td>" +
                        "<td>Total pagado</td>" +
                    "</tr>" +
                "</thead>" +
                "<tbody>" +
                    tr+
                "</tbody>"+
            "</table>" +
        "</div>";
    sugelico.openDialog("Facturas",tblStr);
}
function loadChart() {
    var ctx = document.getElementById("bills");
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Productos mas vendidos',
                data: values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255,99,132,1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero:true
                    }
                }]
            }
        }
    });
}