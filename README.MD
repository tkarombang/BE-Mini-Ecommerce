# Mini E-Commerce Project

Aplikasi mini e-commerce sederhana yang memungkinkan pengguna untuk melihat daftar produk, melakukan checkout sebagai guest, dan melihat daftar pesanan. Dibangun menggunakan **Python FastAPI** dan **PostgreSQL** sebagai database.

## Prerequisite
   - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/windows11/windows11-original.svg" width="20" height="20" /> **Microsoft Windows 11**
   - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/visualstudio/visualstudio-plain.svg" width="20" height="20" /> **Visual Studio Code**
   - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg" width="20" height="20" /> **Extension for vscode** (Pylance, Python, Python, Debugger, Python Environment, yapf)
   - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="20" height="20" /> **Python 3.9+**: Pastikan Python sudah terinstall di komputer kamu.
   - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" width="20" height="20" /> **Git**: Untuk melakukan clone repository dari GitHub.
   - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/chrome/chrome-original.svg" width="20" height="20" /> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/firefox/firefox-original.svg" width="20" height="20" /> **Browser** (Chrome/Firefox)
   - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="20" height="20" />  **PgAdmin** for Management Database
   - <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="20" height="20" />  **PostgreSQL**: Database PostgreSQL yang aktif dan dapat diakses oleh aplikasi. Kamu bisa mengunduh dan menginstall PostgreSQL dari [sini](https://www.postgresql.org/download/).
   - ![pip](https://img.shields.io/badge/pip-21.0.1-61C9FF?style=flat-square&logo=pypi&logoColor=white) **pip**: Python package installer, untuk menginstal dependensi proyek.



## Fitur

- Melihat daftar produk
- Melakukan checkout sebagai guest dengan Form sederhana (on Dev)
- Melihat daftar dan detail pesanan (on Dev)
- Menggunakan Swagger UI untuk dokumentasi API dan pengujian

## Teknologi yang Digunakan

- ![Python](https://img.shields.io/badge/Python-3.9-blue) **Python**: Bahasa pemrograman utama yang digunakan untuk backend.
- ![FastAPI](https://img.shields.io/badge/FastAPI-0.75-blue) **FastAPI**: Framework Python untuk membangun RESTful API yang cepat.
- ![Uvicorn](https://img.shields.io/badge/Uvicorn-0.15-blue) **Uvicorn**: ASGI server untuk menjalankan aplikasi FastAPI secara asinkron.
- ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue) **PostgreSQL**: Database relasional yang digunakan untuk menyimpan data produk dan pesanan.
- ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4-blue) **SQLAlchemy**: ORM untuk berinteraksi dengan database PostgreSQL.
- ![Pydantic](https://img.shields.io/badge/Pydantic-1.8-blue) **Pydantic**: Library untuk validasi dan parsing data menggunakan tipe data Python yang ketat.
- ![Alembic](https://img.shields.io/badge/Alembic-1.7-blue) **Alembic**: Tool untuk mengelola migrasi database menggunakan SQLAlchemy.

## Persyaratan Fungsional

1. **Form Checkout Sederhana untuk Guest**  
   Form ini memungkinkan pengguna guest untuk melakukan checkout. Pengguna harus mengisi nama, email, dan alamat pengiriman, serta memilih produk yang ingin dibeli. (Masih dalam tahap pengembangan)

2. **Menyimpan Pesanan ke Database & Konfirmasi**  
   Setelah checkout, pesanan harus disimpan dalam database PostgreSQL, dan pengguna akan menerima konfirmasi berupa ID pesanan dan status pesanan.

3. **Menampilkan Daftar dan Detail Pesanan**  
   Pengguna dapat melihat daftar pesanan yang telah mereka buat dan juga melihat detail dari setiap pesanan, seperti produk yang dibeli, jumlah, dan status pesanan.

## Persyaratan Teknis

1. **Membuat RESTful API menggunakan FastAPI (Python)**  
   Aplikasi harus dibangun dengan FastAPI dan mengikuti prinsip RESTful API, yaitu menggunakan metode HTTP yang sesuai (GET, POST, PUT, DELETE).

2. **Type Safety dengan Pydantic untuk FastAPI**  
   Validasi data menggunakan Pydantic, yang memungkinkan penggunaan tipe data yang ketat untuk memastikan request dan response API memiliki format yang benar.

3. **Validasi dan Error Handling**  
   Aplikasi harus menyediakan validasi input dan menangani error dengan baik. Misalnya, ketika data checkout tidak valid atau request API gagal, aplikasi harus memberikan response error yang jelas.



## Instalasi

1. Clone repository ini ke dalam direktori lokal:
   ```bash
   git clone https://github.com/tkarombang/BE-Mini-Ecommerce
   ```
2. Masuk kedalam direktori project
    ```bash
    cd be-mini-ecommerce
    ```
3. Buat virtual environment dan aktifkan
    ```bash
    python -m venv venv
    # Os Windows
    venv\Scripts\activate
    ```
4. Install Dependensi yang diperlukan
    ```bash
    pip install fastapi
    docs: https://fastapi.tiangolo.com/tutorial

    pip install uvicorn
    docs: https://www.uvicorn.org/

    pip install SQLAlchemy
    docs: https://docs.sqlalchemy.org/en/20/intro.html#installation

    docs: https://www.sqlalchemy.org/
    ```
5. Install PostgreSQL v17
docs: https://www.postgresql.org/download/windows/

## Menjalankan Aplikasi
```bash
uvicorn app.main:app --reload
```
### STRUKTUR FOLDER
    
```bash
├── app/
│   ├── __init__.py
│   ├── main.py             # Entry point untuk FastAPI
│   ├── models.py           # Definisi model database menggunakan SQLAlchemy
│   ├── schemas.py          # Pydantic schema untuk validasi
│   ├── crud.py             # Fungsi CRUD untuk interaksi dengan database
│   ├── database.py         # Konfigurasi dan koneksi ke database PostgreSQL
│   ├── api/
│   │   ├── __init__.py
│   │   └── product.py      # API untuk produk
│   │   └── order.py        # API untuk pesanan
│   └── alembic.ini         # Konfigurasi untuk Alembic
├── alembic/
│   └── versions/           # Folder untuk menyimpan migrasi database Alembic
├── requirements.txt        # Daftar dependensi Python
└── README.md               # Dokumentasi proyek ini
```

## PENGGUNAAN API
1. Daftar Product
    - Endpoint: GET /products
    - Deskripsi: Mengambil daftar semua produk.
    - Response:
    ```json
    {
        "nama": "RK Tactichal Keyboard",
        "price": 12000000,
        "deskripsi": "Keyboard mekanikal dengan pencahayaan RGB yang halus dan responsif.",
        "kategori": "Aksesoris Komputer",
        "stok": 5,
        "rating": 4.6,
        "image": "/assets/keyboard.jpg",
    }
    ```

2. Checkout Guest
    - Endpoint: POST /checkout
    - Deskripsi: Mengambil data checkout dari guest, dan menyimpan pesanan ke database.
    - Body:
    ```json
    {
        "customer_name": "Muhammad Azwar Anas", (on Dev) 
        "customer_email": "muhanaz@gmail.com",  (on Dev) 
        "items": [
            {"product_id": 1, "quantity": 2},
        ]
    }
    ```
3. Daftar Pesanan
     - Endpoint: GET /orders
     - Deskripsi: Mengambil daftar semua pesanan.
     - Response:
     ```json
     [
        {
            "id": 28,
            "total_price": 8000000,
            "created_at": "2025-08-15T11:31:50.273834+08:00",
            "items": [
                {
                    "id": 28,
                    "product_id": 5,
                    "quantity": 1,
                    "price": 8000000,
                    "product": {
                        "nama": "Smartphone Samsung Galaxy",
                        "price": 8000000,
                        "deskripsi": "Smartphone dengan kamera terbaik",
                        "kategori": "Elektronik",
                        "stok": 14,
                        "rating": 4.7,
                        "image": "/assets/samsung-galaxy.jpg",
                        "id": 5
                    }
                }
            ]
        },
     ]
     ```

## Pengujian
Setelah menjalankan aplikasi, kamu dapat mengakses Swagger UI untuk menguji endpoint API secara interaktif melalui browser.



Muhammad Azwar Anas.
Tanggal: 13 Agustus 2025
Kunjungi profil LinkedIn saya di: https://www.linkedin.com/in/muhanaz dedicated for Redkendi
