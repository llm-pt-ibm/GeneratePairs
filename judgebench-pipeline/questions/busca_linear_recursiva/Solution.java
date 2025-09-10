import java.util.*;

class Solution {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String[] s_nums = sc.nextLine().split(" ");
        int[] nums = new int[s_nums.length];
        
        int k = 0;
        for (String s : s_nums) {
            nums[k++] = Integer.parseInt(s);
        }

        int n = Integer.parseInt(sc.nextLine());
        
        int index = busca_linear_recursiva(nums,0,n);
        System.out.println(index);


    }

    public static int busca_linear_recursiva(int[] nums, int index, int n) {
        
        if (index == nums.length)
            return -1;
        else {
            if (nums[index] == n)
                return index;
            else
                return busca_linear_recursiva(nums, index + 1, n);
        }
    }

}










