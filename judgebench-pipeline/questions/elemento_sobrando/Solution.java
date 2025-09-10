import java.util.*;

class Solution {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        String[] s_nums = sc.nextLine().split(" ");
        int k = 0;
        for (String s : s_nums) {
            k += Integer.parseInt(s);
        }

        int j = 0;
        String[] s_num = sc.nextLine().split(" ");
        for (String s : s_num) {
            j += Integer.parseInt(s);
        }

        System.out.println(Math.abs(k - j));

    }

}
