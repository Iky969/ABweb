section .data
    msg1 db "Memulai perhitungan...", 10
    len1 equ $ - msg1
    msg2 db "Selesai! Hasil ada di register RAX.", 10
    len2 equ $ - msg2

section .text
    global _start

_start:
    ; --- 1. Cetak Pesan Pertama ke Layar ---
    mov rax, 1          ; Syscall number untuk sys_write
    mov rdi, 1          ; File descriptor 1 (stdout / layar)
    mov rsi, msg1       ; Alamat memori teks pertama
    mov rdx, len1       ; Panjang teks pertama
    syscall             ; Panggil Kernel Linux

    ; --- 2. Proses Logika & Komputasi ---
    mov rax, 15         ; Masukkan angka 15 ke register RAX
    mov rbx, 25         ; Masukkan angka 25 ke register RBX
    add rax, rbx        ; Tambahkan nilai RBX ke RAX (RAX sekarang bernilai 40)

    ; --- 3. Cetak Pesan Kedua ke Layar ---
    mov rax, 1          ; Syscall number untuk sys_write
    mov rdi, 1          ; File descriptor 1 (stdout)
    mov rsi, msg2       ; Alamat memori teks kedua
    mov rdx, len2       ; Panjang teks kedua
    syscall             ; Panggil Kernel Linux

    ; --- 4. Keluar dari Program (Exit) ---
    mov rax, 60         ; Syscall number untuk sys_exit
    mov rdi, 0          ; Return code 0 (Sukses)
    syscall             ; Panggil Kernel Linux
