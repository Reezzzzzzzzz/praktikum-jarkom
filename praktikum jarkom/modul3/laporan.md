# Modul 3 — Analisis Protokol HTTP dengan Wireshark

Modul ini membahas protokol HTTP secara lebih dalam lewat lima skenario percobaan: GET/Response dasar, Conditional GET, dokumen panjang, dokumen dengan embedded object, dan autentikasi password.

---

## 3.1 Basic HTTP GET/Response Interaction

### Langkah Percobaan

**1. Siapkan filter.** Buka Wireshark dan ketik `http` di kolom filter, supaya nanti hanya paket HTTP saja yang tampil.

![Filter http pada Wireshark](../assets/modul3/week3(Gambar1).png)

**2. Mulai capture, lalu akses URL.** Setelah filter siap, klik *start capture*, kemudian buka browser dan masukkan alamat:
`http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file1.html`

![Mengakses URL target](../assets/modul3/week3(Gambar2).png)

**3. Verifikasi tampilan browser.** Halaman menampilkan teks satu baris sebagai tanda file HTML berhasil diunduh. Capture langsung dihentikan begitu halaman muncul.

![Halaman berhasil dimuat](../assets/modul3/week3(Gambar3).png)

**4. Analisis paket GET dan Response.** Pada daftar paket, terlihat satu paket **HTTP GET** dari browser dan satu paket **HTTP 200 OK** sebagai balasan dari server.

![Paket GET dan 200 OK](../assets/modul3/week3(Gambar4).png)

### Ringkasan
* **Method**: GET
* **Status**: 200 OK
* **Source IP**: alamat IP komputer sendiri (client)
* **Destination IP**: `128.119.245.12` (server gaia.cs.umass.edu)

**Kesimpulan**: percobaan ini menunjukkan interaksi HTTP paling sederhana — satu request, satu response — yang menjadi pola dasar dari semua komunikasi web.

---

## 3.2 HTTP Conditional GET/Response Interaction

Bagian ini mengamati bagaimana browser menghemat bandwidth lewat mekanisme *caching*.

### Langkah Percobaan
1. Bersihkan cache dan history browser supaya pengambilan data benar-benar dari server, bukan dari cache lama.
2. Mulai capture di Wireshark.
3. Akses URL `http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file2.html`. Browser menampilkan dokumen HTML pendek lima baris.

![Akses pertama ke file2.html](../assets/modul3/week3(Gambar5).png)

4. Refresh halaman yang sama (atau masukkan ulang URL-nya) untuk memicu Conditional GET pada permintaan kedua.
5. Hentikan capture, lalu terapkan filter `http`.

![Daftar paket setelah refresh](../assets/modul3/week3(Gambar6).png)

### Analisis

**Request pertama** — server membalas dengan `HTTP/1.1 200 OK` dan mengirim seluruh isi file, karena browser belum punya salinannya di cache.

**Request kedua (Conditional GET)** — browser kali ini menyertakan header `If-Modified-Since`, yang intinya bertanya ke server: "kalau file ini belum berubah sejak waktu tersebut, tidak usah dikirim ulang."

![Header If-Modified-Since](../assets/modul3/week3(Gambar7).png)

**Balasan server: 304 Not Modified** — karena file di server memang tidak berubah, server tidak mengirim ulang isinya, cukup membalas dengan status `304 Not Modified`. Browser lalu memakai salinan yang sudah ada di cache lokal.

### Kesimpulan
Conditional GET efektif menghemat penggunaan bandwidth. Lewat status 304, server tidak perlu mengirim ulang data yang sama, sehingga halaman bisa dimuat lebih cepat dan kuota data yang terpakai lebih sedikit.

---

## 3.3 HTTP Retrieval of Long Documents

Bagian ini melihat bagaimana HTTP (dan TCP di bawahnya) menangani file yang ukurannya melebihi satu segmen TCP standar (umumnya di atas 1460 byte).

### Langkah Percobaan
1. Bersihkan cache browser lagi agar file benar-benar diunduh penuh dari server.
2. Akses `http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file3.html`, yang isinya dokumen "US Bill of Rights" — cukup panjang untuk satu halaman HTML.

![Dokumen panjang yang diunduh](../assets/modul3/week3(Gambar10).png)

3. Setelah capture dihentikan, gunakan filter `http` untuk menemukan paket GET-nya, lalu hapus filter (atau ganti ke `tcp`) untuk melihat bagaimana file ini sebenarnya terbagi menjadi banyak paket di level transport.

![Filter tcp memperlihatkan banyak segmen](../assets/modul3/week3(Gambar8).png)

