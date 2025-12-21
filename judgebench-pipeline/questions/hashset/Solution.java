import java.util.*;
import java.math.*;

// esta nao eh uma solucao de referencia. feita apenas para passar nos testes.
class Solution {

    private static Scanner scan;
    

    public static void main(String[] args) {

        Scanner scan = new Scanner(System.in);

        int size = scan.nextInt();
        Table table = new Table(size);

        String input = scan.nextLine();

        while(!input.equals("end")) {
            input = scan.nextLine();

            if(input.startsWith("put")) {
                String[] data = input.split(" ");
                table.put(Integer.parseInt(data[1]));
                table.print();
            } else if(input.startsWith("remove")) {
                String[] data = input.split(" ");
                table.remove(Integer.parseInt(data[1]));
                table.print();
            } else if(input.startsWith("contains")) {
                String[] data = input.split(" ");
                System.out.println(table.contains(Integer.parseInt(data[1])));
 
            }


        }
    }

    
}


class Table {

    Pair[] table;

    Table(int size) {
        table = new Pair[size];
    }

    int hashCode(int key) {
        return key % table.length;
    }

    void print() {
        System.out.println(Arrays.toString(this.table));
    }

    void put(int value) {

        for (int i = 0; i <= table.length ; i++) {

            int pos = (hashCode(value) + i) % table.length;

            // found a free pos (null or deleted)
            if (this.table[pos] == null || (this.table[pos].key == null && this.table[pos].key == null) ) {
                this.table[pos] = new Pair(value, value);
                return;
            // update
            } else if (this.table[pos] != null && this.table[pos].key == value) {
                this.table[pos].value = value;
                return;
            }
            
        }

    }

    void remove(int value) {
        
        for (int i = 0; i <= table.length; i++) {

            int pos = (hashCode(value) + i) % table.length;

            if (this.table[pos] != null && this.table[pos].key != null) {

                if (this.table[pos].key == value) {
                    this.table[pos] = new Pair(null, null);
                    return;
                }

            }
        
        }
 
    }

    boolean contains(int v) {
    
         for (int i = 0; i <= table.length; i++) {

            int pos = (hashCode(v) + i) % table.length;

            if (this.table[pos] != null && this.table[pos].key != null) {

                if (this.table[pos].key == v) {
                    return true;
                }

            }
        
        }
 
        return false;
    
    }

}

class Pair {

    Integer key;
    Integer value;

    Pair(Integer key, Integer value) {
        this.key = key;
        this.value = value;
    }
    
    public String toString() {
        if (this.key == null) return "null";
        return key.toString();
    }
}
