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

        int n = nums.length - 1;

        for (int i = parent(n); i >= 0; i--) {
           heapify(nums, i);
        }

        System.out.println(Arrays.toString(nums));
        sc.close();
    }

    static void heapify(int[] nums, int i) {
        
        int left = left(i);
        int right = right(i);
        int max = max(i, left, right, nums);


        if (max != i) {
            int tmp = nums[i];
            nums[i] = nums[max];
            nums[max] = tmp;
            heapify(nums, max);
        }

    }

    static int max(int i, int left, int right, int[] nums) {
        if (isValid(left, nums) && isValid(right, nums)) {
            
            if (nums[left] > nums[i] && nums[left] > nums[right])
                return left;

            if (nums[right] > nums[i] && nums[right] > nums[left])
                return right;

            return i;

        } else if (isValid(left, nums)) {
            if (nums[left] > nums[i]) return left;
            else return i;
 
        } else if (isValid(right, nums)) {
            if (nums[right] > nums[i]) return right;
            else return i;           
        }
        
        return i;

    }

    static boolean isValid(int i, int[] nums) {
        return (i >= 0 && i < nums.length);
    }

    static int parent(int i) {
        return (i-1) / 2 ;
    }

    static int left(int i) {
        return 2*i + 1;
    }

    private static int right(int i) {
        return 2 * (i+1);
    }




}
