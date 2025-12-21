import java.util.*;

class MelhorPivot {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        String[] strA = sc.nextLine().split(" ");
        String data = sc.nextLine();

        int i = Integer.parseInt(data.substring(0,1));
        int j = Integer.parseInt(data.substring(2,3));

        int[] array = new int[strA.length];
        for (int k = 0; k < strA.length; k++) 
            array[k] = Integer.parseInt(strA[k]);

        System.out.println(melhorPivotSimplificado(array, i , j));

	}
	
	public static int melhorPivotSimplificado(int[] array, int i, int j) {
		int menoresI = 0;
		for (int k = 0; k < array.length; k++) {
			if (array[k] < array[i])
				menoresI +=1;
		}
		
		int menoresJ = 0;
		for (int k = 0; k < array.length; k++) {
			if (array[k] < array[j])
				menoresJ +=1;
		}
		
		int med = array.length / 2;
		
		if (Math.abs(menoresI - med) <= Math.abs(menoresJ - med))
			return i;
		else
			return j;
		
	}
	
	private static int particiona(int[] array, int i) {
		swap(array,0,i);
		int pivot = array[0];
		int index_pivot = 0;
		
		for (int j = 1; j < array.length; j++) {
			if (array[j] < pivot) {
				index_pivot+=1;
				swap(array,index_pivot,j);
			}
		}
		return index_pivot;
	}
	
	private static void swap(int[] array, int i, int j) {
		int aux = array[i];
		array[i] = array[j];
		array[j] = aux;
	}

}
