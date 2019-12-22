$(document).ready(function() {

    $("#add_module_group_form").submit(function(event){
        event.preventDefault();

        var data = {
            "classname": "login.addGroupMenu",
            "group_name": $("#group_name").val(),
            "icon": $("#icon").val()
        }

        var callbackAdd = function(data, status){

            if (JSON.parse(data).code) {
                $("#add_module_group_form").find("input").val('');
                $("#add_module_group_form").find("select").val('').trigger("change");
            } else {
                $("#error_alert").removeClass("hidden");
                $("#success_alert").addClass("hidden");
            }
        }

        sugelico.postServerCall(data, callbackAdd, "/");
    });

    // LOAD ALL MODULES GROUPS
    var getGroupModulesCallback = function (data, status){
        if(data){
            var currentTable;
            var editDeleteBtnTemplate = '<button class="btn btn-success edit_module_group left" data-id="\{id\}" ' +
                'data-toggle="modal" data-target="#edit_module_group"><i class="fa fa-pencil"></i></button>' +
                                        '<button class="btn btn-default delete_module_group" data-id="\{id\}" ' +
                'data-toggle="modal" data-target="#delete_module_group"><i class="fa fa-remove">' +
                '</i></button>';

            if ($('#module_group_table').val() == "") {
                currentTable = $('#module_group_table').DataTable();
                JSON.parse(data).forEach(function(group){
                    currentTable.row.add([
                        group.code,
                        group.name,
                        editDeleteBtnTemplate.replace("\{id\}", group.code).replace("\{id\}", group.code)
                    ]).draw( false );
                });
            }



            $('#module_group_table tbody').on('click', 'button.edit_module_group', function () {
                editGroupBtnClicked($(this));
            });

            $('#module_group_table tbody').on('click', 'button.delete_module_group', function () {
                deleteGroupBtnClicked($(this));
            } );
        }

    }

    var data = {
        "classname": "login.getGroupModules",
        "name": ""
    }

    sugelico.getServerCall(data, getGroupModulesCallback);

	// EDIT MODULE GROUP
    var editGroupBtnClicked = function (currentModuleGroup) {
        var editModuleGroupModal = $("#edit_module_group");

        var callback = function (data, status) {
            console.log(data);
            console.log(status);
            editModuleGroupModal.find("#module_group_name").val("JProductos");
        }

        // console.log(data);
        var data = {
            "classname": "login.getGroupModules",
            "name": ""
        }

        sugelico.getServerCall(data, callback);

		var editModuleGroupCallback = function(data, status){
            var form = editModuleGroupModal.find("#edit_user_form");
            console.log(form.serialize());
        }

        $("#edit_module_group_btn").click(function(){
            sugelico.postServerCall({}, editModuleGroupCallback);
        });
    };

    var deleteGroupBtnClicked = function (currentModuleGroup) {
        var deleteModuleGroupModal = $("#delete_module_group");

        var deleteModuleGroupCallback = function(data, status){
            console.log("eliminado");
        }

        $("#delete_module_group_btn").click(function(){
            deleteModuleGroupModal.modal("hide");
            var data = {
                "classname":"Users.Handle",
                "status":13,
                code:14
            }
            sugelico.postServerCall(data, deleteModuleGroupCallback);
        });
    };
});
