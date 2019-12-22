var terms=[];
var guarnicion=[];
var optional=[];
var recipe=[];
var compound=[];
var curCode=0;
$(document).ready(function() {
    var data = {
        "classname": "Accounts.getTax",
        "name": ""
    };
    sugelico.getServerCall(data, function(data, status){
        var taxes_option = '<option value="">Seleccione los impuestos</option>';

        JSON.parse(data).forEach(function(taxes){
            taxes_option+= '<option value="'+ taxes.code +'" data-container="'+taxes.percent+'">'+ taxes.name +'</option>';
        });

        $("#taxes").html(taxes_option);
    });
    // GET ALL PRODUCTS
    if ($('#products_table')[0]!=undefined) {
        $("#edit_product").on('hidden.bs.modal', function () {
                $(this).data('bs.modal', null);
            });
        loadProducts();
        $("#edit_product_btn").click(function(){
            formData = new FormData(document.getElementById("edit_product_form"));
            formData.append("classname", "Items.Handle");
            formData.append("code",curCode);
            formData.append("taxes_info", JSON.stringify(getSelectedTaxes()));
            formData.append("additional", JSON.stringify(guarnicion));
            formData.append("optional", JSON.stringify(optional));
            formData.append("compounds", JSON.stringify(compound));
            formData.append("terms", JSON.stringify(terms));
            formData.append("recipe", JSON.stringify(recipe));
            console.log(recipe);
            sugelico.postFormServerCall(formData, function(data, status){
                if (JSON.parse(data).code>0){
                    $("#error_alert").addClass("hidden");
                    $("#success_alert").removeClass("hidden");
                    location.reload();
                    $("#edit_product").modal('toggle');
                }else {
                    $("#error_alert").removeClass("hidden");
                    $("#success_alert").addClass("hidden");
                }
            });
            //sugelico.postServerCall({}, editProductCallback);
        });
    }

    var data = {
        "classname": "Categories.Get",
        "cat_name": ""
    }
    sugelico.getServerCall(data, function(data, status){
        var type_options = '<option value="">Seleccione categoria</option>';

        JSON.parse(data).forEach(function(category_type){

            type_options += '<option value="'+ category_type.code +'">'+ category_type.cat_name +'</option>';
        });

        $("#category").html(type_options);
    });


        var data = {
            "classname": "Types.Get",
            "level": 5
        }
        sugelico.getServerCall(data, function(data, status){
            var product_units = '<option value="">Seleccione unidad</option>';

            JSON.parse(data).forEach(function(product_unit){
                product_units += '<option value="'+ product_unit.code +'">'+ product_unit.tpname +'</option>';
            });

            $("#sale_unit").html(product_units);
        });
    
        var data = {
            "classname": "Types.Get",
            "level": 4
        }
        sugelico.getServerCall(data, function(data, status){
            var product_options = '<option value="">Seleccione tipo producto</option>';

            JSON.parse(data).forEach(function(product_type){
                product_options += '<option value="'+ product_type.code +'">'+ product_type.tpname +'</option>';
            });

            $("#item_type").html(product_options);
            $("#item_type").change(function () {
               if (parseInt($("#item_type").val())===42){
                   $("#btns_lst").hide();
                   $("#price_info").hide();
               }
               else {
                   $("#btns_lst").show();
                   $("#price_info").show();
               }
            });
        });

        var data = {
            "classname": "supplier.Get",
            "sup_name": ""
        };
        sugelico.getServerCall(data, function(data, status){
            var supplier_options = '<option value="">Seleccione Suplidor</option>';

            JSON.parse(data).forEach(function(supplier){
                supplier_options += '<option value="'+ supplier.code +'">'+ supplier.sup_name +'</option>';
            });

            $("#supplier").html(supplier_options);
        });

    $("#product_add_form").submit(function(event){
        event.preventDefault();
        calculateTax(null);
        formData = new FormData(document.getElementById("product_add_form"));
        formData.append("classname", "Items.create");
        formData.append("additional", JSON.stringify(guarnicion));
        formData.append("optional", JSON.stringify(optional));
        formData.append("compounds", JSON.stringify(compound));
        formData.append("terms", JSON.stringify(terms));
        formData.append("recipe", JSON.stringify(recipe));

        sugelico.postFormServerCall(formData, function(data, status){
            if (JSON.parse(data).code>0){
                alert("Salvado!");
                $("#amount").val("1");
                $("#subtotal").val("0");
                //$("#product_cat").val(0).change();
                $("#price").val("0.00");
                //$("#sale_unit").val(0).change();
                //$("#item_type").val(0).change();
                $("#taxes").val(0).change();

                $("#tax").val("0.00");
                $("#description").val("");
                $("#barcode").val("");
                //$("#status").val(0).change();
                //$("#category").val(0).change();
                //$("#supplier").val(0).change();
                $("#item_name").val("");
                $("#success_alert").removeClass("hidden");
            }else {
                console.log(data);
                $("#error_alert").removeClass("hidden");

            }

        });
    });


    // EDIT PRODUCT

    // Filter by type and category
    $("#filter_product_report").click(function(event) {
        event.preventDefault();
        var data = {
            "product_type": $("#product_type").val(),
            "product_cat": $("#product_cat").val()
        }

        var callback = function(data, status){
            console.log(data);
        }

        sugelico.getServerCall(data, callback);

    });
    var code = sugelico.getParameterByName("code");
    if (code!=null || code.length >0 || code !== ""){
        loadByCode(code);
    }
});
function addTax(target) {
    var e = document.getElementById("taxes");
    var tax=0.00;

    for (var i=0, len=e.options.length; i<len; i++) {
        opt = e.options[i];

        // check if selected

        if (opt.selected) {
            // add to array of option elements to return from this function
            tax+=parseFloat(opt.getAttribute("data-container"));

        }
    }
    $("#tax").val(tax);
    calculateTax(null);
}
function calculateTax(target) {
    var tax=parseFloat($("#tax").val())/100;

    var total_tax=$("#subtotal").val()*tax;
    $("#price").val(parseFloat(parseFloat(total_tax)+parseFloat($("#subtotal").val())).toFixed(2));
}
function calculatesubtotal(target) {
    var gains=parseFloat($("#gain").val())/100;
    var price_uni=parseFloat($("#initial_cost").val())/parseFloat($("#amount").val());

    var total_gain=parseFloat(price_uni*gains);
    $("#subtotal").val(parseFloat(parseFloat(total_gain)+parseFloat(price_uni)).toFixed(2));
    calculateTax(null);
}
function getSelectedTaxes() {
    var e = document.getElementById("taxes");
    var taxes=[];
    for (var i=0, len=e.options.length; i<len; i++) {
        opt = e.options[i];

        // check if selected
        if (opt.selected) {
            // add to array of option elements to return from this function
            taxes.push($(opt).val());
        }
    }
    return taxes;
}
function loadProducts() {
    var data = {
            "classname": "Items.Get",
            "item_name": ""
        };

        sugelico.postServerCall(data, function(data, status){

            var currentTable;
            var editDeleteBtnTemplate = '<button class="btn btn-success edit_product left" action="edit" ' +
                'data-id="\{id\}" data-toggle="modal" ' +
                'data-target="#edit_product"><i class="fa fa-pencil"></i></button>' +

                '<button class="btn btn-default delete_product" action="delete" data-id="\{id\}" data-toggle="modal" ' +
                'data-target="#delete_product"><i class="fa fa-trash"></i></button>';
            if ($('#products_table').val() == "") {
                currentTable = $('#products_table').DataTable();

                currentTable.clear().draw();
                if (JSON.parse(data)[0].code>0){
                    JSON.parse(data).forEach(function(product){
                        currentTable.row.add([
                            product.barcode,
                            product.item_name,
                            product.amount,
                            product.price,
                            "",
                            product.cat_name,
                            product.status_name,
                            editDeleteBtnTemplate.replace("\{id\}", product.code).replace("\{id\}", product.code)
                        ]).draw( false );

                    });
                    $("[data-id]").click(function (event) {
                            if ($(this).attr("action")==="edit"){
                                editProduct(this);
                            }
                        })
                    currentTable.on( 'draw', function () {
                        $("[data-id]").click(function (event) {
                            if ($(this).attr("action")==="edit"){
                                editProduct(this);
                            }else if($(this).attr("action")==="delete"){
                                var currentUser = $(this);
                                var deleteProductModal = $("#delete_product");

                                var deleteProductCallback = function(data, status){
                                    console.log("eliminado");
                                }
                                deleteProductModal.modal("hide");
                                var data = {
                                    "classname":"Users.Handle",
                                    "status":13,
                                    code:14
                                }
                                sugelico.postServerCall(data, deleteProductCallback);
                            }
                        })
                    } );
                }


                $("#product_cat").val("62").trigger("change");
            }



        });
}

