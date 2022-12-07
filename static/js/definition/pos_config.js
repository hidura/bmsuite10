// We create a class for each node within the stack
class posnode {
    // Each node has two properties, its value and a pointer that indicates the node that follows
    constructor(value){
        this.id = value['id'];
        this.name = value['name'];
        this.active = value['active'];
        this.allow_product_varients = value['allow_product_varients'];
        this.allowed_pricelist_ids = value['allowed_pricelist_ids'];
        this.amount_authorized_diff = value['amount_authorized_diff'];
        this.available_pricelist_ids = value['available_pricelist_ids'];
        this.barcode_nomenclature_id = value['barcode_nomenclature_id'];
        this.cash_control = value['cash_control'];
        this.cash_rounding = value['cash_rounding'];
        this.company_has_template = value['company_has_template'];
        this.crm_team_id = value['crm_team_id'];
        this.currency_id = value['currency_id'];
        this.current_session_id = value['current_session_id'];
        this.current_session_state = value['current_session_state'];
        this.current_user_id = value['current_user_id'];
        this.default_bill_ids = value['default_bill_ids'];
        this.default_fiscal_position_id = value['default_fiscal_position_id'];
        this.display_name = value['display_name'];
        this.down_payment_product_id = value['down_payment_product_id'];
        this.employee_ids = value['employee_ids'];
        this.epson_printer_ip = value['epson_printer_ip'];
        this.fiscal_position_ids = value['fiscal_position_ids'];
        this.floor_ids = value['floor_ids'];
        this.group_pos_manager_id = value['group_pos_manager_id'];
        this.group_pos_user_id = value['group_pos_user_id'];
        this.has_active_session = value['has_active_session'];
        this.iface_available_categ_ids = value['iface_available_categ_ids'];
        this.iface_big_scrollbars = value['iface_big_scrollbars'];
        this.iface_cashdrawer = value['iface_cashdrawer'];
        this.iface_customer_facing_display = value['iface_customer_facing_display'];
        this.iface_customer_facing_display_local = value['iface_customer_facing_display_local'];
        this.iface_customer_facing_display_via_proxy = value['iface_customer_facing_display_via_proxy'];
        this.iface_display_categ_images = value['iface_display_categ_images'];
        this.iface_electronic_scale = value['iface_electronic_scale'];
        this.iface_open_product_info = value['iface_open_product_info'];
        this.iface_orderline_customer_notes = value['iface_orderline_customer_notes'];
        this.iface_orderline_notes = value['iface_orderline_notes'];
        this.iface_print_auto = value['iface_print_auto'];
        this.iface_print_skip_screen = value['iface_print_skip_screen'];
        this.iface_print_via_proxy = value['iface_print_via_proxy'];
        this.iface_printbill = value['iface_printbill'];
        this.iface_scan_via_proxy = value['iface_scan_via_proxy'];
        this.iface_splitbill = value['iface_splitbill'];
        this.iface_start_categ_id = value['iface_start_categ_id'];
        this.iface_tax_included = value['iface_tax_included'];
        this.iface_tipproduct = value['iface_tipproduct'];
        this.invoice_journal_id = value['invoice_journal_id'];
        this.is_header_or_footer = value['is_header_or_footer'];
        this.is_installed_account_accountant = value['is_installed_account_accountant'];
        this.is_order_printer = value['is_order_printer'];
        this.is_posbox = value['is_posbox'];
        this.is_table_management = value['is_table_management'];
        this.journal_id = value['journal_id'];
        this.l10n_do_credit_notes_number_of_days = value['l10n_do_credit_notes_number_of_days'];
        this.l10n_do_default_partner_id = value['l10n_do_default_partner_id'];
        this.l10n_do_number_of_days = value['l10n_do_number_of_days'];
        this.l10n_do_order_loading_options = value['l10n_do_order_loading_options'];
        this.l10n_latam_country_code = value['l10n_latam_country_code'];
        this.l10n_latam_use_documents = value['l10n_latam_use_documents'];
        this.last_session_closing_cash = value['last_session_closing_cash'];
        this.last_session_closing_date = value['last_session_closing_date'];
        this.limit_categories = value['limit_categories'];
        this.limited_partners_amount = value['limited_partners_amount'];
        this.limited_partners_loading = value['limited_partners_loading'];
        this.limited_products_amount = value['limited_products_amount'];
        this.limited_products_loading = value['limited_products_loading'];
        this.manual_discount = value['manual_discount'];
        this.module_account = value['module_account'];
        this.iface_tax_included = value['iface_tax_included'];
        this.module_pos_discount = value['module_pos_discount'];
        this.module_pos_hr = value['module_pos_hr'];
        this.module_pos_loyalty = value['module_pos_loyalty'];
        this.module_pos_mercury = value['module_pos_mercury'];
        this.module_pos_restaurant = value['module_pos_restaurant'];
        this.number_of_opened_session = value['number_of_opened_session'];
        this.only_round_cash_method = value['only_round_cash_method'];
        this.other_devices = value['other_devices'];
        this.partner_load_background = value['partner_load_background'];
        this.payment_method_ids = value['payment_method_ids'];
        this.picking_policy = value['picking_policy'];
        this.picking_type_id = value['picking_type_id'];
        this.pos_session_duration = value['pos_session_duration'];
        this.pos_session_state = value['pos_session_state'];
        this.pos_session_username = value['pos_session_username'];
        this.pricelist_id = value['pricelist_id'];
        this.print_address = value['print_address'];
        this.print_title = value['print_title'];
        this.print_unique_id = value['print_unique_id'];
        this.printer_ids = value['printer_ids'];
        this.product_configurator = value['product_configurator'];
        this.product_load_background = value['product_load_background'];
        this.proxy_ip = value['proxy_ip'];
        this.receipt_footer = value['receipt_footer'];
        this.receipt_header = value['receipt_header'];
        this.restrict_price_control = value['restrict_price_control'];
        this.rounding_method = value['rounding_method'];
        this.route_id = value['route_id'];
        this.selectable_categ_ids = value['selectable_categ_ids'];
        this.sequence_id = value['sequence_id'];
        this.sequence_line_id = value['sequence_line_id'];
        this.session_ids = value['session_ids'];
        this.set_maximum_difference = value['set_maximum_difference'];
        this.set_tip_after_payment = value['set_tip_after_payment'];
        this.ship_later = value['ship_later'];
        this.start_category = value['start_category'];
        this.tax_regime = value['tax_regime'];
        this.tax_regime_selection = value['tax_regime_selection'];
        this.tip_product_id = value['tip_product_id'];
        this.use_pricelist = value['use_pricelist'];
        this.uuid = value['uuid'];
        this.warehouse_id = value['warehouse_id'];
    }
}

