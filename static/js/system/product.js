/**
 * Created by hidura on 4/29/2016.
 */
//Create newArea
var server_cls="Items";
function add(){
    success=function (result,status,xhr) {
        $("#code").val(result.code);
        $("#switch").prop("checked",true);
    };
    error = function (xhr,status,error){
        console.log(error("error"));
    };
    serverCall("get", "/?classname=Items.create&name=",success, error);

}
//Save Area
function save() {
    var wparams={};
    wparams.classname="Items.Handle";
    wparams.item_name=$("#item_name").val();
    wparams.description=$("#description").val();


    wparams.code=$("#code").val();
    wparams.item_type=$("#item_type").val();
    wparams.unit=$("#unit").val();
    wparams.supplier=$("#supplier").val();
    wparams.barcode=$("#barcode").val();
    wparams.category=$("#product_cat").val();
    wparams.amount=$("#amount").val();
    if (wparams.item_type==41 || wparams.item_type==40){
        wparams.price=$("#price").val();
        wparams.tax=$("#tax").val();
        wparams.subtotal=$("#subtotal").val();
    }
    success=function (result,status,xhr) {

        $("input").val("");
        $("#amount").val("0");
        $($("select").children()[0]).prop("selected", true);
        $("#status").prop("checked", false);

        
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", wparams,success, error,false);
}

//Load all areas.
function loadTable() {
    var params={};
    params.classname=server_cls+".Get";
    params.item_name="";
    
    success=function (result,status,xhr) {
        $("#item_tbd").empty();
        $.each(result, function (index, field) {
            tr = document.createElement("tr");
            $(tr).append($('<td />').val(field.code).html(field.code));
            $(tr).append($('<td />').val(field.item_name).html(field.item_name));
            $(tr).append($('<td />').val(field.code).html(field.tpname));
            $(tr).append($('<td />').val(field.status).html(field.status_name));
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
//Edif area
function edit(target){
    //Calling the loadByCode function
    loadByCode($(target).parent().parent().children()[0].textContent);//Sending the id of the area.
    $(".bootbox-close-button").click();
}


//Load By Code
function loadByCode(code){
    if (code!=undefined && code!=null && code!=""){
        var params={};
        params.classname=server_cls+".Get";

        params.code=code;
        success=function (result,status,xhr) {
            $.each(result, function (index, field) {

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
        serverCall("post", termparams,termsuccess, error, false);
    }
    
}
function payTypeChg(target){
    if($(target).val()==41 || $(target).val()==40){
        $("#price_div").slideDown('fast');
        $("#recipe_div").slideUp("fast");
    }
    else if($(target).val()==42){
        $("#price_div").slideUp('fast');
        $("#recipe_div").slideUp("fast");
    }
    
    if($(target).val()==40){
        $("#recipe_div").slideDown("fast");
    }
}
//Default
function setByDefault() {
    var code = app.getParameterByName("code");
    if (code!=null || code.length >0 || code != ""){

        loadByCode(code);
    }
}

function getTotal(e) {
    if($("#subtotal").val()!=undefined){
        tax = parseFloat($("#subtotal").val())*(parseFloat($("#per_tax").val()/100));
        $("#tax").val(tax.toFixed(2));
        
    }else{
        $("#tax").val("0.00");
    }
    var total=parseFloat($("#subtotal").val())+parseFloat($("#tax").val());
    
    $("#price").val(total.toFixed(2));
}

function search_item() {
    var table="<div class='row'>" +
        "<div class='col-md-4'>" +
        "<div class='form-group'>" +
        "<label id='product_type_lbl'>Tipo de producto</label><select id='product_type' name='product_type' class='form-control' >" +
        "<option value='' disabled>Tipo</option></select></div>" +
        "</div>" +
        "<div class='col-md-4'>" +
        "<div class='form-group'>" +
        "<label id='product_type_lbl'>Nombre</label><input type='text' id='prod_name_search' name='prod_name_search' class='form-control' />" +
        "</div>" +
        "</div>" +

        "<div class='col-md-2'><br/>" +
        "<button class='btn btn-primary' onClick='search(); return false;'><i class='fa fa-search'></i>		</button></div></div>" +
        "<table id='items_tbl' class='table table-bordered'>" +
        "<thead>" +
        "<tr>" +
        "<th>Codigo</th>" +
        "<th>Nombre</th>" +
        "<th>Tipo</th>" +
        "<th>Categoria</th>" +
        "<th></th>" +
        "</tr>" +
        "</thead>" +
        "<tbody id='item_tbd'></tbody>" +
        "</table>";
    buttons={
        
    };
    openDialog("Busqueda de Item", table, buttons, 'large');
    //loadTable();

    getTypes($("#product_type"), 4);
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
    buttons={

    };
    openDialog("Crear Receta", table, buttons, "large");

    $("#input_sel").select2();

    loadProductsRecipe();
    loadRecipe();
    getTypes("#unit_ins",5);
}
function loadProductsRecipe(){
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

function saveRecepie(target) {
    var params={};
    params.classname=server_cls+".addItemRecipe";
    params.recipe = $("#code").val();
    params.item = $("#input_sel").val();
    params.amount = $("#ins_amount").val();
    params.unit = $("#unit_ins").val();
    success=function (result,status,xhr) {
        $("#input_sel").val(1);
        $("#ins_amount").val("");
        $("#unit_ins").val(0);

        loadRecipe();
    };
    error = function (xhr,status,error){
        console.log(error("error"));
    };
    serverCall("post", params,success, error, false);
}

function loadRecipe() {
    success=function (result,status,xhr) {
        $("#recipe_items").empty();
        $.each(result, function (index, field) {
            console.log(result);
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
    serverCall("get","/?classname=Items.getItemRecipe&item="+$("#code").val(), success, error, false);
}

function delItemRec(target) {
    var tr = $(target).parent().parent();
    var delCode=$(tr).children()[0].textContent;
    success=function (result,status,xhr) {
        $(tr).remove();
    };
    error = function (xhr,status,error){
        console.log(error("error"));
    };
    serverCall("get","/?classname=Items.delItemRecipe&code="+delCode, success, error, false);
}

//Default
function setByDefault() {
    code = getParameterByName("code");
    if (code!=null){
        loadByCode(code);
    }
}

//Creating Categories
function newCat(target) {
    var msg = "" +
        "<div class='row'>" +
            "<div class='col-md-12'>" +
                "<div style='text-align:right;'>" +
                    "<label class='control-label' id='product_name_lbl'>Estado</label><br/>" +
                    "<input id='cat_status' name='cat_status' type='checkbox'/>" +
                "</div>" +
            "</div>" +
            "<div class='col-md-8'>" +
                "<div class='form-group'>" +
                    "<input id='cat_code' name='cat_code' value='0' readonly class='form-control' placeholder='Codigo'/>" +
                "</div>" +
            "</div>" +
            "<div class='col-md-5'>" +
                "<div class='form-group'>" +
                    "<input id='cat_name' name='cat_name' class='form-control' placeholder='Nombre'/>" +
                "</div>" +
            "</div>" +
            "<div class='col-md-5'>" +
                "<div class='form-group'>" +
                    "<select id='cat_type' name='cat_type' class='form-control' >" +
                        "<option value=''>--Tipo de categoria--</option>" +
                    "</select>" +
                "</div>" +
            "</div>" +
            "<div class='col-md-6' style='text-align: left;'>" +
                "<button onClick='addCategory();' class='btn btn-primary'>" +
                    "<i class='fa fa-plus'></i> Nuevo</button>" +
            "</div>" +
            "<div class='col-md-10'>" +
                "<table class='table table-responsive'>" +
                    "<thead>" +
                        "<tr>" +
                            "<th></th>" +
                            "<th>Nombre</th>" +
                            "<th>Estado</th>" +
                            "<th>Tipo</th>" +
                        "</tr>" +
                    "</thead>" +
                    "<tbody id='cat_body'></tbody>"+
                "</table>" +
            "</div>" +
        "</div>";
    
    var buttons={};
    openDialog("Manejador de categorias", msg, buttons, 'large');
    getCategories();
    getTypes($("#cat_type"), 6);
}

function addCategory() {
    var wparams={};
    wparams.classname="Categories.create";
    var code=parseInt($("#cat_code").val());
    if (code>0){
        wparams.classname="Categories.Handle";
        wparams.code=code;
    }
    wparams.cat_name=$("#cat_name").val();
    wparams.cat_type=$("#cat_type").val();
    wparams.status=12;

    if ($("#cat_status").is(':checked')==true){
        wparams.status=11;
    }
    success=function (result,status,xhr) {
        getCategories();
        $("#cat_code").val("0");
        $("#cat_name").val("");
        $("#cat_status").prop("checked", false);
        $("#product_cat").append($('<option />').val(result.code).html(wparams.cat_name));
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post",wparams, success, error, false);
}

function getCategories() {
    success=function (result,status,xhr) {
        $("#cat_body").empty();
        $.each(result, function (index, field) {
            var tr = document.createElement("tr");
            $(tr).append($('<td />').val(field.code).html(field.code));
            $(tr).append($('<td />').val(field.cat_name).html(field.cat_name));
            $(tr).append($('<td />').val(field.status_name).html(field.status_name));
            $(tr).append($('<td />').val(field.cat_tpname).html(field.cat_tpname));
            $(tr).append($('<td />').html("<button onClick='editCat(this);' class='btn btn-info'>" +
                "<i class='fa fa-edit'></i></button>"));
            $("#cat_body").append(tr);
        });
    };
    error = function (xhr,status,error){
        console.log(error("error"));
    };
    serverCall("get","/?classname=Categories.Get&cat_name=", success, error, false);
}

function editCat(target) {
    cat_code=$(target).parent().parent().children()[0].textContent;
    success=function (result,status,xhr) {
        $.each(result, function (index, field) {
            if(field.status==11){
                $("#cat_status").prop("checked", true);
            }
            $("#cat_code").val(field.code);
            $("#cat_name").val(field.cat_name);
            $("#cat_type").val(field.cat_type);
            
        });
    };
    error = function (xhr,status,error){
        console.log(error("error"));
    };
    serverCall("get","/?classname=Categories.Get&code="+cat_code, success, error, false);
    
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
    openDialog("Manejador de fotos", msg, buttons);

    
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
    var msg = "" +
        "<form id='image_form'>" +
            "<table  class='table table-bordered'>"+
                    "<thead>"+
                        "<tr>"+
                            "<th>Nombre</th>"+
                            "<th>Seleccionar</th>"+
                        "</tr>"+
                    "</thead>"+
                    "<tbody id='tblterms'>"+
                        "<tr>"+
                            "<td>Vuelta y vuelta</td>"+
                            "<td>"+
                                "<input name='term' type='checkbox' id='term1' value='3'/>"+
                            "</td>"+
                        "</tr>"+
                        "<tr>"+
                            "<td>Rojo o ingles</td>"+
                            "<td>"+
                                "<input name='term' type='checkbox' id='term2' value='4'/>"+
                            "</td>"+
                        "</tr>"+
                        "<tr>"+
                            "<td>Termino medio</td>"+
                            "<td>"+
                                "<input name='term' type='checkbox' id='term3' value='5'/>"+
                            "</td>"+
                        "</tr>"+
                        "<tr>"+
                            "<td>Tres cuartos</td>"+
                            "<td>"+
                                "<input name='term' type='checkbox'  id='term4' value='6'/>"+
                            "</td>"+
                        "</tr>"+
                        "<tr>"+
                            "<td>Bien cocido</td>"+
                            "<td>"+
                                "<input name='term' type='checkbox'  id='term5' value='7'/>"+
                            "</td>"+
                        "</tr>"+
                        "<tr>"+
                            "<td>Frozen</td>"+
                            "<td>"+
                                "<input name='term' type='checkbox'  id='term6' value='8'/>"+
                            "</td>"+
                            "<td>Solo para jugos</td>"+
                        "</tr>"+
                        "<tr>"+
                            "<td>Normal</td>"+
                            "<td>"+
                                "<input name='term' type='checkbox'  id='term7' value='9'/>"+
                            "</td>"+
                            "<td>Solo para jugos</td>"+
                        "</tr>"+
                    "</tbody>"+
                "</table>"+
                "<div class='col-md-3'>" +
                    "<button onclick='saveTerms(this); return false;' class='fa fa-2x fa-save btn btn-info'></button>" +
                "</div>"+
        "</form>" ;

    var buttons={};
    app.openDialog("Manejador de terminos", msg, buttons, 'large');
    var sugLst =$("#terms_hist").val().split(",");
    $.each(sugLst, function (index, value) {
        $("input[value='"+value+"']").prop('checked', true);
    });
}

function saveTerms(target) {
    var params={};
    params.classname=server_cls+".add2term";
    params.product=$("#code").val();

    var terms=$("#tblterms input:checkbox:checked").map(function(){
      return $(this).val();
    }).get(); // <----
    params.terms=terms.toString();
    success=function (result,status,xhr) {
        $(".bootbox-close-button").click();
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", params,success, error, false);

}
/*
Companions area
 */
function addCompanions(target) {
    var msg = "<div class='col-lg-5 form-group'>"+
                        "<span class='col-sm-2 control-label'>Categoria</span>"+
                            "<select name='optCategories' " +
        "onChange='categorycompChange(this); return false;' " +
                                    "id='optCategories' class='form-control' >"+
                                "<option value='0'>Seleccione uno</option>"+
                            "</select>"+
                    "</div>"+
                    "<div class='col-md-5 form-group'>"+
                        "<span class='col-sm-8 control-label'>Ciclos de elección</span>"+
        "<input name='cycles' id='cycles' value='1' class='form-control' type='number'/>"+
        "</div>"+"<table class='table table-bordered'>"+
        "<thead>"+"<tr>"+"<th>Codigo</th>"+"<th>Nombre</th>"+"</tr>"+"</thead>"+
        "<tbody id='tbdcompanions'>"+"</tbody>"+"</table>"+
        "<br/>"+"<button onclick='saveCompanions(this);' class='fa fa-2x fa-save btn btn-info'></button>";

    var buttons={};
    app.openDialog("Manejador de Guarniciones", msg, buttons, "large");
        $.ajax({
        url: '/?classname=Categories.Get&cat_type=61',
        type: 'get',
        processData: false,
        contentType: false,
        success: function (data) {
            $("#optCategories").empty().append("<option value='0'>Seleccione uno</option>");
            $.each(data, function(index, piece){
                htmlStr="<option value='"+piece.code+"'>"+piece.cat_name+"</option>";
                $("#optCategories").append(htmlStr);
            });
        }
    });


}


function saveCompanions(target) {
    var params={};
    params.classname=server_cls+".addAdditional";
    params.product=$("#code").val();

    var additional=$("#tbdcompanions input:checkbox:checked").map(function(){
      return $(this).val();
    }).get(); // <----
    console.log(additional.toString());
    params.additional=additional.toString();
    params.cycle=$("#cycles").val();
    success=function (result,status,xhr) {
        $(".bootbox-close-button").click();
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", params,success, error, false);

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
        "<br/>"+"<button onclick='saveOptions(this);' class='fa fa-2x fa-save btn btn-info'></button>";

    var buttons={};
    app.openDialog("Manejador de Opciones", msg, buttons, "large");
    loadCategories($("#optCategories")[0]);


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


function categoryChange(target) {
    var sugLst ="".split(",");
    // if ($("#companions").val().toString().length>0)
    //     sugLst = $("#companions").val().toString().split(",");
    $.ajax({
        url: '/?classname=Items.Get&category='+$(target).val(),
        type: 'get',
        processData: false,
        contentType: false,
        success: function (data) {
            $("#tbdadditional").empty();
            $.each(data, function(index, piece){
                htmlStr="<tr style='text-align: center'><td>";
                htmlStr+=piece.code+"</td>";
                htmlStr+="<td>"+piece.item_name+"</td>";
                if (piece.price!=null){
                    htmlStr+="<td>"+piece.price+"</td>";
                }else {
                    htmlStr+="<td>0.00</td>";
                }
                if (sugLst.indexOf(""+piece.code)>=0)
                    htmlStr+="<td><input value='"+piece.code+"' name='additional' " +
                        "type='checkbox' checked/></td>";
                else
                    htmlStr+="<td><input value='"+piece.code+"' name='additional' " +
                        "type='checkbox' /></td>";
                htmlStr+="</tr>";
                $("#tbdadditional").append(htmlStr);
            });
        }
    });
}

function categorycompChange(target) {
    var sugLst =$("#additionals_hist").val().split(",");
    // if ($("#companions").val().toString().length>0)
    //     sugLst = $("#companions").val().toString().split(",");
    $.ajax({
        url: '/?classname=Items.Get&category='+$(target).val(),
        type: 'get',
        processData: false,
        contentType: false,
        success: function (data) {
            $("#tbdcompanions").empty();
            $.each(data, function(index, piece){
                htmlStr="<tr style='text-align: center'><td>";
                htmlStr+=piece.code+"</td>";
                htmlStr+="<td>"+piece.item_name+"</td>";
                if (piece.price!=null){
                    htmlStr+="<td>"+piece.price+"</td>";
                }else {
                    htmlStr+="<td>0.00</td>";
                }
                if (sugLst.indexOf(""+piece.code)>=0)
                    htmlStr+="<td><input value='"+piece.code+"' name='additional' " +
                        "type='checkbox' checked/></td>";
                else
                    htmlStr+="<td><input value='"+piece.code+"' name='additional' " +
                        "type='checkbox' /></td>";
                htmlStr+="</tr>";
                $("#tbdcompanions").append(htmlStr);
            });
        }
    });
}



function addCompounds(target) {

}