function editProduct(target) {
    var currentPruduct = $(target);
    var editProductModal = $("#edit_product");
    var callback = function(data, status){
        product=JSON.parse(data)[0];
        product.taxes.forEach(function(tax){
           var select = document.getElementById( 'taxes' );

            for ( var i = 0, l = select.options.length, o; i < l; i++ )
            {
              o = select.options[i];
              if ( tax.tax ===parseInt($(o).val()))
              {
                o.selected = true;
              }
            }
        });
        $("#taxes").change();
        editProductModal.find("#item_name").val(product.item_name);
        editProductModal.find("#barcode").val(product.barcode);
        editProductModal.find("#amount").val(product.amount);
        editProductModal.find("#item_type").val(product.item_type).trigger("change");
        editProductModal.find("#category").val(product.category).trigger("change");
        editProductModal.find("#supplier").val(product.supplier).trigger("change");
        editProductModal.find("#status").val(product.status).trigger("change");
        editProductModal.find("#sale_unit").val(product.unit).trigger("change");
        editProductModal.find("#subtotal").val(product.subtotal);
        editProductModal.find("#tax").val(product.tax);
        editProductModal.find("#price").val(product.price);
        editProductModal.find("#description").val(product.description);
        if(product.avatar!=null){
            $("#avatar_preview").attr("src", "/resources/site/products/"+product.avatar);

        }
        curCode =product.code;
        var addparams={};
        addparams.classname="Items.getAdditional";
        addparams.product=currentPruduct.attr("data-id");
        success=function (result,status,xhr) {
            JSON.parse(result).forEach(function (index, field) {
                var additional_lst=$("#additionals_hist").val();
                if (index===0){
                    additional_lst=field.additional;
                }else {
                    additional_lst+=","+field.additional;
                }
                $("#additionals_hist").val(additional_lst);
            });

        };
        error = function (xhr,status,error){
            console.log(error);
        };
        sugelico.getServerCall(addparams,success);

        var termparams={};
        termparams.classname="Items.getTerm";
        termparams.product=currentPruduct.attr("data-id");
        termsuccess=function (result,status,xhr) {
            JSON.parse(result).forEach(function (index, field) {

                var terms_lst=$("#terms_hist").val();
                if (index===0){
                    terms_lst=field.code;
                }else {
                    terms_lst+=","+field.code;
                }
                $("#terms_hist").val(terms_lst);
            });

        };
        error = function (xhr,status,error){
            console.log(error);
        };
        sugelico.getServerCall(termparams,termsuccess);
    };

    sugelico.getServerCall({classname:"Items.Get", code:currentPruduct.attr("data-id")}, callback);


}


