package main
import "fmt"

func main() {
	total := 0
	for i := 1; i <= 5; i++ {
		total += i
		fmt.Printf("Menambahkan %d, total: %d\n", i, total)
	}
	fmt.Printf("Hasil akhir: %d\n", total)
}
