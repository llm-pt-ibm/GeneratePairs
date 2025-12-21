
import java.util.*; class Sol{public static void main(String[] args){Scanner sc = new Scanner(System.in);
        String entrada = sc.nextLine();
        LinkedList pilha = new LinkedList();

        if (entrada.charAt(0) == ')') {
            System.out.println("N");
            return;
        }

        int i = 0;
        while (i < entrada.length()) {
            if (entrada.charAt(i) == '(')
                pilha.push("(");
            else if (!pilha.isEmpty())
                pilha.pop();
            else {
                System.out.println("N");
                return;
            }
            i++;
        }

        if (pilha.isEmpty()) {
            System.out.println("S");
            return;
        } else {
            System.out.println("N");
            return;
        }

    
    }

}
////////
// user: joao.arthur@computacao.ufcg.edu.br
// group: prog1-20152
// mode: None
// open_datetime: 2016-03-14T19:08:55.531410
// create_datetime: 2016-03-14T19:08:44.652010
// revision: 6
// activity: 6067343163654144-1.0.0
// assignment: 4856516989419520
// ip: 150.165.98.111
// timestamp: 2016-03-14T19:37:34.098820
