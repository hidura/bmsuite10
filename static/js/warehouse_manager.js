$(function () {

	//LOAD all Categories
	var getCategoryCallBack = function (data, status) {
		if(data){
            var category_options = '<option value="">Seleccione categoría</option>';

            JSON.parse(data).forEach(function(category){
                category_options += '<option value="'+ category.code +'">'+ category.cat_name +'</option>';
            });

            $("#category").html(category_options);
            $("#category2").html(category_options);
        }
	}

	var data = {
        "classname": "Categories.Get"
    };

	sugelico.getServerCall(data, getCategoryCallBack);


	//LOAD all Warehouse manager
	var getWarehouseManagersCallBack = function (data, status) {
		if(data){
            var manager_options = '<option value="">Seleccione Almacenista</option>';

            JSON.parse(data).forEach(function(user){
                manager_options += '<option value="'+ user.code +'">'+ user.username +'</option>';
            });

            $("#warehouse_manager").html(manager_options);
        }
	}

	var data = {
        "classname": "login.Get",
        "type": 73
    }

	sugelico.getServerCall(data, getWarehouseManagersCallBack);


	// On category1 Change
	$("#category").change(function(){

		$("#products_by_category_table").dataTable().fnClearTable();

		var data = {
			"classname": "Items.Get",
        	"category": $(this).val()
		}

		var table1DataCallback = function(data, status){
			console.log(data);
			if(data){
	            var table1_rows = '';

	            JSON.parse(data).forEach(function(product){
	            	$('#products_by_category_table').dataTable().fnAddData( [
					    product.item_name+"",
					    product.amount+"",
					    product.unit_name+"",
					    ""+"" ]
					  );
	                // table1_rows += '<tr><td>'++'</td><td>'++'</td><td>'++'</td></tr>';
	            });

	            // $("#products_by_category_table_body").html(table1_rows);
	        } else {
	        	$("#products_by_category_table").dataTable().fnClearTable();
	        }
		}


		sugelico.getServerCall(data, table1DataCallback);

	});









});