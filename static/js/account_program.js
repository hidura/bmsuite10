function changemodule(target) {
    var data = {
	        "module": $("#modules").val()
	    };

    	sugelico.postServerCall(data, function(data, status) {

            console.log(data)
		}, "getfields_module");

}