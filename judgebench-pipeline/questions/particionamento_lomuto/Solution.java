import java.util.*;

class Solution {

     public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        String[] strA = sc.nextLine().split(" ");

        int[] array = new int[strA.length];
        for (int k = 0; k < strA.length; k++)
            array[k] = Integer.parseInt(strA[k]);

        particiona(array, 0, array.length - 1);

        System.out.println(Arrays.toString(array));

     }
    

    public static int particiona(int[] v, int ini, int fim) {
        
        int pivot = v[ini];
        int i = ini;

        for (int j = ini + 1; j <= fim; j++) {
            if (v[j] < pivot) {
                i+=1;
                swap(v, i, j);
                System.out.println(Arrays.toString(v));
            }
        }

        // troca pivot (v[ini]) com i.
        swap(v, ini, i);
        System.out.println(Arrays.toString(v));
        
        return i; 
    }

    public static void swap(int[] v, int i, int j) {
        int aux = v[i];
        v[i] = v[j];
        v[j] = aux;
    }



}