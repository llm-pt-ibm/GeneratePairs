import java.util.*;
import java.math.*;

// esta nao eh uma solucao de referencia. feita apenas para passar nos testes.
class Solution {

    private static Scanner scan;
    

    public static void main(String[] args) {

        Scanner scan = new Scanner(System.in);
        HashMap<String, Integer> freqTable = new HashMap<String, Integer>();

        String[] tokens = scan.nextLine().split(" ");

        for (String s : tokens) {
        
            if (freqTable.containsKey(s))
                freqTable.put(s, freqTable.get(s) + 1);
            else
                freqTable.put(s, 1);
        
        }

        String input = scan.nextLine().trim();

        while(!input.equals("fim")) {
            if (freqTable.containsKey(input))
                System.out.println(freqTable.get(input));    

            input = scan.nextLine();
        }
    }

    
}
