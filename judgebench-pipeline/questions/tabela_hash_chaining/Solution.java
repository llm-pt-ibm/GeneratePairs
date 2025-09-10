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

    ArrayList[] table;
    int size;

    Table(int size) {
        table = new ArrayList[size];
        for (int i = 0; i < table.length; i++) {
            table[i] =  new ArrayList();
        }
        size = 0;
    }

    int hashCode(int key) {
        return key % table.length;
    }

    void print() {
        System.out.println(Arrays.toString(this.table));
    }

    void put(int key, String value) {
        int pos = hashCode(key);
        ArrayList l = this.table[pos];
    
        boolean update = false;
        for (int i = 0; i < l.size(); i++) {
            if (  ((Pair)(l.get(i))).key == key) {
                ((Pair)(l.get(i))).value  = value; 
                update = true;
                break;
            }
        }

        if (!update)
            l.add(new Pair(key, value));
        
        this.table[pos] = l;
    }

    boolean remove(int key) {
        int pos = hashCode(key);
        ArrayList l = this.table[pos];
        for (int j = l.size()-1; j >= 0; j--) {
            if (((Pair)(l.get(j))).key == key) {
                l.remove(j);
                return true;
            }
        }
        return false;
    }

    String keys() {
        ArrayList l = new ArrayList();
        for (int i = 0; i < table.length; i++)
            for (int j = 0; j < table[i].size(); j++)
                l.add( ((Pair)table[i].get(j)).key );
        Collections.sort(l);
        return l.toString();
    }

    String values() {
        ArrayList l = new ArrayList();
        for (int i = 0; i < table.length; i++)
            for (int j = 0; j < table[i].size(); j++)
                l.add( ((Pair)table[i].get(j)).value);
        Collections.sort(l);
        return l.toString();
    }


}

class Pair {

    int key;
    String value;

    Pair(int key, String value) {
        this.key = key;
        this.value = value;
    }
    
    public String toString() {
        return "<" + key + ", " + value + ">";
    }
}
