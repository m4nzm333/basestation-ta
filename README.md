# Basestation for Research

Ini adalah project skripsi tentang salah satu proses kerja Basestation yang dipasang pada Raspberry Pi dengan judul "Rancang Bangun Base Station untuk Monitoring Kualitas Udara Kota Makassar"

## Kebutuhan

1. Python 3.x
2. Library Paho-MQTT
3. Library rasp.BME280
4. Library SMBus

## Instalasi

1. Ambil source codenya terlebih dahulu
```
$ git clone https://gitlab.com/m4nzm333/basestation-ta
```
2. Install library Paho-MQTT
```
$ pip3 install Paho-MQTT
```
3. Install library BME280
```
$ pip3 install rasp.bme280
```

4. Install library BME280
```
$ pip3 install rasp.bme280
```

5. Install library SMBus
```
$ pip3 install smbus
```

6. Jalankan Main Program
```
$ python3 MainProgram.py
```
## Alur Sistem

1. Menerima Data

* Cara 1 : Terima data sensor dengan mengakses API (http). Bentuk data dalam file tersebut berdasarkan baris per baris:
```
id=abc,temp=xx,long=xxx.xxx,lat=xxx.xxx,timestamp=yyyy-mm-dd HH:MM:ss.sss
```
| Parameter | Kebutuhan|      Keterangan                                                                                         |
|-----------|----------|--------------------------------------------------------------------------------------------------------:|
| id        | required | id sensor yang mengirim (contoh: Basestation-A1)                                                        |
| temp      | required | "temp" adalah nama variabel sensor, nama varibel boleh diganti kemudian diikuti nilai variabel tersebut |
| long      | optional | longitude atau garis bujur                                                                              |
| lat       | optional | latitude atau garis lintang                                                                             |
| timestamp | optional | waktu saat sensor mengambil data                                                                        |

* Cara 2 : Terima data sensor melalui broker dengan subscribe ke topic sesuai jenis sensor. Data yang diterima berupa string:
```
abc,xx,xxx.xxx,xxx.xxx,yyyy-mm-dd HH:MM:ss.sss
```
Data disusun berdasarkan urutan:
| Parameter | Kebutuhan|      Keterangan                                                                                         |
|-----------|----------|--------------------------------------------------------------------------------------------------------:|
| id        | required | id sensor yang mengirim (contoh: Basestation-A1)                                                        |
| temp      | required | "temp" adalah nama variabel sensor, nama varibel boleh diganti kemudian diikuti nilai variabel tersebut |
| long      | optional | longitude atau garis bujur                                                                              |
| lat       | optional | latitude atau garis lintang                                                                             |
| timestamp | optional | waktu saat sensor mengambil data                                                                        |

2. Penyaringan Data
Untuk saat ini, filtering data hanya dengan metode eliminasi untuk mengetahui data valid atau tidak. Data yang bernilai 0.0 atau negatif akan dibuang/dilewati (tidak dikirim ke server)

2. Mengirim Data
Proses pengiriman data ke server adalah melalui MQTT broker yang ada di server. Basestation akan mengirimkan data dengan publish ke topic sesuai paremeter sensor. Data yang dikirim sama dengan model data yang diterima oleh basestation dari sensor Cara 2

## Tim Pengembang (Developer)

* [Irman Mashuri / m4nzm333](https://gitlab.com/m4nzm333)

## Catatan
Copyright (c) 2020 by [Irman Mashuri / m4nzm333](https://gitlab.com/m4nzm333)
