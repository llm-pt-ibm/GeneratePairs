import java.util.*;
import java.math.*;
class M {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = Integer.parseInt(sc.nextLine());
        String out = "";

        String[] lines = sc.nextLine().split(" ");

        for (int i = 0; i < lines.length; i++) {
            out = out + Integer.toString((Integer.parseInt(lines[i])*n)) + " ";
        }

        System.out.println(out.trim());
    
    }
}