function addRecipe(){
    var table="" +
        "<div class='row'>" +
            "<div class='col-md-5'>	" +
                "<div class='col-lg-9'>" +
                    "<span class='control-label' id='input_lbl'>Insumo</span>" +
                    "<select id='input_sel' name='input_sel' style='width:100%' class='form-control'>" +
                    ""+
                    "</select>" +
                "</div>" +
            "</div>" +
            "<div class='form-group col-md-3'>" +
                "<div class='form-group'>" +
                    "<span class='control-label' id='amount_lbl'>Cantidad</span>" +
                    "<input type='number' id='ins_amount' name='amount' class='form-control'/>" +
                "</div>" +
            "</div>" +
            "<div class='form-group col-md-3'>" +
                "<div class='form-group'>" +
                    "<span class='control-label' id='unity_lbl'>Unidad</span>" +
                    "<select id='unit_ins' name='unit_ins' class='form-control'>" +
                        "<option value='0' disabled>Tipo</option>"+
                    "</select>" +
                "</div>" +

            "</div>" +
            "<div class='col-md-1'><br/>" +
                    "<button class='btn btn-primary' onClick='saveRecepie(this); return false;'>" +
                        "<i class='fa fa-save'></i>" +
                    "</button>" +
                "</div>" +
            "<div class='col-md-10'>" +
                "<table class='table table-responsive'>" +
                    "<thead>" +
                        "<tr>" +
                            "<th>Codigo</th>" +
                            "<th>Nombre</th>" +
                            "<th>Cantidad</th>" +
                            "<th>Tipo de unidad</th>" +
                        "</tr>" +
                    "</thead>" +
                    "<tbody id='recipe_items'></tbody>"+
                "</table>" +

            "</div>" +
        "</div>";
    var buttons={cancel: {
            label: 'Cerrar',
            className: 'btn-danger'
        }
    };
    sugelico.openDialog("Crear Receta", table, buttons, "large");


    loadProductsRecipe();
    loadRecipe();
    sugelico.getTypes("#unit_ins",5);

}
function loadProductsRecipe(){
    var data = {
        "classname": "Items.Get",
        "item_name": ""
    };
    sugelico.getServerCall(data, function(data, status){
            var taxes_option = '<option value="">Seleccione los productos</option>';

            JSON.parse(data).forEach(function(item){
                taxes_option+= '<option value="'+ item.code +'" data-container="'+item.code+'">'+ item.item_name+'</option>';
            });


            $("#input_sel").html(taxes_option);
            $("#input_sel").select2({
                    height: "40px"
            });
        });
}


