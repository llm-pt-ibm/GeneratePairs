import java.util.Scanner;
import java.util.Arrays;
class Solution {

	public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);	
		// Recebe sequencia de valores
		String input = scan.nextLine();
		String[] arrString = input.split(" ");

		int[] fila = new int[arrString.length];
		for (int i = 0; i < arrString.length; i++) {
			fila[i] = Integer.parseInt(arrString[i]);
		}
		
        for (int i = 0; i < fila.length - 1; i+=2) {
            int aux = fila[i];
            fila[i] = fila[i+1];
            fila[i+1] = aux;
        }

        System.out.println(Arrays.toString(fila));
	}

}
