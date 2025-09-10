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
        
        int pivot = intArray[0];
        int cont = 0;
        for (int i : intArray) {
            if (i < pivot) {
                cont+=1;
            }
        }

        System.out.println(cont + 1);
	}

}