function saveRecepie(target) {

    var tr = document.createElement("tr");
    $(tr).append($('<td />').val(0).html(0));
    $(tr).append($('<td />').val($('#input_sel option:selected').val()).html($('#input_sel option:selected').text()));
    $(tr).append($('<td />').val($('#ins_amount').val()).html($('#ins_amount').val()));
    $(tr).append($('<td />').val($('#unit_ins').val()).html($('#unit_ins option:selected').text()));
    $(tr).append($('<td />').html("<button onClick='delItemRec(this); return false;' " +
        "data-id='"+(recipe.length+1)+"' class='btn btn-danger'><i class='fa fa-trash'></i></button>"));
    $("#recipe_items").append(tr);

    recipe.push({product:$('#input_sel option:selected').val(), amount:$('#ins_amount').val(),
    unit:$('#unit_ins').val(), unit_name:$('#unit_ins option:selected').text(),
        item_name:$('#input_sel option:selected').text()});

    $("#input_sel").val(1);
    $("#ins_amount").val("");
    $("#unit_ins").val(0);
}

function delItemRec(target) {
    delete recipe[parseInt($(target).attr("data-id"))];
    $(target).parent().parent().remove();
    console.log(recipe);
}
function loadRecipe() {
    success=function (result,status,xhr) {
        $("#recipe_items").empty();
        $.each(result, function (index, field) {
            console.log(result)
            var tr = document.createElement("tr");
            $(tr).append($('<td />').val(field.code).html(field.code));
            $(tr).append($('<td />').val(field.item_name).html(field.item_name));
            $(tr).append($('<td />').val(field.amount).html(field.amount));
            $(tr).append($('<td />').val(field.unit).html(field.unit_name));
            $(tr).append($('<td />').html("<button onClick='delItemRec(this); return false;' class='btn btn-danger'><i class='fa fa-trash'></i></button>"));
            $("#recipe_items").append(tr);
        })
    };
    error = function (xhr,status,error){
        console.log(error("error"));
    };

    sugelico.getServerCall("classname=Items.getItemRecipe&item="+curCode, success);
}



