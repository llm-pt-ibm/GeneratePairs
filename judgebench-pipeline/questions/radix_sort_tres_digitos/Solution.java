import java.util.Arrays;
import java.util.Scanner;

 class RadixSort {
	
	public static int[] counting(int[] a, int k, int nthDig) {
		
		// frequência
		int[] c = new int[k];
		for (int i = 0; i < a.length; i++) {
			int n = extractDigits(a[i], nthDig);	
			c[n - 1] += 1;
		}
		
		// cumulativa
		for (int i = 1; i < c.length; i++)
			c[i] += c[i-1];
		
		int[] b = new int[a.length];
		for (int i = a.length - 1; i >= 0; i--) {
			int d = extractDigits(a[i], nthDig);
			
			b[c[d - 1] - 1] = a[i];
			c[d - 1] -= 1;
		}
		
		return b;
	}
	
	public static int extractDigits(int n, int nthDig) {
		int d1 = (int) (n % Math.pow(10, nthDig));
		d1 = (int) (d1 / Math.pow(10, nthDig - 1));
		
		int d2 = (int) (n % Math.pow(10, nthDig+1));
		d2 = (int) (d2 / Math.pow(10, nthDig));

      	int d3 = (int) (n % Math.pow(10, nthDig+2));
		d3 = (int) (d3 / Math.pow(10, nthDig+1));

		return Integer.valueOf(String.valueOf(d3) + String.valueOf(d2) + String.valueOf(d1));
	}
	
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		String[] entrada = sc.nextLine().split(" ");
		int[] a = new int[entrada.length];
		for (int i = 0; i < a.length; i++)
			a[i] = Integer.parseInt(entrada[i]);
		
        int d = Integer.parseInt(sc.nextLine());
        
        for (int i = 1; i <= d; i += 3) {
        		a = counting(a, 999, i);
        		System.out.println(Arrays.toString(a));
        }
        
		
		sc.close();
	}
	
}

