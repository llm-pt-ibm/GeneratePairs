import java.util.Scanner;

class PilhaComArray {

	private static Scanner scan;
	private static int size;
	private static int last;
	private static String[] array;

	public static void main(String[] args) {
		
		scan = new Scanner(System.in);
		
		last = -1;
		size = scan.nextInt();
		array = new String[size];
		
		String input = scan.nextLine();
		
		while(!input.equals("end")) {
			input = scan.nextLine();
			
			if(input.equals("pop"))
				pop();
			else if(input.contains("push"))
				push(input);
			else if(input.equals("peek"))
				peek();
			else if(input.equals("print"))
				print();
			
		}
	}

	private static void print() {
        String out = "";
		if(last == -1) {
			System.out.println("empty");
		} else {
			for (int i = 0; i <= last; i++) {
				out += array[i]+ " ";
			}	
			System.out.println(out.trim());
		}
	}

	private static void peek() {
		System.out.println(array[last]);
	}

	private static void push(String input) {
		if(last+1 == size) {
			System.out.println("full");
		} else {
			String num = input.split(" ")[1];
			
			last++;
			array[last] = num;
		}
	}

	private static void pop() {
		  if(last == -1) {
			  System.out.println("empty");
		  } else {
			  array[last] = null;
			  last--;
		  }
	}
}
