/**
 * Created by hidura on 4/4/2016.
 */



function login(){

    if (validmail($("#mail").val())){
        var formData = {};
        formData.classname="login.LoginSys";
        formData.username=$("#username").val();
        formData.passwd=$("#password").val();
        success=function (result,status,xhr) {
                if(result.key !=null || result.key != undefined){
                    addCookie("loginkey",result.key,7);
                    window.location.href="/?md=index";
                }else{
                    $("#msg_error strong").empty().text("Datos invalidos!");
                    $("#msg_error span").empty().text("Los datos suministrados no son validos, favor volverlo a intentar");
                    $("#danger_alert").slideDown("fast");
                }
        };
        error=function(xhr,status,error){

        };
        serverCall("post", formData, success, error, false);
    }
    return false;
}