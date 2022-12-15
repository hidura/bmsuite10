// We create a class for each node within the stack
class variantnode {
    // Each node has two properties, its value and a pointer that indicates the node that follows
    constructor(value){
        this.id = value['id'];
        this.display_name = value['display_name'];
        this.type = value['type'];
        this.amount_to_choose = value['amount_to_choose'];
        this.is_limited = value['is_limited'];
        this.is_required = value['is_required'];
        this.sequence = value['sequence'];
        this.product_target=value['product_target'];
        this.product_variant=value['product_variant'];
        this.product_product=value['product_product']
    }
}

// We create a class for the stack
class Variants {
    // The stack has three properties, the first node, the last node and the stack size
    constructor(){
        this.variant_current = null;// Can be the last value too or the current search
        this.variants=[]
        
    }
    // The push method receives a value and adds it to the "top" of the stack
    push(val){
        this.variant_current = new variantnode(val);
        this.variants.push(this.variant_current);
        
    }
    // The pop method eliminates the element at the "top" of the stack and returns its value
    popByName(name){
        let self=this;
        self.variant_current=null;
        this.variants.forEach(function(value, index){
           if (name === value.name){self.variants.pop(value);} 
        });
    }
    searchByName(name){
        let self=this;
        self.variant_current=null;
        this.variants.forEach(function(value, index){
           if (name === value.name){self.variant_current=value;} 
        });
        return this.variant_current;

    }
    
    popById(id){
        let self=this;
        self.variant_current=null;
        this.variants.forEach(function(value, index){
           if (id === value.id){self.variants.pop(value);} 
        });
    }
    searchById(id){
        let self=this;
        self.variant_current=null;
        this.variants.forEach(function(value, index){
           if (id === value.id){self.variant_current=value;} 
        });
        return this.variant_current;

    }


    searchByProductVariant(product){
        let self=this;
        let variant={"term":[],"suggested":[],
    "optional":[],"companion":[]};
        this.variants.forEach(function(value, index){
            if (parseInt(product) === value.product_product[0]){
                if (value.type==="term"){
                    
                    variant[value.type].push({"id":false,
                    "name":value.display_name});
                }else{

                    variant[value.type].push({"id":value.product_target[0],
                    "name":value.product_target[1]});
                }
            } 
        });
        
        return variant;
    }



    searchSimilar(name){
        let self=this;
        let products_cats=[];
        this.products.forEach(function(value, index){
           if (value.name.includes(name)){products_cats.push(value);} 
        });
        return products_cats;

    }

}