//Load By Code
function loadByCode(code){
    if (code!=undefined && code!=null && code!=""){
        var params={};
        params.classname=server_cls+".Get";

        params.code=code;
        success=function (result,status,xhr) {
            $.each(result, function (index, field) {
                var terms=[];
                var guarnicion=[];
                var optional=[];
                var recipe=[];
                var compound=[];
                $("#code").val(field.code);
                $("#item_type").val(field.item_type);
                $("#item_type").change();
                $("#item_name").val(field.item_name);


                if (field.description!=null){
                    $("#description").val(field.description);
                }
                if (field.unit!=null){
                    $("#unit").val(field.unit);
                }
                if (field.supplier!=null){
                    $("#supplier").val(field.supplier);
                }
                $("#switch").prop("checked", false);
                if (field.status==11){

                    $("#switch").prop("checked", true);
                }
                if (field.amount!=null){
                    $("#amount").val(field.amount);
                }
                if (field.subtotal!=null){
                    $("#subtotal").val(field.subtotal);
                }
                if (field.price!=null){
                    $("#price").val(field.price);
                }
                if (field.tax!=null){
                    $("#tax").val(field.tax);
                }
                if (field.category!=null){
                    $("#product_cat").val(field.category);
                }
            });

        };
        error = function (xhr,status,error){
            console.log(error);
        };
        serverCall("post", params,success, error, false);


        var addparams={};
        addparams.classname=server_cls+".getAdditional";
        addparams.product=code;
        success=function (result,status,xhr) {
            $.each(result, function (index, field) {
                console.log(field);
                guarnicion.push(field.additional)
                var additional_lst=$("#additionals_hist").val();
                if (index===0){
                    additional_lst=field.additional;
                }else {
                    additional_lst+=","+field.additional;
                }
                $("#additionals_hist").val(additional_lst);
            });

        };
        error = function (xhr,status,error){
            console.log(error);
        };
        serverCall("post", addparams,success, error, false);

        var termparams={};
        termparams.classname=server_cls+".getTerm";
        termparams.product=code;
        termsuccess=function (result,status,xhr) {
            console.log(result)
            $.each(result, function (index, field) {
                console.log(field);
            });

        };
        error = function (xhr,status,error){
            console.log(error);
        };
        serverCall("post", termparams,termsuccess, error, false);
    }

}


function search() {
        var params={};
        params.classname=server_cls+".Get";
        params.item_type=$("#product_type").val();
        params.item_name=$("#prod_name_search").val();

        success=function (result,status,xhr) {
            $("#item_tbd").empty();
            $.each(result, function (index, field) {
                tr = document.createElement("tr");
                $(tr).append($('<td />').val(field.code).html("<a href='/?md=product&code="+field.code+"' target='_blank'>"+field.code+"</a>"));
                $(tr).append($('<td />').val(field.item_name).html(field.item_name));
                $(tr).append($('<td />').val(field.code).html(field.tpname));
                $(tr).append($('<td />').val(field.code).html(field.cat_name));
                $(tr).append($('<td />').html("<button onClick='edit(this);' class='btn btn-info'><i class='fa fa-edit'></i></button>"));

                $("#item_tbd").append(tr)
            });
            $("#items_tbl").DataTable();
        };
        error = function (xhr,status,error){
            console.log(error);
        };
        serverCall("post", params,success, error, false);

}
function addPhoto(target) {
    var msg = "" +
        "<form id='image_form'>" +
            "<div class='row'>" +
                "<div class='col-md-4'>" +
                    "<div style='text-align:right;'>" +
                        "<label class='control-label'>Foto</label><br/>" +
                        "<input id='avatar' name='avatar' onChange='uploadImage(this); return false;' type='file'/>" +
                    "</div>" +
                "</div>" +
                "<div class='col-md-10'>" +
                    "<div class='form-group'>" +
                        "<label class='control-label' >Vista-Previa</label><br/>" +
                        "<img id='photo_target' class='img-thumbnail'/>" +
                    "</div>" +
                "</div>" +
            "</div>" +
        "</form>";

    var buttons={};
    sugelico.openDialog("Manejador de fotos", msg, buttons);


}

