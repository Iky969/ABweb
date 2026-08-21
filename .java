public class Main {
    public static void main(String[] args) {
        int total = 0;
        for (int i = 1; i <= 5; i++) {
            total += i;
            System.out.println("Menambahkan " + i + ", total: " + total);
        }
        System.out.println("Hasil akhir: " + total);
    }
}
