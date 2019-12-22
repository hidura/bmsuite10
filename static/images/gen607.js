$(function () {

    $("#filters").submit(function(event){
    	event.preventDefault();
    	var data = {
	        "classname": "Accounting.get607",
	        "end_date": $("#end").val(),
	        "from_date": $("#from").val()
	    }
    	sugelico.postServerCall(data, function(data, status) {
			console.log(data);
		});
    });
});