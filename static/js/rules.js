var users=[];
$(document).ready(function() {
    if (sugelico.getParameterByName("code")!==undefined){
        var data = {
            "classname": "General.getRule"
        };
        sugelico.getServerCall(data, function(result, status) {
            $("#description").val(result[1][0].description);
            $("#rule_name").val(result[1][0].name);
            $("#description").attr("readonly","");
            $("#rule_name").attr("readonly","");
            JSON.parse(result[0]).forEach(function (user) {
                users.push(user.user_code);
                var btn=$("[data-id='"+user.user_code+"'][action='addRule']");
                $(btn.children()[0]).removeClass("glyphicon-plus");
                $(btn.children()[0]).addClass("glyphicon-check");
            });

        });

    }
    sugelico.getServerCall("classname=login.Get", function(data, status) {



        var currentTable = $('#users_lst').DataTable();
        currentTable.clear().draw();
        JSON.parse(data).forEach(function (user) {
            var classname="glyphicon-plus";
            if (users.indexOf(parseInt(user.code))>=0){
                classname="glyphicon-check";
            }
            var editDeleteBtnTemplate='<button class="btn btn-success" ' +
                'data-id="\{id\}" ' +
                'action="addRule"><i class="glyphicon '+classname+'"></i></button>';
            editDeleteBtnTemplate += '<button class="btn btn-default" ' +
                'data-id="\{id\}" ' +
                'action="delRule"><i class="glyphicon glyphicon-remove"></i></button>';
            currentTable.row.add([
                user.contact_name+user.lastname,
                user.tpname,
                editDeleteBtnTemplate.replace("\{id\}", user.code).replace("\{id\}", user.code)
            ]).draw(false);

        });
        $("[data-id]").click(function (event) {
            if ($(this).attr("action")==="addRule"){
                addRule(this);
            }else if ($(this).attr("action")==="delRule"){
                delRule(this);
            }
        });

    });


});

function addRule(target) {

    users.push($(target).attr("data-id"));
    $($(target).children()[0]).removeClass("glyphicon-plus");
    $($(target).children()[0]).addClass("glyphicon-check");
}
function delRule(target) {

    users.pop($(target).attr("data-id"));
    var btn=$($(target).parent().find(".glyphicon-check")[0]);
    btn.removeClass("glyphicon-check");
    btn.addClass("glyphicon-plus");
    console.log(users)
}

function save_data(target) {

    var data={
        "classname":(sugelico.getParameterByName("code")==="") ? "General.addRule" : "General.modRule",
        "code":sugelico.getParameterByName("code"),
        "rule_name":$("#rule_name").val(),
        "description":$("#description").val(),
        "users":JSON.stringify(users)
    };
    console.log(data);
    var saveAcccount = function (data, status) {
        if (JSON.parse(data).code===undefined){
            window.location.href="/?md=rule_add";
        }
    };


    sugelico.postServerCall(data, saveAcccount);
}