function uploadImage(target){
    fd = new FormData(document.getElementById("image_form"));
    fd.append("classname", "Items.Handle");
    fd.append("code",$("#code").val());
    $.ajax({
            url: '/',
            data: fd,
            processData: false,
            contentType: false,
            type: 'POST',
            success: function(data){


              $("#photo_target").attr('src', "/resources/site/products"+"/"+data.avatar);

            }
        }
    );
}

function addTerms(target) {
    var html="<form id='image_form'><table  class='table table-bordered'><thead><tr><th>Nombre</th><th>Seleccionar</th></tr></thead><tbody id='tblterms'></tbody></table></form>"
    var buttons={};
    sugelico.openDialog("Manejador de terminos", html, buttons, 'large');
    sugelico.getServerCall("classname=Items.getTerm&_name=", function(data, status) {
        JSON.parse(data).forEach(function (term) {
            var tr=document.createElement("tr");
            $(tr).append($("<td/>").attr("data-id",term.code).html(term._name));
            $(tr).append($("<td/>").html($("<input type='checkbox' data-id='"+term._name+"' onClick='checkTerm(this)'/>").val(term.code)));
            $("#tblterms").append(tr);
        });
    });
}

function checkTerm(target) {
    if($(target).is(':checked')){
        var code=$(target).val();
        var name=$(target).attr("data-id");
        terms.push({code:code, name:name});
    }else {
        terms.forEach(function (term) {
            if (term.code===$(target).val()){
                var pos=terms.indexOf(term);
                delete terms[pos];
            }
        });
    }
}

/*
Companions area
 */
function addCompanions(target) {
    sugelico.getServerCall("classname=Items.getAdditional&product="+curCode, function(data, status) {
        JSON.parse(data).forEach(function (value) {
            guarnicion.push({code:value.additional, name:value.name,
            price:value.price,cycle:value.cycle});
        });

    });
    var msg = "<div class='col-lg-5 form-group'>" +
            "<span class='col-sm-2 control-label'>Categoria</span>" +
            "<select name='optCategories' " +
            "onChange='categorycompChange(this); return false;' " +
            "id='optCategories' class='form-control' >" +
            "<option value='0'>Seleccione uno</option>" +
            "</select>" +
            "</div>" +
            "<div class='col-md-5 form-group'>" +
            "<span class='col-sm-8 control-label'>Ciclos de elección</span>" +
            "<input name='cycles' id='cycles' value='1' class='form-control' type='number'/>" +
            "</div>" + "<table class='table table-bordered'>" +
            "<thead>" + "<tr>" + "<th>Codigo</th>" + "<th>Nombre</th>" + "</tr>" + "</thead>" +
            "<tbody id='tbdcompanions'>" + "</tbody>" + "</table>" +
            "<br/>";

        var buttons = {
            cancel: {
                label: 'Cerrar',
                className: 'btn-danger'
            }
        };
        afterload = function () {
            sugelico.loadCategories($("#optCategories")[0]);
        };
        sugelico.openDialog("Manejador de Guarniciones", msg, buttons, "large", afterload);
}




function saveCompanions(target) {
    guarnicion.push($(target).val());
}
/*
End companions area.
 */


/*
Otionals area.
 */
