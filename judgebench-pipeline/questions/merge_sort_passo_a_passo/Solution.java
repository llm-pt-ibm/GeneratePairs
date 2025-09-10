import java.util.*;
class Solution {

	private int[] helper;
	private int[] v;

	public Solution(int[] unsortedArray) {
		this.v = unsortedArray;
		this.helper = new int[v.length];
	}

	public void mergeSort(int low, int high) {
		
		if (low < high) {
			int middle = low + (high - low) / 2;
			
			gravar(v, low, middle);
			mergeSort(low, middle);
			gravar(v, middle +1, high);
			mergeSort(middle + 1, high);
			merge(low, middle, high);
		}

	}
	
	public void gravar(int[] vetor, int low, int high){
		String result = "";
		for (int i = low; i <= high; i++) {
			result += vetor[i];
			if( i < high){
				result += ", ";
			}
		}
		System.out.print("[" + result + "]");
		System.out.println();
	}
	
	
	private void merge(int low, int middle, int high) {
		for (int i = low; i <= high; i++) {
			this.helper[i] = v[i];
		}
		int i = low;
		int j = middle + 1;
		int k = low;

		while (i <= middle && j <= high) {
			if (helper[i] <= helper[j]) {
				v[k] = helper[i];
				i++;
			} else {
				v[k] = helper[j];
				j++;
			}
			k++;
		}

		while (i <= middle) {
			v[k] = helper[i];
			k++;
			i++;
		}

		while (j <= high) {
			v[k] = helper[j];
			k++;
			j++;
		}
		
		gravar(v, low, high);
		
	}

    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        String input = scan.nextLine();
            
        String[] strArray = input.split(" ");
        int[] intArray = new int[strArray.length];
        for(int i = 0; i < strArray.length; i++) {
            intArray[i] = Integer.parseInt(strArray[i]);
        }

        System.out.println(Arrays.toString(intArray));
        Solution m = new Solution(intArray);
        m.mergeSort(0,intArray.length-1);

    }
}
