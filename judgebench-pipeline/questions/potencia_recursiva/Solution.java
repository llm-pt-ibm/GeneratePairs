import java.util.*;
class Solution {

    public static void main(String[] args) {
    
        Scanner sc = new Scanner(System.in);

        int i = sc.nextInt();
        int j = sc.nextInt();

        System.out.println(pow(i,j));
    
    }

    public static int pow(int i, int j) {
        if (j == 0)
            return 1;
        else
            return i*pow(i, j-1);
    }

}
