$(function () {
	// GET ALL CATEGORIES
	if ($('#categories_table').val() == "") {
		loadTable();
	}




	// ADD CATEGORY FORM



	sugelico.getServerCall({"classname": "Types.Get","level": 6}, function(data, status){
		var type_options = '<option value="">Seleccione tipo</option>';

		JSON.parse(data).forEach(function(category_type){
			type_options += '<option value="'+ category_type.code +'">'+ category_type.tpname +'</option>';
		});

		$("#type").html(type_options);
	});

	//Loading company to the categories

	sugelico.getServerCall({"classname": "Company.Get","_name": ""}, function(data, status){
		cont =0;
		JSON.parse(data).forEach(function(company){
			$("#company").append($('<option />').val(company.code).html(company._name));
		});

	});

	sugelico.getServerCall({"classname": "Types.Get","level": 13}, function(data, status){
		var product_options = '<option value="">Seleccione tipo producto</option>';

		JSON.parse(data).forEach(function(product_type){
			product_options += '<option value="'+ product_type.code +'">'+ product_type.tpname +'</option>';
		});

		$("#type_product").html(product_options);
		$("#product_type").html(product_options);
	});

	sugelico.getServerCall({"classname": "General.getPrinters","brand": ""}, function(data, status){
		data = JSON.parse(data);
		var printer_options = '<option value="">Seleccione printer</option>';

		JSON.parse(data).forEach(function(printer){
			printer_options += '<option value="'+ printer.code +'">'+ printer.name +'</option>';
		});

		$("#printer").html(printer_options);
	});

	// ADD NEW CATEGORY
	$("#add_category_form").submit(function(event){
		event.preventDefault();


		formData = new FormData(document.getElementById("add_category_form"));
		formData.append("classname", "Categories.create");
		sugelico.postFormServerCall(formData, function(data, status){

			if (JSON.parse(data).code) {
				$("#avatar").val("");
				$("#cat_name").val("");
				alert("Salvado");
				window.scrollTo(0.00, 0.00);

			} else {
				$("#error_alert").toggle();
				console.log(data)
			}
		});

	});

	$("#edit_category_btn").click(function(event){
		event.preventDefault();
		formData = new FormData(document.getElementById("edit_category_form"));
		formData.append("classname", "Categories.Handle");
		sugelico.postFormServerCall(formData, function(data, status){
			if (JSON.parse(data).code>0){
				$("#error_alert").addClass("hidden");
				$("#success_alert").removeClass("hidden");
				loadTable();
				$("#edit_category").modal('toggle');
			}else {
				$("#error_alert").removeClass("hidden");
				$("#success_alert").addClass("hidden");
				console.log(data)
			}
		});

	});

	$("#delete_category_btn").click(function(event){
		event.preventDefault();
		formData = new FormData();
		formData.append("code", $("#delete_code").val());
		formData.append("status", 12);
		formData.append("classname", "Categories.Handle");
		console.log(formData);
		sugelico.postFormServerCall(formData, function(data, status){
			if (JSON.parse(data).code>0){
				loadTable();
			}else {

				console.log(data)
			}
		});

	});


});
function loadTable() {
	var data = {
		"classname": "Categories.Get",
		"cat_name": ""
	}
	sugelico.getServerCall(data, function(data, status) {
		var currentTable;
		var editDeleteBtnTemplate = '<div style="width: 85px;"><button class="btn btn-success edit_category left" data-id="\{id\}" ' +
			'data-toggle="modal" data-target="#edit_category"><i class="fa fa-edit"></i></button>' +
			'<button class="btn btn-default delete_category" data-id="\{id\}" data-toggle="modal"' +
			'data-target="#delete_category"><i class="fa fa-trash"></i></button></div>';

		if ($('#categories_table').val() == "") {
			currentTable = $('#categories_table').DataTable();
			currentTable.clear().draw();
			console.log(data);
			JSON.parse(data).forEach(function (category) {
				currentTable.row.add([
					category.cat_name,
					category.product_type_name,
					category.categorytp_name,
					category.company_name,
					category.printer,
					category.status_name,
					editDeleteBtnTemplate.replace("\{id\}", category.code).replace("\{id\}", category.code)
				]).draw(false);

			});
		}
		$(".edit_category").click(function (event) {

				$("#error_alert").addClass("hidden");
				$("#success_alert").addClass("hidden");
				var data = {
					"classname": "Categories.Get",
					"code": $(this).attr("data-id")
				};
				sugelico.postServerCall(data, function(data, status){
					category=JSON.parse(data)[0];
					$("#avatar_preview").attr("src", "/resources/site/products/"+category.avatar);
					$("#code").val(category.code);
					$("#cat_name").val(category.cat_name);
					$("#type_product").val(category.type_product).trigger('change');
					$("#type").val(category.cat_type).trigger('change');
					$("#status").val(category.status).trigger('change');
					$("#company").val(category.company).trigger('change');
					$("#printer").val(category.printer_id).trigger('change');

				});
			});

		$(".delete_category").click(function (event) {
			$("#delete_code").val($(this).attr("data-id"));

		});
	});
}