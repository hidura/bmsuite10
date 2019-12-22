/**
 * Created by hidura on 10/14/2016.
 */
function create() {
    var frm={};
    frm.classname="Accounts.transfer";
    frm.account_from=$("#from_acc").val();
    frm.account_to=$("#to_acc").val();
    frm.amount=$("#amount").val();
    frm.notes=$("#notes").val();


    success=function (result,status,xhr) {
        document.getElementById("register_form").reset();
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", frm,success, error, false);
}
