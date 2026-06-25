# Modul 1 — Instalasi Wireshark

## Tujuan
Sebelum bisa menganalisis lalu lintas data di jaringan, hal pertama yang perlu disiapkan adalah alat untuk menyadap dan membaca paketnya. Modul ini berisi langkah instalasi **Wireshark**, packet sniffer yang akan dipakai terus-menerus di modul-modul selanjutnya.

## Langkah Instalasi

1. **Unduh installer.** Buka situs resmi Wireshark di https://www.wireshark.org, lalu pilih installer yang sesuai dengan sistem operasi yang dipakai (untuk laporan ini menggunakan Windows x64 Installer).
2. **Jalankan installer.** Buka file `.exe` yang sudah diunduh, kemudian klik **Next** pada jendela *Welcome to Wireshark Setup*.
3. **Setujui lisensi.** Baca *License Agreement* sekilas, lalu klik **Noted** untuk lanjut.
4. **Pilih komponen & lokasi instalasi.** Komponen yang ditawarkan (*Choose Components*) dibiarkan default saja. Folder instalasi juga dibiarkan default (`C:\Program Files\Wireshark`), lalu klik **Next**.
5. **Centang instalasi Npcap.** Ini bagian yang paling penting — pada langkah *Packet Capture*, pastikan opsi **Install Npcap** tercentang. Tanpa Npcap, Wireshark tidak akan bisa menangkap trafik jaringan secara langsung karena driver inilah yang menjembatani Wireshark dengan kartu jaringan.
6. **USBPcap (opsional).** Karena kebutuhan saat ini hanya untuk memonitor jaringan LAN/internet biasa, opsi *USB Capture* tidak perlu dicentang. Klik **Install**.
7. **Tunggu proses instalasi.** Jika muncul pop-up instalasi Npcap di tengah jalan, ikuti saja sampai selesai (*Finish*), baru lanjutkan instalasi utama Wireshark dengan klik **Next** lalu **Finish**.
8. **Verifikasi.** Buka aplikasi Wireshark yang baru terinstal untuk memastikan programnya bisa jalan dengan normal.

## Hasil

Setelah instalasi selesai, Wireshark berhasil dibuka dan menampilkan halaman awal berisi daftar antarmuka jaringan yang tersedia di komputer (Wi-Fi, Ethernet, Local Area Connection, dan lain-lain). Munculnya daftar interface ini menjadi tanda bahwa Npcap sudah terpasang dengan benar dan Wireshark siap digunakan untuk menangkap paket.

![Hasil instalasi Wireshark](../assets/modul1/week1.png)
