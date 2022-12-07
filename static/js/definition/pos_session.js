// We create a class for each node within the stack
class possession_node {
    // Each node has two properties, its value and a pointer that indicates the node that follows
    constructor(value){
        this.id = value['id'];
        this.activity_calendar_event_id = value['activity_calendar_event_id'];
        this.activity_date_deadline = value['activity_date_deadline'];
        this.activity_exception_decoration = value['activity_exception_decoration'];
        this.activity_exception_icon = value['activity_exception_icon'];
        this.activity_ids = value['activity_ids'];
        this.activity_state = value['activity_state'];
        this.activity_summary = value['activity_summary'];
        this.activity_type_icon = value['activity_type_icon'];
        this.activity_type_id = value['activity_type_id'];
        this.activity_user_id = value['activity_user_id'];
        this.bank_payment_ids = value['bank_payment_ids'];
        this.cash_control = value['cash_control'];
        this.cash_journal_id = value['cash_journal_id'];
        this.cash_real_difference = value['cash_real_difference'];
        this.cash_real_expected = value['cash_real_expected'];
        this.cash_register_balance_end = value['cash_register_balance_end'];
        this.cash_register_balance_end_real = value['cash_register_balance_end_real'];
        this.cash_register_balance_start = value['cash_register_balance_start'];
        this.cash_register_difference = value['cash_register_difference'];
        this.cash_register_id = value['cash_register_id'];
        this.cash_register_total_entry_encoding = value['cash_register_total_entry_encoding'];
        this.company_id = value['company_id'];
        this.config_id = value['config_id'];
        this.crm_team_id = value['crm_team_id'];
        this.currency_id = value['currency_id'];
        this.display_name = value['display_name'];
        this.failed_pickings = value['failed_pickings'];
        this.has_message = value['has_message'];
        this.is_in_company_currency = value['is_in_company_currency'];
        this.login_number = value['login_number'];
        this.message_attachment_count = value['message_attachment_count'];
        this.message_follower_ids = value['message_follower_ids'];
        this.message_has_error = value['message_has_error'];
        this.message_has_error_counter = value['message_has_error_counter'];
        this.message_has_sms_error = value['message_has_sms_error'];
        this.message_ids = value['message_ids'];
        this.message_is_follower = value['message_is_follower'];
        this.message_main_attachment_id = value['message_main_attachment_id'];
        this.message_needaction = value['message_needaction'];
        this.message_needaction_counter = value['message_needaction_counter'];
        this.message_partner_ids = value['message_partner_ids'];
        this.message_unread = value['message_unread'];
        this.message_unread_counter = value['message_unread_counter'];
        this.move_id = value['move_id'];
        this.my_activity_date_deadline = value['my_activity_date_deadline'];
        this.opening_notes = value['opening_notes'];
        this.order_count = value['order_count'];
        this.order_ids = value['order_ids'];
        this.payment_method_ids = value['payment_method_ids'];
        this.picking_count = value['picking_count'];
        this.picking_ids = value['picking_ids'];
        this.rescue = value['rescue'];
        this.sequence_number = value['sequence_number'];
        this.start_at = value['start_at'];
        this.state = value['state'];
        this.statement_ids = value['statement_ids'];
        this.stop_at = value['stop_at'];
        this.total_payments_amount = value['total_payments_amount'];
        this.update_stock_at_closing = value['update_stock_at_closing'];
        this.user_id = value['user_id'];
        this.website_message_ids = value['website_message_ids'];
        
    }
}

// We create a class for the stack
class POSSession {
    // The stack has three properties, the first node, the last node and the stack size
    constructor(){
        this.possession_current = null;// Can be the last value too or the current search
        this.possessions=[]
        
    }
    // The push method receives a value and adds it to the "top" of the stack
    push(val){
        this.possession_current = new possession_node(val);
        this.possessions.push(this.possession_current);
        
    }
    // The pop method eliminates the element at the "top" of the stack and returns its value
    popByName(name){
        let self=this;
        self.possession_current=null;
        this.possessions.forEach(function(value, index){
           if (name === value.name){self.possessions.pop(value);} 
        });
    }
    searchByName(name){
        let self=this;
        self.possession_current=null;
        this.possessions.forEach(function(value, index){
           if (name === value.name){self.possession_current=value;} 
        });
        return this.possession_current;

    }


    searchById(posconfig){
        let self=this;
        self.possession_current=null;
        this.possessions.forEach(function(value, index){
           if (parseInt(posconfig) === value.id){self.possession_current=value;} 
        });
        return this.possession_current;

    }
    
    searchByPosConfig(id){
        let self=this;
        self.possession_current=null;
        this.possessions.forEach(function(value, index){
            if (parseInt(id) === value.config_id[0]){self.possession_current=value;} 
        });
        return this.possession_current;

    }
}
