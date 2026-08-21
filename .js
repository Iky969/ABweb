// Program menghitung total angka 1 sampai 5
let total = 0;
const angkaList = [1, 2, 3, 4, 5];

angkaList.forEach((angka) => {
  total += angka;
  console.log(`Menambahkan ${angka}, total sementara: ${total}`);
});

console.log(`Hasil akhir: ${total}`);
