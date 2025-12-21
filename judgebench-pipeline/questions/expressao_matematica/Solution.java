
import java.util.*;


class Sol {

    public static void main(String[] args) {

        Scanner sc = new Scanner(System.in);
        String entrada = sc.nextLine();

        LinkedList<Character> op = new LinkedList<Character>();
        LinkedList<Integer> nums  = new LinkedList<Integer>();
        int n1 = 0;
        int n2 = 0; 
        int result = 0;
        char t;
        for (int i = 0; i < entrada.length(); i ++) {
        
          char c = entrada.charAt(i);
          if (Character.isDigit(c)) {
            nums.push(Integer.parseInt(c+""));
          } else if (isOperator(c)) {
            op.push(c);
          } else if (c == ')') {
              n1 = nums.pop();
              n2 = nums.pop();
              t = op.pop();
              result = getResult(n1,n2,t);
              nums.push(result);

          }

        
        }
        
        while (!op.isEmpty()) {
            n1 = nums.pop();
            n2 = nums.pop();
            t = op.pop();
            result = getResult(n1,n2,t);
            nums.push(result); 
        }
        System.out.println(nums.getFirst()); 
    }

    public static boolean isOperator(char c) {
        return (c =='/' || c =='*' || c == '+' || c == '-');
    }

    public static int getResult(int n1, int n2, char t) {
                if (t == '-')
                    return (n2 - n1);
                else if (t == '*')
                    return (n1*n2);
                else if (t =='+')
                    return (n1+n2);
                else
                    return (n1/n2);
    
    
    }

}
