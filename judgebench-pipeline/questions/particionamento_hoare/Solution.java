import java.util.*;
class Solution {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        String[] strA = sc.nextLine().split(" ");

        int[] array = new int[strA.length];
        for (int k = 0; k < strA.length; k++)
            array[k] = Integer.parseInt(strA[k]);

        Solution.hoare(array, 0, array.length - 1);

        System.out.println(Arrays.toString(array));

     }

    public static void quickSort(int[] v, int ini, int fim) {
    
        if (ini < fim) {
            int pos_pivot = hoare(v, ini, fim);
            quickSort(v, ini, pos_pivot);
            quickSort(v, pos_pivot + 1, fim);
        }
    
    }

    public static int hoare(int[] v, int ini, int fim) {
        int pivot = v[ini];
        int i = ini - 1;
        int j = fim + 1;

        while (true) {
            do {
                i += 1;
            } while (v[i] < pivot);
        
            do {
                j -= 1;
            } while (v[j] > pivot);

            if (i < j) {
                int tmp = v[i];
                v[i] = v[j];
                v[j] = tmp;
            } else {
                return j + 1;
            }

        }

    }

    public static int particiona(int[] v, int ini, int fim) {
    
        int pivot = v[ini];
        int i = ini;

        for (int j = ini + 1; j <= fim; j++) {
            if (v[j] < pivot) {
                i += 1;
                int tmp = v[i];
                v[i] = v[j];
                v[j] = tmp;
            }
        }

        int tmp = v[i];
        v[i] = pivot;
        v[ini] = tmp;

        return i;
    }


    public static void mergeSort(int[] v, int ini, int fim) {
    
        if (ini < fim) {
            int meio = (ini + fim) / 2;
            mergeSort(v, ini, meio);
            mergeSort(v, meio + 1, fim);
            merge(v, ini, meio, fim);
        }
    
    }


    public static void merge(int[] v, int ini, int meio, int fim) {
    
        int[] helper = new int[v.length];
        for (int i = 0; i < v.length; i++)
            helper[i] = v[i];


        int i = ini;
        int j = meio + 1;
        int k = ini;

        while (i <= meio && j <= fim) {
            if (helper[i] < helper[j])
                v[k++] = helper[i++]; 
            else
                v[k++] = helper[j++];

        }

        while (i <= meio)
            v[k++] = helper[i++];

        while (j <= fim)
            v[k++] = helper[j++];
    
    }
}
