// We create a class for each node within the stack
class tablenode {
    // Each node has two properties, its value and a pointer that indicates the node that follows
    constructor(value){
        this.id = value['id'];
        this.active = value['active'];
        this.color = value['color'];
        this.display_name = value['display_name'];
        this.floor_id = value['floor_id'];
        this.height = value['height'];
        this.name = value['name'];
        this.order_id=value['order_id'];
        this.position_h=value['position_h'];
        this.position_v = value['position_v'];
        this.seats=value['seats'];
        this.shape=value['shape'];
        this.width=value['width'];
    }
}

// We create a class for the stack
class TablesOrder {
    // The stack has three properties, the first node, the last node and the stack size
    constructor(){
        this.table_current = null;// Can be the last value too or the current search
        this.tables=[]
        
    }
    // The push method receives a value and adds it to the "top" of the stack
    push(val){
        if (this.searchById(parseInt(val['id']))===null){
            this.table_current = new tablenode(val);
            this.tables.push(this.table_current);
        }
    }
    // The pop method eliminates the element at the "top" of the stack and returns its value
    popByName(name){
        let self=this;
        self.table_current=null;
        this.tables.forEach(function(value, index){
           if (name === value.name){self.table_current.pop(value);} 
        });
    }
    searchByOrder(order_id){
        let self=this;
        self.table_current=null;
        this.tables.forEach(function(value, index){
           if (order_id === value.order_id){self.table_current=value;} 
        });
        return this.table_current;

    }
    
    popById(id){
        let self=this;
        self.table_current=null;
        this.tables.forEach(function(value, index){
           if (id === value.id){self.tables.pop(value);} 
        });
    }
    searchById(id){
        let self=this;
        self.table_current=null;
        this.tables.forEach(function(value, index){
           if (id === value.id){self.table_current=value;} 
        });
        return this.table_current;

    }



}
