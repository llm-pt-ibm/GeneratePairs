import java.util.*;
import java.lang.*;
import java.io.*;

class Solution {

    public static void main(String[] args) {
        Node root1 = new Node();
        Node root2 = new Node();

        Scanner in = new Scanner(System.in);
        int tam = in.nextInt();
        
        for (int i = 0; i < tam; i++) {
            root1.add(in.nextInt());
        }
        for (int i = 0; i < tam; i++) {
            root2.add(in.nextInt());
        }

        boolean isSimilar = test(root1, root2);
        System.out.println(isSimilar ? "Arvores similares." : "Arvores com estruturas diferentes.");
    }

    static boolean test(Node node1, Node node2) {
        if (node1 == null && node2 == null) {
            return true;
        }
        if (node1 == null || node2 == null) {
            return false;
        }
        return test(node1.esq, node2.esq) && test(node1.dir, node2.dir);
    }

    static class Node {

        private Integer valor;
        private Node esq;
        private Node dir;

        Node() {}

        void add(int valor) {
            if (this.valor == null) {
                this.valor = valor;
                // Estratégia de folhas não nulas
                this.esq = new Node();
                this.dir = new Node();
            }
            else if (this.valor > valor) this.esq.add(valor);
            else this.dir.add(valor);
        }
    }
}