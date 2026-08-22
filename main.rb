# Program menghitung total angka 1 sampai 5
total = 0
(1..5).each do |i|
  total += i
  puts "Menambahkan #{i}, total sementara: #{total}"
end

puts "Hasil akhir: #{total}"
# Selesai
