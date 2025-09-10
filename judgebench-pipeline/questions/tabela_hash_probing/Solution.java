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
                table.put(Integer.parseInt(data[1]), data[2]);
                table.print();
            } else if(input.startsWith("remove")) {
                String[] data = input.split(" ");
                table.remove(Integer.parseInt(data[1]));
                table.print();
            } else if(input.startsWith("keys"))
                System.out.println(table.keys());
            else if(input.startsWith("values"))
                System.out.println(table.values());

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

    void put(int key, String value) {

        for (int i = 0; i <= table.length ; i++) {

            int pos = (hashCode(key) + i) % table.length;

            // found a free pos (null or deleted)
            if (this.table[pos] == null || (this.table[pos].key == null && this.table[pos].key == null) ) {
                this.table[pos] = new Pair(key, value);
                return;
            // update
            } else if (this.table[pos] != null && this.table[pos].key == key) {
                this.table[pos].value = value;
                return;
            }
            
        }

    }

    void remove(int key) {
        
        for (int i = 0; i <= table.length; i++) {

            int pos = (hashCode(key) + i) % table.length;

            if (this.table[pos] != null && this.table[pos].key != null) {

                if (this.table[pos].key == key) {
                    this.table[pos] = new Pair(null, null);
                    return;
                }

            }
        
        }
 
    }

    String keys() {
        ArrayList keys = new ArrayList();

        for (int i = 0; i < table.length; i++) {
            if (table[i] != null && table[i].key != null)
                keys.add(table[i].key);
        }

        Collections.sort(keys);
        return Arrays.toString(keys.toArray());
    }
     String values() {
        ArrayList values = new ArrayList();

        for (int i = 0; i < table.length; i++) {
            if (table[i] != null && table[i].key != null)
                values.add(table[i].value);
        }

        Collections.sort(values);
        return Arrays.toString(values.toArray());
    }
 
}

class Pair {

    Integer key;
    String value;

    Pair(Integer key, String value) {
        this.key = key;
        this.value = value;
    }
    
    public String toString() {
        if (this.key == null) return "null";
        return "<" + key + ", " + value + ">";
    }
}
