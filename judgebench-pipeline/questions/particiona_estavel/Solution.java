import java.util.*;

class Solution {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        String[] strA = sc.nextLine().split(" ");

        int[] array = new int[strA.length];
        for (int k = 0; k < strA.length; k++) 
            array[k] = Integer.parseInt(strA[k]);

	    particiona(array);	
	}
	
	private static void particiona(int[] array) {
        int pivot = array[0];
        int i = 0;

		for (int j = 1; j < array.length; j++) {
			if (array[j] <= pivot) {
                for (int k = j; k > i; k--) {
                    swap(array,k,k-1);
                }
				i+=1;
			}
		}
//swap(array, i , 0);
        System.out.println(Arrays.toString(array));
	}
	
	private static void swap(int[] array, int i, int j) {
		int aux = array[i];
		array[i] = array[j];
		array[j] = aux;
	}

}
