/**
 * Created by hidura on 10/14/2016.
 */
function create() {
    var frm={};
    frm.classname="Accounts.create";
    frm.account_name=$("#account_name").val();
    frm.acc_type=$("#acc_type").val();
    frm.amount=$("#amount").val();


    success=function (result,status,xhr) {
        document.getElementById("register_form").reset();
        loadAccounts();
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);
}

function loadAccounts() {
    var frm={};
    frm.classname="Accounts.Get";
    frm.account_name="";

    success=function (result,status,xhr) {

        var tbd=$("#account_tbd");
        tbd.fadeOut("fast");
        tbd.empty();
        $.each(result,function (index, field) {
            var tr =document.createElement("tr");
            $(tr).append($('<td />').html(field.code));
            $(tr).append($('<td />').html(field.account_name));
            $(tr).append($('<td />').html(field.cat_tpname));
            $(tr).append($('<td />').html(field.current_amount));

            tbd.append(tr);
        });
        tbd.fadeIn("fast");
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);
}