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
        busca(nums,0,nums.length-1,n);


    }

    public static int busca(int[] nums, int left, int right, int n) {
        if (left > right) {
            System.out.println("-1");
            return -1;
        } else {
            int mid = (left + right) / 2;
            System.out.println(mid);
            if (nums[mid] == n)
                return mid;
            else if (n < nums[mid])
                return busca(nums,left,mid-1,n);
            else
                return busca(nums,mid+1,right,n);
        }


    }

}
