# Tugas Kecil 3 IF2211 Strategi Algoritma 2021/2022

13520024 Hilya Fadhilah Imania

## Deskripsi Singkat

Program ini adalah program pencarian solusi Puzzle-15 dengan
algoritma Branch and Bound. Heuristik yang digunakan untuk
menghitung cost adalah jumlah sel yang tidak berada pada
tempatnya.

> Program dapat menerima masukan puzzle berukuran apapun,
> tidak hanya 4x4.

## Requirements dan Run

Program ditulis dalam bahasa Python 3.10. Secara default,
program diasumsikan dijalankan secara interaktif pada platform
console yang memiliki support untuk ANSI Escape Sequence.

Untuk menyelesaikan persoalan Puzzle-15 random:

```
$ python3 solver.py
```

Untuk menyelesaikan persoalan dari sebuah file:

```
$ python3 solver.py test/1.txt
```

Untuk noninteraktif, atau platform yang tidak support ANSI
Escape Sequence:

```
$ python3 solver.py --verbose
$ python3 solver.py test/1.txt --verbose
$ python3 solver.py test/1.txt --verbose > test/result/1.txt
```

## License

[MIT](https://opensource.org/licenses/MIT)

Copyright (C) 2022, Hilya Fadhilah Imania
