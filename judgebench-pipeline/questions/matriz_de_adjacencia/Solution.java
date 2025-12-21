import java.util.*;
import java.math.*;

// esta nao eh uma solucao de referencia. feita apenas para passar nos testes.
class Solution {

    private static Scanner scan;
    

    public static void main(String[] args) {

        Scanner scan = new Scanner(System.in);
        HashMap<String, String> grafo = new HashMap<String, String>();

        String[] tokens = scan.nextLine().split(" ");

        for (int i = 0; i < tokens.length; i++) {
            String[] pesos = scan.nextLine().split(" ");
            
            for (int j = 0; j < pesos.length; j++) {

                if (!pesos[j].equals("0"))
                    grafo.put(tokens[i]+tokens[j], pesos[j]);

            }
        
        }


        String input = scan.nextLine().trim();

        while(!input.equals("fim")) {
            if (grafo.containsKey(input))
                System.out.println(grafo.get(input));
            else
                System.out.println("aresta inexistente.");

            input = scan.nextLine();
        }

        scan.close();
    }

    
}
