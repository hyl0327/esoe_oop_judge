import java.util.Scanner;

class Main {
        public static void main(String[] args) {
                Scanner sc = new Scanner(System.in);

                for (int i = 0; i < 10000; ++i)
                        System.out.println(APlusB.plus(sc.nextInt(), sc.nextInt()));
        }
}
