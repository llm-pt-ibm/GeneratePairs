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
		
		recInsertion(intArray, 1);
	}

	public static void recInsertion(int[] v, int i) {

        if (i >= v.length)
            return;
        else {
            int j = i;
            while (j > 0 && v[j] < v[j-1]) {
                swap(v,j, j-1);
                j--;
            }

            System.out.println(Arrays.toString(v));
            recInsertion(v, i+1);
        }
    }

    public static void swap(int[] v, int i , int j) {
        int aux = v[i];
        v[i] = v[j];
        v[j] = aux;
    }

}
