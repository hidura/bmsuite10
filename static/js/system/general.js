/**
 * Created by hidura on 4/4/2016.
 */

function validmail(mail){
    valid=true;


    return valid;
}



/*
 * This function creates the cookie.
 */
function addCookie(c_name,value,exdays)
{
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = c_name+"="+value+"; "+expires;
}


function delCookies( name ) {
  document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

/*
 * This function gets the cookie value.
 */

function getCookie(cname)
{
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function getLoginKey(){
    var logkey = getCookie("loginkey");
    if (logkey==""){
        window.location="/";
    }else{
        return logkey;
    }
}
function serverCall(method, data, success, error, ctype){
    /*
    This is the serverCall Function,
    for execute this funcion, just need to:
    give a method, params, success function and error function.
     */

    if (method.toLowerCase()=="post"){
        contentType="multipart/form-data";
        if(ctype !=undefined)
            contentType=ctype;

        $.ajax({
            url: new connection().url,
            type: method,
            data: data,
            contentType: contentType,
            success: success,
            error:error
        });
    }else if(method.toLowerCase()=="get"){
        $.ajax({
            url: new connection().url+data,
            type: method,
            contentType:"application/x-www-form-urlencoded",
            success: success,
            error:error
        });
    }

}



function openDialog(title, message, buttons, classname){
    /*
    This function, receives the title, the message(can be html or string), and the buttons.
     */
    if (classname==undefined){
        classname="medium"
    }
    bootbox.dialog({
            title: title,
            message: message,
            buttons: buttons,
            size: classname
        }
    );
}


function gotomodule(module, params){
    if (params==null)
        params="";
    key=getLoginKey();
    window.location.href="/?md="+module+"&key="+key+"&"+params;
}

function getStatus(type, target, success){

    success=function (result,status,xhr) {
        if (target != null){
            $.each(result, function (index, field) {
                console.log(field);
                $('#'+target).append($('<option />').val(field.code).html(field.description));
            })

        }
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", '?classname=Status.Get&statustp='+type,success, error);


}


function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}

function stateChange(target) {
        if ($(target)[0].checked) {
            $(target).parent().children('label').html('Activo');
        } else {
            $(target).parent().children('label').html('Inactivo');
        }
        
    
}
//Function that read the database and retrieves the types.
function getTypes(target, type) {
    success=function (result,status,xhr) {
        if (target != null){
            $.each(result, function (index, field) {
                $(target).append($('<option />').val(field.code).html(field.tpname));    
            });
            
        }
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", "/?classname=Types.Get&level="+type,success, error);
}

// function getSupplier(target) {
//     console.log("dasdasd");
//    
// }

$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

function gotoModule() {
    
}


function logout() {
    delCookies("loginkey");
    console.log(getCookie("loginkey"));
    getLoginKey();
}

function getCountry(target) {
    success=function (result,status,xhr) {
        if (target != null){
            $.each(result, function (index, field) {
                $(target).append($('<option />').val(field.code).html(field.name));    
            });
            
        }
    };
    error = function (xhr,status,error){
        console.log(error("error"));
    };
    serverCall("get", "/?classname=General.getCountry",success, error);
}
function getLang() {
    return "es";
}
function loadJSON(path) {
    var json=null;
    $.ajax({
      url: path,
      async: false,
      dataType: 'json',
      success: function (response) {
        json=response;
      }
    });
    return json;
}

function loadTable(target_tbl, params) {
    if (getLang()=="es"){
        lang = loadJSON("/resources/site/js/il8n/datatable/spanish.json")
    }
    if (params==null || params == undefined){
        params={language:lang}
    }else{
        params.language=lang;
    }
    $(target_tbl).DataTable(params);
}

function getSupplier(target) {
    success=function (result,status,xhr) {
        $.each(result, function (index, field) {

            $(target).append($('<option />').val(field.code).html(field.sup_name));
        });
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", "/?classname=supplier.Get&sup_name=",success, error);
}

function loadProds(target, type){
    /*
    This is the replacement for the loadProducts on the products.js,
    if you' ve time, delete it.
     */
    success=function (result,status,xhr) {
        $.each(result, function (index, field) {
            $(target).append($('<option />').val(field.code).html(field.item_name));
        });

    
    };
    error = function (xhr,status,error){
        console.log(error("error"));
    };
    serverCall("get", "/?classname=Items.Get&item_type="+type,success, error);
}

function loadProducts(){
    url=new connection().url+"?classname=Items.Get&wrap_to=select2";
    select = $("#input_sel");
    select.parents('.bootbox').removeAttr('tabindex');
    select.select2({
                placeholder: "Colocar nombre del producto",
                minimumInputLength: 1,
                ajax: { // instead of writing the function to execute the request we use Select2's convenient helper
                    url: new connection().url+"?classname=Items.Get&wrap_to=select2",
                    dataType: 'json',
                    quietMillis: 250,
                    data: function (term, page) {
                        return {
                            item_name: term.term, // search term
                        };
                    },
                    results: function (data, page) { // parse the results into the format expected by Select2.
                        // since we are using custom formatting functions we do not need to alter the remote JSON data
                        return { results: data.items };
                    },
                    cache: true
                },

                id: function(bond){ console.log(bond); return bond.id; },
                text:function(bond){ return bond.text+"-"+bond.tpname; }
                //escapeMarkup: function (m) { return m; } // we do not want to escape markup since we are displaying html in results
            });

}



function loadCategories(target) {
    $.ajax({
        url: '/?classname=Categories.Get&cat_type=61',
        type: 'get',
        processData: false,
        contentType: false,
        success: function (data) {
            $(target).empty().append("<option value='0'>Seleccione uno</option>");
            $.each(data, function(index, piece){
                htmlStr="<option value='"+piece.code+"'>"+piece.cat_name+"</option>";
                $(target).append(htmlStr);
            });
        }
    });
}

function loadProfile() {
    var profile={};
    success=function (result,status,xhr) {
        profile.type=result[0].type;
        profile.name=result[0].name;
        profile.username=result[0].username;
        profile.code=result[0].code;
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", "/?classname=login.getUsersBy",success, error, false);
    return profile;
}