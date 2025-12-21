import java.util.Arrays;
import java.util.Scanner;

class Solution {
	public static void main(String[] args) {
		Scanner in = new Scanner(System.in);
		String entrada = in.nextLine();
		String[] livros = entrada.split(",");

		sortComPrints(livros, 1);
	}

	private static void sortComPrints(String[] livros, int indice) {
		System.out.println(String.join(", ", livros));
		int indiceIt = indice;
		while (indiceIt > 0 && indice < livros.length) {
			if (livros[indiceIt].compareTo(livros[indiceIt - 1]) < 0)
				swap(livros, indiceIt, --indiceIt);
			else
				break;
		}
		if (indice < livros.length)
			sortComPrints(livros, indice + 1);
	}

	private static void swap(String[] arr, int i1, int i2) {
		String temp = arr[i1];
		arr[i1] = arr[i2];
		arr[i2] = temp;
	}
}
