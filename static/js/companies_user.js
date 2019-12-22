var company={};
var company_send={};
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



    // LOAD ALL MODULES FOR A SPECIFIC MODULE GROUP
    var getModulesCallback = function (data, status){
        console.log(data);
        if(data){
            var module_options = '';

            JSON.parse(data).forEach(function(company_data){
                company[company_data.code]={company_id:company_data.code, name_cmp:company_data._name,
                telephone_cmp:company_data.telephone,address_cmp:company_data._address, rnc_cmp:company_data.rnc,
                otherfields_cmp:""};
                module_options += '<option value="'+ company_data.code +'">'+ company_data._name +'</option>';
            });

            $("#companies").html(module_options);
        }

    };

    $("#companies").change(function (event) {
       var companies_id=$(this).val();
       company_send={};
       companies_id.forEach(function (value) {
           company_send[parseInt(value)]=company[parseInt(value)]
       });
       console.log(company_send);
    });
    var data = {
        "classname": "Company.Get",
        "_name": ""
    }

    sugelico.getServerCall(data, getModulesCallback);


    $("#add_user_company").click(function(event){
    	event.preventDefault();

    	var addPermmisionCallback = function (data, status) {
    	    console.log(data)
    		if (JSON.parse(data).code > 0) {
    			$("#user").val("").trigger("change");
                $("#companies").val("").trigger("change");

                $("#error_alert").addClass("hidden");
                $("#success_alert").removeClass("hidden");
    		} else {
                $("#error_alert").removeClass("hidden");
                $("#success_alert").addClass("hidden");
            }
    	};
        console.log(company_send);
    	var data = {
    		"classname": "login.addCompanyUser",
    		"user": $("#user").val(),
    		"companies": JSON.stringify(company_send)
    	};
    	sugelico.postServerCall(data, addPermmisionCallback);
    });

});

