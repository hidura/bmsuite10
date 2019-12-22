$(document).ready(function() {
    loadData();
});

function loadData() {
    sugelico.getServerCall("classname=Items.getTerm", function(data, status){
        var currentTable;
        var editDeleteBtnTemplate = '<button class="btn btn-success edit_product left" ' +
            'action="edit" data-id="\{id\}"' +
            ' data-toggle="modal" data-target="#edit_product"><i class="glyphicon glyphicon-pencil"></i></button>';
        currentTable = $('#term_lst').DataTable();
        currentTable.clear().draw();
        JSON.parse(data).forEach(function(term){
            currentTable.row.add([
                term._name,
                term.notes,
                editDeleteBtnTemplate.replace("\{id\}", term.code)
            ]).draw( false );

        });
        $("[data-id]").click(function (event) {
                if ($(this).attr("action")==="edit"){
                    editTerm(this);
                }
            })
        currentTable.on( 'draw', function () {
            $("[data-id]").click(function (event) {
                if ($(this).attr("action")==="edit"){
                    editTerm(this);
                }
            })
        } );


    });
}

function editTerm(target) {
    var newTerm={
        "classname":"Items.getTerm",
        "code":$(target).attr("data-id")
    };

    sugelico.postServerCall(newTerm, function(data, status){
        $("#term_name").val(JSON.parse(data[0])._name);
        $("#term_notes").val(JSON.parse(data[0]).notes);
        $("#term_code").val(JSON.parse(data[0]).code);
    });
}
function addterm(target) {

    if (parseInt($("#term_code").val())===0){
        var termdata={
            "classname":"Items.newTerm",
            "name":$("#term_name").val(),
            "notes":$("#term_notes").val()
        };
    }else{
        var termdata={
            "classname":"Items.modTerm",
            "name":$("#term_name").val(),
            "notes":$("#term_notes").val(),
            "code":$("#term_code").val()
        };
    }
    console.log(termdata);
    sugelico.postServerCall(termdata, function(data, status){
        if (JSON.parse(data).code!==undefined){
            $("#term_name").val("");
            $("#term_notes").val("");
            $("#term_code").val("0");
            loadData();
        }
    });
}