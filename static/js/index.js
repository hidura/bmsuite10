


function openPOS(pos_id){
    
    $("#pos").slideUp();
    $("#zones").slideDown();
    $("#zones_aviable").empty();
    pos_config.searchById(pos_id);
    pos_session.searchByPosConfig(pos_id);
    sugelico.postServerCall({"pos":pos_id}, function(data, status){
        JSON.parse(data).forEach(function(value, index){
            zone=value[0];

            $("#zones_aviable").html("<div class='col-md-4 pos_div'>\
                <button onclick='openZone("+zone.id+");' class='pos_btn btn btn-primary'><span class='btn-label'><i class='fa-solid fa-square'></i></span>"+zone.display_name+"</button>\
            </div>");
        });
    },"/getFloors");

}

function openZone(zone_id){
    
    sugelico.postServerCall({"zone":zone_id}, function(data, status){
        
        $("#zones").slideUp();
        $("#tables").slideDown();
        htmlStr="";

        $("#tables_aviable").empty();
        data.forEach(function(value, index){
            
            table=value[0];
            tablesorderdb.push(table);
            pos_btn='pos_btn btn';
            var tbl_name=table.display_name;
            if (table.order_id!=false){
                pos_btn+=" btn-success"
                tbl_name+="<br/>("+table.order_id+")";
            }else{
                pos_btn+=" btn-primary"
            }

            htmlStr+="<button style='margin-bottom: 15px;' onclick='openTable("+table.id+");' class='"+pos_btn+"'><span class='btn-label'><i class='fa-solid fa-square'></i></span>"+tbl_name+"</button>";
            
        });
        $("#tables_aviable").html(htmlStr)
    },"/getFloorTables");

}

function openTable(table_id){
    tablesorderdb.searchById(parseInt(table_id));

    if (tablesorderdb.table_current.order_id===false){
        //Usando esta funcion me mandaras los detalles de la orden a /addOrder
        var orderInfo={
            "table_id":table_id,
            "sale_journal":pos_session.possession_current.cash_journal_id[0],
            "user_id":2,
            "company_id":pos_session.possession_current.company_id[0],
            "id_session":pos_session.possession_current.id,
            "amount_tax":0,
            "amount_total":0,
            "amount_paid":0,
            "amount_return":0,
            "pricelist_id":pos_config.posconfig_current.pricelist_id[0],
            };
        sugelico.postServerCall(orderInfo, function(data, status){
            orderdb.push(data[0]);
        },"/addOrder");
    }else{
        orderdb.searchById(tablesorderdb.table_current.order_id);
        console.log(orderdb.order_current);
    }

    $("#pos_prep").slideUp();
    $("#orders").slideDown();
}

function gobackPOS(){

    $("#zones").slideUp();
    $("#pos").slideDown();
}

function gobackZones(){

    $("#tables").slideUp();
    $("#zones").slideDown();
}

function loadProducts(){
    sugelico.postServerCall({}, function(data, status){
        var products = JSON.parse(data);
        var htmlStr="";
        products.forEach(function(value, index){
            if (categorydb.searchByName(value.category[1])===null){               
                categorydb.push({
                    "id":value.category[0],
                    "name":value.category[1],
                    "printername":value.category[2]
                });
            }
            productsdb.push({
                "id":value.id,
                "name":value.name,
                "description":value.description,
                "is_product_variant":value.is_product_variant,
                "price":value.price,
                "image":value.image,
                "category":value.category[1]
            });
            htmlStr+="<button onclick='addProduct("+value.id+");' style='width:150px;line-height: 14px;font-size: 12px;text-overflow: ellipsis;' class='btn btn-light'><img class='img-thumbnail' src='"+value.image+"'/><br/><div class='product_name'>"+value.name+"</div></button>";
            
        });
        $("#product_details").html(htmlStr);
    },"/getProducts");
}


function loadVariants(){
    sugelico.postServerCall({}, function(data, status){
        
        data.forEach(function(value, index){
            value[0].variants.forEach(function(product_target, subindex){
                variantdb.push(product_target[0]);
            })
        });
        
    },"/getVariants");
}



function getPOS(){
    sugelico.postServerCall({}, function(pos, status){
        sessions_ids=[];
        pos.forEach(function(value, index){
            pos_config.push(value[0]);
            if (pos_config.posconfig_current.has_active_session){
                sessions_ids.push(pos_config.posconfig_current.current_session_id[0]);
            }

        });
        getSession(sessions_ids);
    },"/loadPOS");
}

function getSession(sessions_ids){
    sugelico.postServerCall({"session_ids":sessions_ids}, function(pos, status){
        var htmlstr="";
        pos.forEach(function(value, index){
            pos_session.push(value[0]);
            pos_config.searchById(pos_session.possession_current.config_id[0]);
            htmlstr+="<button onclick='openPOS("+pos_session.possession_current.config_id[0]+");' class='pos_btn btn btn-primary'><span class='btn-label'><i class='fa-solid fa-square'></i></span>"+ pos_config.posconfig_current.name+"</button>";
        });
        $("#pos_aviable").html(htmlstr);

        getOrdersBySession(sessions_ids);
    },"/loadSession");
}


function getOrdersBySession(sessions_ids){
    console.log(sessions_ids);
    sugelico.postServerCall({"session_ids":sessions_ids}, function(pos_orders, status){
        pos_orders.forEach(function(value, index){
            orderdb.push(value[0]);
        });
    },"/getOrder");
}

function gobackDashboard(){
    $("#pos_prep").slideDown();
    $("#orders").slideUp();
}
function addProductOrder(){
    


}

function afterload(){}

function addProduct(product_id){
    let product = productsdb.searchById(product_id);

    var htmlStr=sugelico.getNumPad;
    var buttons={}
    sugelico.openDialog("PRODUCTO: "+product.name,htmlStr,buttons,"large",afterload)


}

function setAmount(value){
    var current_amount=$("#amount_to_pick").val();
    $("#amount_to_pick").val(current_amount+value);
}
function delAmount(){
    var current_amount=$("#amount_to_pick").val();

    $("#amount_to_pick").val(current_amount.slice(0,-1));
}
$(function(){
    
    const loadProduct = new Promise(loadProducts);
    const loadPOS = new Promise(getPOS);
    const loadVariant = new Promise(loadVariants);
    loadProduct.then((value)=>{
        loadPOS.then((value)=>{
            
            loadVariant.then((value)=>{

            });
        }).
        catch((err)=>{
            console.error(err);
        });
        
    }).
    catch((err)=>{
        console.error(err);
    });
});