/**
 * Created by hidura on 10/14/2016.
 */

function create() {
    var frm={};
    frm.classname="Accounts.create";
    frm.account_name=$("#account_name").val();
    frm.classification=$("#acc_type").val();
    frm.account_type=$("#class_account").val();
    frm.amount=$("#amount").val();
    frm.position=$("#position").val();


    success=function (result,status,xhr) {
        document.getElementById("register_form").reset();
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    sugelico.postServerCall(frm,success);
}

function changeClassification(element) {


    success=function (result,status,xhr) {

        var tbd=$("#acc_type");
        tbd.empty();
        $(tbd).append($('<option />').val("0").html("Favor elegir un tipo de cuenta"));
        JSON.parse(result).forEach(function (field,index) {
            $(tbd).append($('<option />').val(field.code).html(field.tpname));
        });

    };
    error = function (xhr,status,error){
        console.log(error);
    };
    if(parseInt($(element).val())==18){
        $("#position").val("1")
    }
    if(parseInt($(element).val())==19){
        $("#position").val("2")
    }
    if(parseInt($(element).val())==20){
        $("#position").val("3")
    }
    if(parseInt($(element).val())==21){
        $("#position").val("4")
    }
    if(parseInt($(element).val())==22){
        $("#position").val("5")
    }
    if(parseInt($(element).val())==23){
        $("#position").val("6")
    }
    if(parseInt($(element).val())==24){
        $("#position").val("7")
    }

    sugelico.getServerCall("classname=Types.Get&key=&level="+$(element).val(),success);
}



