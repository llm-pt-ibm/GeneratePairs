import java.util.Scanner;

class TorreDeHanoi {


    public void torreDeHanoi(int qntdDiscos, String hasteDeSaida, String hasteDeChegada, String hasteAuxiliar){
        if (qntdDiscos == 1) {
            System.out.println("Move o disco 1 da haste " + hasteDeSaida + " para a haste " + hasteDeChegada);
            return;
        }
        torreDeHanoi(qntdDiscos - 1, hasteDeSaida, hasteAuxiliar, hasteDeChegada);
        System.out.println("Move o disco " + qntdDiscos + " da haste " + hasteDeSaida + " para a haste " + hasteDeChegada);
        torreDeHanoi(qntdDiscos - 1, hasteAuxiliar, hasteDeChegada, hasteDeSaida);
    }

    public static void main (String[] args) {
        TorreDeHanoi th = new TorreDeHanoi();
        Scanner sc = new Scanner(System.in);
        int qntdDiscos = Integer.parseInt(sc.nextLine());
        th.torreDeHanoi(qntdDiscos, "A", "C", "B");
    }

}
