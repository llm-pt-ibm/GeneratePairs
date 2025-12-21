
import java.util.*;

class Solution {
	
	public static void main(String[] args) {
		Scanner in = new Scanner(System.in);
		String entrada = in.nextLine();
		String[] placas = entrada.split(",");
		
		final int ultimoIndice = 7;
		final int indexHifen = 3;
	
        // radix    
		for (int indice = ultimoIndice; indice > indexHifen; indice--)
            placas = countingSort(placas, indice);

        String out = "";
        for (String placa : placas) {
            out += placa + ", ";
        }

        System.out.println(out.substring(0,out.length() - 2));
	}

	private static String[] countingSort(String[] v, int index) {

        int[] c = new int[10];
        for (int i = 0; i < v.length; i++) {
            c[Integer.parseInt(v[i].charAt(index)+"")] += 1;
        }

        // cumulativa
        for (int i = 1; i < c.length; i++)
            c[i] += c[i-1];

        String[] b = new String[v.length];
        for (int i = v.length - 1; i >= 0; i--) {
            b[c[Integer.parseInt(v[i].charAt(index)+"")] - 1] = v[i];
            c[Integer.parseInt(v[i].charAt(index)+"")] -= 1;
        }

        return b;
	}

	private static void swap(String[] arr, int i1, int i2) {
		String temp = arr[i1];
		arr[i1] = arr[i2];
		arr[i2] = temp;
	}
}
