<?php
// Program menghitung total angka 1 sampai 5
$total = 0;

for ($i = 1; $i <= 5; $i++) {
    $total += $i;
    echo "Menambahkan $i, total sementara: $total\n";
}

echo "Hasil akhir: $total\n";
?>
