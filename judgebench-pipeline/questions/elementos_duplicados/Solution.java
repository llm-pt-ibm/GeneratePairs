import java.util.Scanner;

class ElementosRepetidos {

	private static Scanner scan;

	public static void main(String[] args) {
		scan = new Scanner(System.in);
		String input = scan.nextLine();
		
		// Este if garante que nao havera erro caso o usuario apenas aperte enter
		if(input.length() == 0) {
			System.out.println(false);
		} else {
			String[] strArray = input.split(" ");
			int[] intArray = new int[strArray.length];
			
			for(int i = 0; i < strArray.length; i++) {
			    intArray[i] = Integer.parseInt(strArray[i]);
			}
			
			System.out.println(checkDuplicated(intArray));
		}		
	}
	
	// Principio similar ao do counting sort
	public static boolean checkDuplicated(int[] seq) {
		int[] aux = new int[max(seq)];
		for (int i = 0; i < aux.length; i++) {
			aux[i] = 0;
		}
		
		for (int i = 0; i < seq.length; i++) {
			if(aux[seq[i]-1] == 1) {
				return true;
			}
			aux[seq[i]-1]++;
		}
		return false;
	}

	private static int max(int[] seq) {
		int max = Integer.MIN_VALUE;
		
		for (int i = 0; i < seq.length; i++) {
			if(seq[i] > max) {
				max = seq[i];
			}
		}
		return max;
	}
}
