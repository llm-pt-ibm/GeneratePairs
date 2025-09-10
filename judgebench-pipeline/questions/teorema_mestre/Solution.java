import java.util.Scanner;

class Solution {

	private static Scanner scan;

	public static void main(String[] args) {
		scan = new Scanner(System.in);
		
		String input = scan.nextLine();
		String[] arrString = input.split(" ");
		
		teoremaMestre(arrString[0], arrString[1], arrString[2]);
	}

	private static void teoremaMestre(String a, String b, String ord) {
		double log = (Math.log(Integer.parseInt(a)) / Math.log(Integer.parseInt(b)));
		int ordem = Integer.parseInt(ord);
		
		if(log > ordem) {
			System.out.printf("T(n) = theta(n**%.0f)", log);
		} else if (log == ordem) {
			System.out.printf("T(n) = theta(n**%.0f * log n)", log);
		} else {
			System.out.printf("T(n) = theta(n**%d)", ordem);	
		}
        System.out.println();
	}
}
