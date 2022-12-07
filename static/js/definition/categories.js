// We create a class for each node within the stack
class categorynode {
    // Each node has two properties, its value and a pointer that indicates the node that follows
    constructor(value){
        this.id = value['id'];
        this.name = value['name'];
        this.printername = value['printername'];
    }
}

// We create a class for the stack
class Category {
    // The stack has three properties, the first node, the last node and the stack size
    constructor(){
        this.category_current = null;// Can be the last value too or the current search
        this.categories=[]
        
    }
    // The push method receives a value and adds it to the "top" of the stack
    push(val){
        this.category_current = new categorynode(val);
        this.categories.push(this.category_current);
        
    }
    // The pop method eliminates the element at the "top" of the stack and returns its value
    popByName(name){
        let self=this;
        self.category_current=null;
        this.categories.forEach(function(value, index){
           if (name === value.name){self.categories.pop(value);} 
        });
    }
    searchByName(name){
        let self=this;
        self.category_current=null;
        this.categories.forEach(function(value, index){
           if (name === value.name){self.category_current=value;} 
        });
        return this.category_current;

    }
    
    popByPrinter(printer){
        let self=this;
        self.category_current=null;
        this.categories.forEach(function(value, index){
           if (printer === value.printername){self.categories.pop(value);} 
        });
    }
    searchByPrinter(name){
        let self=this;
        self.category_current=null;
        this.categories.forEach(function(value, index){
           if (name === value.printername){self.current=value;} 
        });
        return this.category_current;

    }
}
