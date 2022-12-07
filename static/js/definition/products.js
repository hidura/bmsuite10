// We create a class for each node within the stack
class productnode {
    // Each node has two properties, its value and a pointer that indicates the node that follows
    constructor(value){
        this.id = value['id'];
        this.name = value['name'];
        this.description = value['description'];
        this.image = value['image'];
        this.is_product_variant = value['is_product_variant'];
        this.price = value['price'];
        this.category=value['category']
    }
}

// We create a class for the stack
class Product {
    // The stack has three properties, the first node, the last node and the stack size
    constructor(){
        this.product_current = null;// Can be the last value too or the current search
        this.products=[]
        
    }
    // The push method receives a value and adds it to the "top" of the stack
    push(val){
        this.product_current = new productnode(val);
        this.products.push(this.product_current);
        
    }
    // The pop method eliminates the element at the "top" of the stack and returns its value
    popByName(name){
        let self=this;
        self.product_current=null;
        this.products.forEach(function(value, index){
           if (name === value.name){self.products.pop(value);} 
        });
    }
    searchByName(name){
        let self=this;
        self.product_current=null;
        this.products.forEach(function(value, index){
           if (name === value.name){self.product_current=value;} 
        });
        return this.product_current;

    }
    
    popById(id){
        let self=this;
        self.product_current=null;
        this.products.forEach(function(value, index){
           if (id === value.id){self.products.pop(value);} 
        });
    }
    searchById(id){
        let self=this;
        self.product_current=null;
        this.products.forEach(function(value, index){
           if (id === value.id){self.product_current=value;} 
        });
        return this.product_current;

    }


    searchByCategory(category){
        let self=this;
        let products_cats=[];
        this.products.forEach(function(value, index){
           if (category === value.category){products_cats.push(value);} 
        });
        return products_cats;

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
