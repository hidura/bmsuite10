var types={};

var sugelico = {
    route:"/",
    type:types,
    postServerCall: function(data, callback, route, header) {
        if (header===undefined || header===null){
            header={}
        }
        if (route===undefined  || route===null){
            route="/";
        }
        $.ajax({
                headers:header,
                url: route,
                data: JSON.stringify(data),
                contentType: "application/json",
                type: 'POST',
                success: callback
            }
        );
    },
    postSyncServerCall: function(data, callback) {
        $.ajax({
                url: sugelico.route,
                data:  JSON.stringify(data),
                contentType: "application/json",
                type: 'POST',
                success: callback
            }
        );
    },
    postFormServerCall: function(data, callback, route) {
        if (route===undefined){
            route="";
        }
        $.ajax({
                url: sugelico.route+route,
                data: data,
                processData: false,
                contentType: false,
                type: 'POST',
                success: callback
            }
        );
    },
    getServerCall: function(data, callback) {
        $.get(sugelico.route+"?", data, callback);
    },
    openDialog:function (title, message, buttons, classname, afterload){
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
                if (afterload!==undefined){
                    afterload()
                }

        },
   
    getCookie:function(cname)
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
},
    
    numberWithCommas:function (x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
    numberWithOutCommas:function (x) {
        return x.toString().replace(",", "");
    },

    getParameterByName:function(name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(location.search);
        return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    },
    getSelectedValue:function (select) {
            var result = {};
            var options = select && select.options;
            var opt;

            for (var i=0, iLen=options.length; i<iLen; i++) {
                opt = options[i];

                if (opt.selected) {
                    result[opt.value] = opt.text;
                }
            }
            return result;
    }, getSHAOdooText: function(){
        sha1(new Date());
        var hash = sha1.create();
        hash.update(new Date());
        return hash.hex();

    },getNumPad: function(){
       return "<div class='col-md-6'><div class='row'>\
                    <input type='text' disabled='disabled' id='amount_to_pick' value=''/>\
                </div>\
       <table>\
            <tbody>\
                    <tr>\
                        <td><button class='btn btn-primary' onclick='setAmount(1)'>1</button></td>\
                        <td><button class='btn btn-primary' onclick='setAmount(2)'>2</button></td>\
                        <td><button class='btn btn-primary' onclick='setAmount(3)'>3</button></td>\
                    <tr>\
                        <td><button class='btn btn-primary' onclick='setAmount(4)'>4</button></td>\
                        <td><button class='btn btn-primary' onclick='setAmount(5)'>5</button></td>\
                        <td><button class='btn btn-primary' onclick='setAmount(6)'>6</button></td>\
                    </tr>\
                    <tr>\
                        <td><button class='btn btn-primary' onclick='setAmount(7)'>4</button></td>\
                        <td><button class='btn btn-primary' onclick='setAmount(8)'>5</button></td>\
                        <td><button class='btn btn-primary' onclick='setAmount(9)'>6</button></td>\
                    </tr>\
                    <tr>\
                        <td><button class='btn btn-primary' onclick='setAmount(0)'>0</button></td>\
                        <td><button class='btn btn-primary' onclick='setAmount('.')'>.</button></td>\
                        <td><button class='btn btn-primary' onclick='delAmount()'><i class='fa-solid fa-delete-left'></i></button></td>\
                    </tr>\
                </tbody>\
        </table>\
        <div class='row'>\
            <button type='button' onclick='addProductOrder()' class='btn btn-success btn-lg btn-block'><i class='fa-solid fa-accept'></i>Agregar</button>\
        </div></div>"
    }


    
};



// $(document).ready(function() {

//     $("select").select2({
//             height: "40px"
//     });
    
// });
