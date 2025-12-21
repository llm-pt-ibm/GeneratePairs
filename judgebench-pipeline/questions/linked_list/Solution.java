import java.util.*;
class LinkedList {

    private Node head;
    private int size;

    public LinkedList() {
        this.head = null;
        this.size = 0;
    }

    public boolean isEmpty() {
        return this.head == null;
    }

    public void add(int v) {
        Node newNode = new Node(v);
        
        if (isEmpty())
            this.head = newNode;
        else {
            Node aux = head;
            while (aux.next != null)
                aux = aux.next;
            aux.next = newNode;
        }
        
        this.size += 1;
    }

    private int search(int value) {
        int i = 0;
        Node aux = head;
        while (aux != null && aux.value != value) {
            aux = aux.next;
            i++;
        }
        return (aux == null) ? -1 : i;
    }

    public boolean remove(int value) {
    
        if (!isEmpty()) {

            if (this.head.value == value) {
                this.head = this.head.next;
                this.size--;
                return true;
            }

            Node prev = null;
            Node aux = head;
            
            while (aux != null && aux.value != value) {
                prev = aux;
                aux = aux.next;
            }

            if (aux == null) return false;
            else {
                prev.next = aux.next;
                this.size--;
                return true;
            }

        }
        
        return false;
    
    
    }

    public boolean removeLast() {
    
        if (!isEmpty()) {
        
            if (this.head.next == null)
                this.head = null;
            else {
                Node prev = null;
                Node aux = head;

                while(aux.next != null) {
                    prev = aux;
                    aux = aux.next;
                }

                prev.next = null;
            }
            this.size--;
            return true;
        }
        return false;
    
    }

    public int size() {
        return this.size;
    }

    public String toString() {
        if (isEmpty()) return "empty";
        
        String out = "";
        Node aux = head;

        while (aux != null) {
            out += aux.value + " ";
            aux = aux.next;
        }

        return out.trim();
    }

    public int element() {
        return this.head.value;
    }

    public boolean remove() {
        if (isEmpty()) return false;
        head = head.next; 
        return true;
    }

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        LinkedList fila = new LinkedList();

        while (true) {
        
            String op = sc.nextLine();

            if (op.equals("end"))
                break;

            if (op.contains("add")) {
                String[] tokens  = op.split(" ");
                int e = Integer.parseInt(tokens[1]);
                fila.add(e);
            
            } else if (op.contains("remove")) {
                if (!fila.remove())
                    System.out.println("empty");

            } else if (op.contains("element")) {
                if (fila.isEmpty())
                    System.out.println("empty");
                else
                    System.out.println(Integer.toString(fila.element()));
            } else if (op.contains("search")) {
                String[] tokens  = op.split(" ");
                int e = Integer.parseInt(tokens[1]);
                System.out.println(fila.search(e));
            } else {
               System.out.println(fila);
            }
        
        }
    
    }

}


class Node {
    int value;
    Node next;

    Node(int value) {
        this.value = value;
        this.next = null;
    }
}
