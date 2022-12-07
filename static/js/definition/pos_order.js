// We create a class for each node within the stack
class ordernode {
    // Each node has two properties, its value and a pointer that indicates the node that follows
    constructor(value){
        this.id = value['id'];
        this.name = value['name'];
        this.session_id = value['session_id'];
        this.date_order = value['date_order'];
        this.refunded_orders_count = value['refunded_orders_count'];
        this.account_move = value['account_move'];
        this.failed_pickings = value['failed_pickings'];
        this.picking_type_id = value['picking_type_id'];
        this.margin=value['margin'];
        this.l10n_do_is_return_order=value['l10n_do_is_return_order'];
        this.procurement_group_id = value['procurement_group_id'];
        this.pricelist_id = value['pricelist_id'];
        this.l10n_latam_use_documents = value['l10n_latam_use_documents'];
        this.is_invoiced = value['is_invoiced'];
        this.partner_id=value['partner_id'];
        this.cashier=value['cashier'];
        this.company_id=value['company_id'];
        this.pos_reference=value['pos_reference'];
        this.user_id = value['user_id'];
        this.crm_team_id = value['crm_team_id'];
        this.refunded_order_ids = value['refunded_order_ids'];
        this.session_move_id = value['session_move_id'];
        this.l10n_latam_sequence_id=value['l10n_latam_sequence_id'];
        this.refund_orders_count=value['refund_orders_count'];
        this.l10n_latam_document_number=value['l10n_latam_document_number'];
        this.l10n_do_payment_credit_note_ids=value['l10n_do_payment_credit_note_ids'];
        this.to_ship=value['to_ship'];
        this.create_date=value['create_date'];
        this.l10n_do_ncf_expiration_date = value['l10n_do_ncf_expiration_date'];
        this.l10n_latam_country_code = value['l10n_latam_country_code'];
        this.note = value['note'];
        this.session_move_id = value['session_move_id'];
        this.payment_ids=value['payment_ids'];
        this.customer_count=value['customer_count'];
        this.amount_total=value['amount_total'];
        this.sale_journal=value['sale_journal'];
        this.config_id = value['config_id'];
        this.nb_print = value['nb_print'];
        this.invoice_group = value['invoice_group'];
        this.amount_return = value['amount_return'];
        this.l10n_do_origin_ncf=value['l10n_do_origin_ncf'];
        this.tip_amount=value['tip_amount'];
        this.sequence_number = value['sequence_number'];
        this.to_invoice = value['to_invoice'];
        this.is_refunded = value['is_refunded'];
        this.display_name = value['display_name'];
        this.state=value['state'];
        this.margin_percent=value['margin_percent'];
        this.employee_id = value['employee_id'];
        this.picking_count = value['picking_count'];
        this.sale_order_count = value['sale_order_count'];
        this.lines = value['lines'];
        this.is_tipped=value['is_tipped'];
        this.fiscal_position_id=value['fiscal_position_id'];
        this.is_total_cost_computed = value['is_total_cost_computed'];
        this.amount_paid = value['amount_paid'];
        this.picking_ids = value['picking_ids'];
        this.table_id = value['table_id'];
        this.currency_rate=value['currency_rate'];
        this.l10n_do_return_order_id=value['l10n_do_return_order_id'];
        this.has_refundable_lines = value['has_refundable_lines'];
        this.l10n_do_return_status=value['l10n_do_return_status'];
        this.multiprint_resume=value['multiprint_resume'];
        
    }
}

// We create a class for the stack
class Order {
    // The stack has three properties, the first node, the last node and the stack size
    constructor(){
        this.order_current = null;// Can be the last value too or the current search
        this.orders=[]
        
    }
    // The push method receives a value and adds it to the "top" of the stack
    push(val){
        this.order_current = new ordernode(val);
        this.orders.push(this.order_current);
        
    }
    // The pop method eliminates the element at the "top" of the stack and returns its value
    popByName(name){
        let self=this;
        self.order_current=null;
        this.orders.forEach(function(value, index){
           if (name === value.name){self.orders.pop(value);} 
        });
    }
    searchByName(name){
        let self=this;
        self.order_current=null;
        this.orders.forEach(function(value, index){
           if (name === value.name){self.order_current=value;} 
        });
        return this.order_current;

    }
    
    popById(id){
        let self=this;
        self.order_current=null;
        this.orders.forEach(function(value, index){
           if (id === value.id){self.orders.pop(value);} 
        });
    }
    searchById(id){
        let self=this;
        self.order_current=null;
        this.orders.forEach(function(value, index){
           if (id === value.id){self.order_current=value;} 
        });
        return this.order_current;

    }

    searchByNCF(ncf){
        let self=this;
        self.order_current=null;
        this.orders.forEach(function(value, index){
           if (ncf === value.l10n_latam_document_number){self.order_current=value;} 
        });
        return this.order_current;

    }
    
}
