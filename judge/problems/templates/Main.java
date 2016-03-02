import java.io.IOException;
import java.io.PrintWriter;
import java.io.File;
import java.math.BigDecimal;
import java.math.RoundingMode;

public class Main {
        private static int n_correct = 0, n_total = 0;

        public static void main(String args[]) throws IOException {
                PrintWriter out = new PrintWriter(new File("score"));

                System.setSecurityManager(new SecurityManager());

                /* test code here */

                out.print(n_correct);
                out.print(",");
                out.print(n_total);
                out.print(",");
                out.print((new BigDecimal(n_correct))
                          .divide(new BigDecimal(n_total), 4, RoundingMode.HALF_UP)
                          .multiply(new BigDecimal(100))
                          .setScale(2, RoundingMode.HALF_UP));
                out.print("\n");
                out.close();
        }

        private static void _s(boolean predicate) {
                if (predicate)
                        ++n_correct;
                ++n_total;
        }
}
