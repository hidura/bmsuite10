/**
 * Created by hidura on 4/16/2016.
 */

function loadAreas() {
    success=function (result,status,xhr) {
        $.each(result, function (index, field) {
            $("#tables_area").append($("<option/>").val(field.code).html(field.area_name));
            $("#area").append($("<option/>").val(field.code).html(field.area_name));
        })
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", "/?classname=TableArea.Get&area_name=",success, error, false);
}

function setDefaults(){
    loadAreas();
    loadTables();

}

function saveTbl(target) {
    var params=$(document.getElementById("formulary")).serializeObject();
    params.classname="Table.Handle";
    success=function (result,status,xhr) {
        td = $($("table tbody").children()[0]).children()[0];
        $(td).children("br").remove();
        var cls="";
        if (parseInt($("#tables_type").val())==1){
            cls="fa fa-circle-thin fa-5x";
        }
        else if (parseInt($("#tables_type").val())==2){
            cls="fa fa-square fa-5x";
        }
        $(td).append("<i draggable='true' id='"+$("#tables_name").val()+"' name='" +result.code+"'"+
            "ondragstart='drag(event)' class='"+cls+"'>"+$("#tables_name").val()+
            "</i>")
        
        document.getElementById("formulary").reset();
        
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", params,success, error, false);
}
function loadTables() {
    success=function (result,status,xhr) {
        $.each(result, function (index, field) {
            $("#tables_area").append($("<option/>").val(field.code).html(field.area_name))
        })
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("get", "/?classname=Table.Get&area_name=",success, error, false);

}

function searchTable(target) {
     var table="<div class='row'>" +
                    "<div class='col-md-6'>" +
                            "<div class='form-group'>" +
                                "<label id='product_type_lbl'>Area</label>" +
                                "<select id='area' name='area' class='form-control' >" +
                                    "<option value='0' disabled>Area</option>" +
                                "</select>" +
                            "</div>" +
                    "</div>" +
                "</div>";
    buttons={
        success: {
              label: "<i class='fa fa-search'></i>Buscar",
              className: "btn-success",
              callback: function() {
                    populateTable($("#area").val())

              }
        }
    };
    openDialog("Busqueda de Mesa", table, buttons);
    
    loadAreas();

}

function populateTable(area) {
    success=function (result,status,xhr) {
          $("table tbody i").remove();
          $.each(result, function (index, fields) {
              
              if (fields._position==null){
                  td = $($("table tbody").children()[0]).children()[0];
              }else{
                  td = document.getElementById(fields._position);
              }
              var cls="";
              if (fields.table_type == 1){
                    cls="fa fa-circle-thin fa-5x";
              }
              else if (fields.table_type == 2){
                    cls="fa fa-square fa-5x";
              }
              $(td).append("<i draggable='true' id='"+fields.tblname+"' name='"+fields.code +"' " +
                    "ondragstart='drag(event)' class='"+cls+"'>"+fields.tblname+
                    "</i>")
          });
    };
    error = function (xhr,status,error){
            console.log(error);
    };
    serverCall("get", "/?classname=Table.Get&tblname=&area="+area,success, error, false);
}


function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    var params={};
    params.tblname=data;
    params._position=ev.target.id;
    params.classname="Table.Handle";
    success=function (result,status,xhr) {
        ev.target.appendChild(document.getElementById(data));
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", params,success, error, false);
    
}

function createTbl(target) {
    var params={};
    params.classname="Table.create";    
    success=function (result,status,xhr) {
        document.getElementById("formulary").reset();
        $("#tables_code").val(result.code);
    };
    error = function (xhr,status,error){
        console.log(error);
    };
    serverCall("post", params,success, error, false);
}