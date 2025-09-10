import java.util.*;

class Solution {
    
    private int head, tail;
    private int[] fila;
    private int capacidade;

    public Solution(int capacidade) {
       this.head = -1;
       this.tail = -1;
       this.capacidade = capacidade;
       fila = new int[capacidade];
    }

    public boolean isEmpty() {
        return this.head == -1;
    }

    public boolean isFull() {
        return ((this.tail + 1) % capacidade) == head;
    }

    public boolean add(int n) {
    
        if (this.isFull())
            return false;

        if (this.isEmpty()) {
            this.head = 0;
            this.tail = 0;
            this.fila[head] = n;
        } else {
            this.tail = (this.tail + 1) % capacidade;
            this.fila[tail] = n;
        }
        return true; 
    }

    public boolean remove() {
        if (isEmpty()) return false;

        if (head == tail) {
            int out = this.fila[head];
            this.head = -1;
            this.tail = -1;
            return true;
        } else {
            this.head = (this.head + 1) % capacidade;
            return true;

        }
    }

    public int element() {
        if (this.isEmpty()) throw new RuntimeException("Queue is empty.");
        return this.fila[head];
    }


    public void print() {
        if (head != -1) {

            if (head == tail) {
                System.out.println(fila[head]);
                return;
            }
            
            int i = head;
            String s = "";
            do { 
                s += Integer.toString(fila[i]) + " ";
                i = ++i % capacidade;
            } while (i != tail);
                s += Integer.toString(fila[i]);
            System.out.println(s);
        } else {
            System.out.println("empty");
       }
   }



    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int cap = Integer.parseInt(sc.nextLine());

        Solution fila = new Solution(cap);

        while (true) {
        
            String op = sc.nextLine();

            if (op.equals("end"))
                break;

            if (op.contains("add")) {
                String[] tokens  = op.split(" ");
                int e = Integer.parseInt(tokens[1]);
                if (!fila.add(e))
                    System.out.println("full");
            
            } else if (op.contains("remove")) {
                if (!fila.remove())
                    System.out.println("empty");

            } else if (op.contains("element")) {
                if (fila.isEmpty())
                    System.out.println("empty");
                else
                    System.out.println(Integer.toString(fila.element()));
            } else {
               fila.print();
            }
        
        }
    
    }


}