// We create a class for the stack
class POSConfig {
    // The stack has three properties, the first node, the last node and the stack size
    constructor(){
        this.posconfig_current = null;// Can be the last value too or the current search
        this.posconfigs=[]
        
    }
    // The push method receives a value and adds it to the "top" of the stack
    push(val){
        this.posconfig_current = new posnode(val);
        this.posconfigs.push(this.posconfig_current);
        
    }
    // The pop method eliminates the element at the "top" of the stack and returns its value
    popByName(name){
        let self=this;
        self.posconfig_current=null;
        this.posconfigs.forEach(function(value, index){
           if (name === value.name){self.posconfigs.pop(value);} 
        });
    }
    searchByName(name){
        let self=this;
        self.posconfig_current=null;
        this.categories.forEach(function(value, index){
           if (name === value.name){self.posconfig_current=value;} 
        });
        return this.posconfig_current;

    }
    // The pop method eliminates the element at the "top" of the stack and returns its value
    popById(id){
        let self=this;
        self.posconfig_current=null;
        this.posconfigs.forEach(function(value, index){
           if (id === value.id){self.posconfigs.pop(value);} 
        });
    }
    searchById(id){
        let self=this;
        self.posconfig_current=null;
        this.posconfigs.forEach(function(value, index){
           if (id === value.id){self.posconfig_current=value;} 
        });
        return this.posconfig_current;

    }

    
}
