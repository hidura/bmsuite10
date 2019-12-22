$(function () {

	//LOAD all Users
	var getUserCallBack = function (data, status) {
		if(data){
            var users_options = '<option value="">Seleccione usuario</option>';

            JSON.parse(data).forEach(function(user){
                users_options += '<option value="'+ user.code +'">'+ user.username +'</option>';
            });

            $("#user").html(users_options);
        }
	}

	var data = {
        "classname": "login.Get"
    }

	sugelico.getServerCall(data, getUserCallBack);

	// LOAD ALL MODULES GROUPS
	var getGroupModulesCallback = function (data, status){
        if(data){
            var group_options = '<option value="">Seleccione grupo</option>';

            JSON.parse(data).forEach(function(group){
                group_options += '<option value="'+ group.code +'">'+ group.name +'</option>';
            });

            $("#group").html(group_options);
        }

    }

    var data = {
        "classname": "login.getGroupModules",
        "name": ""
    }

    sugelico.getServerCall(data, getGroupModulesCallback);


    // LOAD ALL MODULES FOR A SPECIFIC MODULE GROUP
    var getModulesCallback = function (data, status){
        if(data){
            var module_options = '';

            JSON.parse(data).forEach(function(module){
                module_options += '<option value="'+ module.code +'">'+ module.name +'</option>';
            });

            $("#modules").html(module_options);
        }

    }

    $("#group").change(function(){

    	var code = $(this).val();
    	var data = {
	        "classname": "login.getModules",
	        "group": code
	    }

        if (code) {
            sugelico.getServerCall(data, getModulesCallback);
        }
    });

    $("#add_module_permmission").click(function(event){
    	event.preventDefault();

    	var addPermmisionCallback = function (data, status) {
    		if (JSON.parse(data).response == 0) {
    			$("#user").val("").trigger("change");
                $("#group").val("").trigger("change");
                $("#modules").val("").trigger("change");

                $("#error_alert").addClass("hidden");
                $("#success_alert").removeClass("hidden");
    		} else {
                $("#error_alert").removeClass("hidden");
                $("#success_alert").addClass("hidden");
            }
    	};

        var data = {
    		"classname": "login.addUserModule",
    		"user": $("#user").val(),
    		"group": $("#group").val(),
    		"group_name": document.getElementById("group").options[document.getElementById("group").selectedIndex].text,
    		"modules": sugelico.getSelectedValue(document.getElementById("modules"))
    	};
    	sugelico.postSyncServerCall(data, addPermmisionCallback);
    });

});

