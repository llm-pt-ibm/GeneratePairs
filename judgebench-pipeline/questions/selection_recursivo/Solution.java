import java.util.Arrays;
import java.util.Scanner;

class Solution {


    public static void main(String[] args) {
		
		Scanner scan = new Scanner(System.in);
		String input = scan.nextLine();
		
		String[] strArray = input.split(" ");
		int[] intArray = new int[strArray.length];
		for(int i = 0; i < strArray.length; i++) {
		    intArray[i] = Integer.parseInt(strArray[i]);
		}
		
		recSelection(intArray, 0);
	}

	public static void recSelection(int[] v, int i) {

        if (i >= v.length)
            return;
        else {
            if (is_sorted(v))
                return;
            int menor = i;
            for (int j = i+1; j < v.length; j++) {
                if (v[j] < v[menor])
                    menor = j;
            }
            swap(v, i, menor);
            System.out.println(Arrays.toString(v));
            recSelection(v, i+1);
        }
    }

    public static void swap(int[] v, int i , int j) {
        int aux = v[i];
        v[i] = v[j];
        v[j] = aux;
    }
    
    public static boolean is_sorted(int[] v) {
        for (int i = 0; i < v.length - 1; i++) {
            if (v[i] > v[i+1])
                return false;
        }
        return true;
    }

}