function addOptions(target) {
    var msg = "<div class='col-lg-5 form-group'>"+
                        "<span class='col-sm-2 control-label'>Categoria</span>"+
                            "<select name='optCategories' " +
        "onChange='categoryChange(this); return false;' " +
                                    "id='optCategories' class='form-control' >"+
                                "<option value='0'>Seleccione uno</option>"+
                            "</select>"+
                    "</div>"+
                    "<div class='col-md-5 form-group'>"+
                        "<span class='col-sm-8 control-label'>Ciclos de elección</span>"+
        "<input name='cycles' id='cycles' value='1' class='form-control' type='number'/>"+
        "</div>"+"<table class='table table-bordered'>"+
        "<thead>"+"<tr>"+"<th>Codigo</th>"+"<th>Nombre</th>"+"</tr>"+"</thead>"+
        "<tbody id='tbdadditional'>"+"</tbody>"+"</table>"+
        "<br/>";

    var buttons={cancel: {
            label: 'Cerrar',
            className: 'btn-danger'
        }};
    afterload = function () {
        sugelico.loadCategories($("#optCategories")[0]);
    };
    sugelico.openDialog("Manejador de Opciones", msg, buttons, "large", afterload);


}



function saveOptions(target) {
    var params={};
    params.classname=server_cls+".addOptional";
    params.product=$("#code").val();

    var additional=$("#tbdadditional input:checkbox:checked").map(function(){
      return $(this).val();
    }).get(); // <----
    params.optionals=additional.toString();
    success=function (result,status,xhr) {
        $(".bootbox-close-button").click();
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", params,success, error, false);
}


function loadAdditional(){
    $("#addCategories").empty().append("<option value='0'>Seleecione</option>");

    $("#category").children().each(function(index, element){
        if (index>0)
            $("#addCategories").append("<option value='"+$(element).attr("value")+"'>"+$(element).text()+"</option>");
    });
}


function categorycompChange(target) {
    sugelico.getServerCall('classname=Items.Get&category='+$(target).val(),
        function (data) {
            $("#tbdcompanions").empty();
            JSON.parse(data).forEach(function(piece, index){
                var htmlStr="<tr style='text-align: center'><td>";
                htmlStr+=piece.code+"</td>";
                htmlStr+="<td>"+piece.item_name+"</td>";
                if (piece.price!=null){
                    htmlStr+="<td>"+piece.price+"</td>";
                }else {
                    htmlStr+="<td>0.00</td>";
                }
                var checked="";
                guarnicion.forEach(function (value) {
                    console.log(value.code===piece.code,value.code,piece.code);
                    if (value.code===piece.code){
                        checked="checked";
                    }
                });
                htmlStr+="<td><input onClick='addGuarnicion(this)' value='"+piece.code+"' name='additional' " +
                        "type='checkbox' "+checked+"/></td>";
                htmlStr+="</tr>";
                $("#tbdcompanions").append(htmlStr);
            });
        }
    );

}

function addGuarnicion(target) {
    if ($(target).is(":checked")){
        var data =$(target).parent().parent().children();
        guarnicion.push({code:parseInt($(target).val()), name:data[1].textContent,
            price:data[2].textContent,cycle:$("#cycles").val()});
    }else {
        guarnicion.forEach(function (value) {
            if (value.code===parseInt($(target).val())){
                var pos=guarnicion.indexOf(value);
                delete guarnicion[pos];
            }
        });
    }
    console.log(guarnicion);
}



function addOptionals(target) {
    if ($(target).is(":checked")){
        var data =$(target).parent().parent().children();
        optional.push({code:parseInt($(target).val()), name:data[1].textContent,
            price:data[2].textContent,cycle:$("#cycles").val()});
    }else {
        optional.forEach(function (value) {
            if (value.code===parseInt($(target).val())){
                var pos=optional.indexOf(value);
                delete optional[pos];
            }
        });
    }
    console.log(optional);
}



function addcomp(target) {
    if ($(target).is(":checked")){
        var data =$(target).parent().parent().children();
        compound.push({code:parseInt($(target).val()), name:data[1].textContent,
            price:data[2].textContent,cycle:$("#cycles").val()});
    }else {
        compound.forEach(function (value) {
            if (value.code===parseInt($(target).val())){
                var pos=compound.indexOf(value);
                delete compound[pos];
            }
        });
    }
    console.log(compound);
}

function categoryChange(target) {
    // if ($("#companions").val().toString().length>0)
    //     sugLst = $("#companions").val().toString().split(",");
    $.ajax({
        url: '/?classname=Items.Get&category='+$(target).val(),
        type: 'get',
        processData: false,
        contentType: false,
        success: function (data) {
            $("#tbdadditional").empty();
            JSON.parse(data).forEach(function(piece, index){
                var htmlStr="<tr style='text-align: center'><td>";
                htmlStr+=piece.code+"</td>";
                htmlStr+="<td>"+piece.item_name+"</td>";
                if (piece.price!=null){
                    htmlStr+="<td>"+piece.price+"</td>";
                }else {
                    htmlStr+="<td>0.00</td>";
                }
                if (optional.indexOf(piece.code)>=0)
                    htmlStr+="<td><input onClick='addOptionals(this)' value='"+piece.code+"' name='optional' " +
                        "type='checkbox' checked/></td>";
                else
                    htmlStr+="<td><input onClick='addOptionals(this)' value='"+piece.code+"' name='optional' " +
                        "type='checkbox' /></td>";
                htmlStr+="</tr>";
                $("#tbdadditional").append(htmlStr);
            });
        }
    });
}

function categoryCompoundChange(target) {
    // if ($("#companions").val().toString().length>0)
    //     sugLst = $("#companions").val().toString().split(",");
    $.ajax({
        url: '/?classname=Items.Get&category='+$(target).val(),
        type: 'get',
        processData: false,
        contentType: false,
        success: function (data) {
            $("#tbdadditional").empty();
            JSON.parse(data).forEach(function(piece, index){
                var htmlStr="<tr style='text-align: center'><td>";
                htmlStr+=piece.code+"</td>";
                htmlStr+="<td>"+piece.item_name+"</td>";
                if (piece.price!=null){
                    htmlStr+="<td>"+piece.price+"</td>";
                }else {
                    htmlStr+="<td>0.00</td>";
                }
                if (optional.indexOf(piece.code)>=0)
                    htmlStr+="<td><input onClick='addcomp(this)' value='"+piece.code+"' name='compound' " +
                        "type='checkbox' checked/></td>";
                else
                    htmlStr+="<td><input onClick='addcomp(this)' value='"+piece.code+"' name='compound' " +
                        "type='checkbox' /></td>";
                htmlStr+="</tr>";
                $("#tbdadditional").append(htmlStr);
            });
        }
    });
}

function addCompounds(target) {
    var msg = "<div class='col-lg-5 form-group'>"+
                        "<span class='col-sm-2 control-label'>Categoria</span>"+
                            "<select name='optCategories' " +
        "onChange='categoryCompoundChange(this); return false;' " +
                                    "id='optCategories' class='form-control' >"+
                                "<option value='0'>Seleccione uno</option>"+
                            "</select>"+
                    "</div>"+
                    "<div class='col-md-5 form-group'>"+
                        "<span class='col-sm-8 control-label'>Ciclos de elección</span>"+
        "<input name='cycles' id='cycles' value='1' class='form-control' type='number'/>"+
        "</div>"+"<table class='table table-bordered'>"+
        "<thead>"+"<tr>"+"<th>Codigo</th>"+"<th>Nombre</th>"+"</tr>"+"</thead>"+
        "<tbody id='tbdadditional'>"+"</tbody>"+"</table>";

    var buttons={cancel: {
            label: 'Cerrar',
            className: 'btn-danger'
        }};
    afterload = function () {
        sugelico.loadCategories($("#optCategories")[0]);
    };
    sugelico.openDialog("Manejador de Componentes", msg, buttons, "large", afterload);


}


