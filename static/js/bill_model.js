$(function () {
   
    setTotals();
    var datatime=$("[data-time]").attr("data-time");
    console.log(datatime);
    $("[data-time]").val(datatime.replace(" ", "T"))
});
function price_set(target) {
    var tr = $(target).parent().parent();
    var amount = $(tr).find("[data-type='amount']").val();
    var price_uni = $(tr).find("[data-type='price_uni']").text();
    var tax = $(tr).find("[data-type='tax']").text();

    var disc_clean = (parseFloat($("#general_disc").val())/100);
    var subtotal=((amount*price_uni))-(disc_clean*(amount*price_uni));
    var tax_clean=subtotal*(tax/100);

    $(tr).find("[data-type='total']").text(sugelico.numberWithCommas(subtotal+tax_clean));
    setTotals();


}

function setTotals() {
    var subtotal=0.00;
    var tax_clean=0.00;
    var disc_total=0.00;
    var disc_clean = (parseFloat($("#general_disc").val())/100);


    $("#products_tbd tr").each(function (value, element) {

        var amount = $(element).find("[data-type='amount']").val();
        var price_uni = $(element).find("[data-type='price_uni']").text();
        var tax = $(element).find("[data-type='tax']").text();

        var fieldsubtotal=(amount*price_uni);
        var discount_total=fieldsubtotal*disc_clean;
        disc_total+=discount_total;
        subtotal+=(fieldsubtotal-discount_total);

        tax_clean+=((fieldsubtotal-discount_total)*(tax/100));
        $(element).find("[data-type='total']").val(sugelico.numberWithCommas(subtotal+tax_clean));

    })
    $("#total_disc").text(sugelico.numberWithCommas(disc_total));
    $("#subtotal").text(sugelico.numberWithCommas((subtotal)));
    $("#tax").text(sugelico.numberWithCommas(parseFloat(tax_clean)));
    $("#total").text(sugelico.numberWithCommas(subtotal+tax_clean));
}

