$(function () {
	var gen606ReportCallback = function(data, status) {
		console.log(data);
	};

	

    $("#filters").submit(function(event){
    	event.preventDefault();
    	var data = {
	        "classname": "Accounting.get606",
	        "end_date": $("#end").val(),
	        "from_date": $("#from").val()
	    }
    	sugelico.postServerCall(data, gen606ReportCallback);
    });
});