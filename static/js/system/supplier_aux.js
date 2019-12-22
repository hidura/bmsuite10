/**
 * Created by hidura on 5/18/2016.
 */
function openContact(target) {
    success=function (result,status,xhr) {
        $(result).slideUp('fast');
        $("#contact_div_content").append(result);
        $(result).slideDown('fast');
        
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", "/?md=contact",success, error, "text/html");
}

function createSup(target) {
    success=function (result,status,xhr) {
        console.log(result)
        $("#sup_code").val(result.code);
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    var wparams = {};
    wparams.classname="supplier.create";
    wparams.sup_name=$("#supname").val();
    console.log(wparams);

    serverCall("post", wparams,success, error, false);
    
}

function saveSupplier() {
    var wparams = {};
    wparams.classname="supplier.Handle";
    wparams.code=$("#sup_code").val();
    wparams.sup_name=$("#supname").val();
    wparams.doc_type=$("#doc_type").val();
    wparams.rnc=$("#rnc").val();
    success=function (result,status,xhr) {
        $("#sup_code").val(result.code);
        $("#supplier").append($("<option selected/>").val(result.code).html(wparams.sup_name));
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", wparams,success, error, false);
    return false;
}