import java.util.Scanner;

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
		
		// Recebe valor N
		int n = scan.nextInt();
        String out = "";
        for (int i = 0; i < n; i++) {
            out += fila[i % fila.length] + " ";
        }

        System.out.println(out.trim());
	}

}
