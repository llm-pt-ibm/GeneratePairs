import java.util.*;
class Solution {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String[] entrada = sc.nextLine().split(" ");
        int i = Integer.parseInt(sc.nextLine());
        int stop = 0;
        int step = i;
        for (int k = i ; k < entrada.length; k++) {
            for (int j = step; j > stop; j--) {
               String aux = entrada[j-1];
               entrada[j-1] = entrada[j];
               entrada[j] = aux;
            }
            stop += 1;
            step += 1;
            System.out.println(Arrays.toString(entrada));
        }
        
    }

}
