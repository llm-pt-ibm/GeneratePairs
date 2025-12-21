import java.util.*;

class Solution {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String in = sc.nextLine();
        String[] s_nums = in.split(" ");
        int[] nums = new int[s_nums.length];
        
        
        int k = 0;
        for (String s : s_nums) {
            nums[k++] = Integer.parseInt(s);
        }

        int maior = nums[0];
        for (int j = 1; j < nums.length; j++) {
            if (nums[j] > maior)
                maior = nums[j];
        }

        int[] freq = new int[maior + 1];

        for (int i = 0; i < nums.length; i++)
            freq[nums[i]] += 1;

        String out= "";
        for (int i = 0; i < nums.length; i++) {
            if (freq[nums[i]] != 0) {
                out += (nums[i] + "," + freq[nums[i]] + " ");
                freq[nums[i]] = 0;
            }
        
        }

/*
 * -   category: public
 *         input: |
 *                 1 1 5 7 1
 *                     type: io
 *                         output: |
 *                                 1,3 5,1 7,1
 * */        


//        System.out.println("-   input: |");
//        System.out.println("        " + in);
//        System.out.println("    output: |");
//        System.out.println("        " + out.trim());
        System.out.println(out.trim());      
        sc.close();
    }


}