### Analisis Segmentasi
File HTML yang diminta berukuran sekitar 4500 byte. Karena ukuran ini melebihi **Maximum Segment Size (MSS)** dari koneksi TCP, server tidak bisa mengirimkannya dalam satu paket saja.

Pada kolom *Info* di Wireshark, beberapa paket diberi label **"TCP segment of a reassembled PDU"** — artinya satu respons HTTP yang sama dipecah menjadi beberapa segmen TCP berurutan.

![Label "TCP segment of a reassembled PDU"](../assets/modul3/week3(Gambar9).png)

Meski terpecah di lapisan transport, Wireshark tetap mampu menyusunnya kembali (*reassemble*) sehingga di lapisan aplikasi (HTTP) paket-paket itu tetap terlihat sebagai satu respons `200 OK` yang utuh.

### Kesimpulan
* HTTP mengandalkan TCP untuk menangani segmentasi data yang berukuran besar.
* File besar otomatis dipecah jadi segmen-segmen kecil agar aman ditransmisikan tanpa error.
* Wireshark bisa menyusun ulang segmen-segmen itu sehingga isi file HTML tetap bisa dibaca secara utuh di level aplikasi.

---

## 3.4 HTML Documents dengan Embedded Objects

Bagian ini melihat apa yang terjadi ketika satu halaman HTML memuat objek tambahan seperti gambar.

### Langkah Percobaan
1. Akses `http://gaia.cs.umass.edu/wireshark-labs/HTTP-wireshark-file4.html`. Browser menampilkan teks beserta dua gambar (logo Pearson dan sampul buku).

![Halaman dengan dua gambar embedded](../assets/modul3/week3(Gambar11).png)

2. Browser pertama-tama mengirim `GET` untuk file HTML dasarnya. Setelah file ini diterima, browser baru "tahu" bahwa ada dua referensi gambar yang harus diambil juga.

![GET untuk file HTML dasar](../assets/modul3/week3(Gambar13).png)

3. Begitu mengetahui ada objek tambahan, browser otomatis mengirim permintaan `GET` lagi — satu untuk setiap gambar.

![GET untuk masing-masing gambar embedded](../assets/modul3/week3(Gambar14).png)

Sebagai pembanding, berikut tampilan dari panel Network di DevTools browser yang merekam request yang sama: terlihat ada permintaan terpisah untuk `pearson.png` dan `8E_cover_small.jpg` (dua gambar embedded), plus satu permintaan tambahan untuk `favicon.ico` yang gagal (404) karena server tidak menyediakan file ikon tersebut.

![Panel Network DevTools merekam request untuk tiap embedded object](../assets/modul3/week3(Gambar12).png)

### Kesimpulan
* Satu halaman web yang tampak sederhana sering kali sebenarnya terdiri dari banyak file terpisah.
* Browser mengirim permintaan HTTP tersendiri untuk setiap objek yang dirujuk di dalam file HTML dasarnya.
* Pengguna hanya mengetik satu alamat URL, tapi di balik layar terjadi beberapa kali interaksi request-response sekaligus.

---

## 3.5 HTTP Password Authentication

Bagian terakhir menguji bagaimana HTTP menangani halaman yang dilindungi password (Basic Authentication).

### Langkah Percobaan
1. Saat pop-up login muncul, masukkan username dan password yang diminta.

![Pop-up login Basic Authentication](../assets/modul3/week3(Gambar16).png)

2. **Permintaan pertama ditolak (401 Unauthorized).** Saat browser pertama kali meminta halaman tanpa kredensial, server membalas dengan status `401 Unauthorized` — sinyal bagi browser untuk menampilkan dialog login ke pengguna.

![Respons 401 Unauthorized](../assets/modul3/week3(Gambar17).png)

3. **Permintaan kedua berhasil (200 OK).** Setelah username dan password diisi, browser mengirim ulang `GET` dengan tambahan header `Authorization: Basic`. Server memverifikasi kredensial tersebut dan membalas dengan `200 OK`.

![Respons 200 OK setelah autentikasi](../assets/modul3/week3(Gambar18).png)

### Kesimpulan
* Basic Authentication selalu melibatkan minimal dua pasang request/response.
* Permintaan pertama nyaris selalu gagal (401) terlebih dahulu, sebagai pemicu munculnya dialog login.
* Kredensial dikirim dalam header HTTP dengan enkode Base64 — bukan terenkripsi — sehingga koneksi semacam ini idealnya selalu lewat HTTPS agar aman.

---

**Selesai.** Modul ini mencakup seluruh siklus dasar interaksi HTTP: dari request-response sederhana, caching, penanganan dokumen besar, embedded object, sampai autentikasi.
