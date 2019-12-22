function loadAccounts(target){
    url=new connection().url+"?classname=Accounts.Get&wrap_to=select2&account_name=";
    select = $(target);
    select.parents('.bootbox').removeAttr('tabindex');
    select.select2({
                placeholder: "Colocar nombre de la cuenta",
                minimumInputLength: 1,
                ajax: { // instead of writing the function to execute the request we use Select2's convenient helper
                    url: new connection().url+"?classname=Accounts.Get&wrap_to=select2&account_name=",
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
                text:function(bond){ return bond.text; }
                //escapeMarkup: function (m) { return m; } // we do not want to escape markup since we are displaying html in results
            });

}
loadAccounts($("#from_acc")[0]);
loadAccounts($("#to_acc")[0]);