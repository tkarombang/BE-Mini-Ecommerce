# Menggunakan base image Python resmi
FROM python:3.13.5

# Menetapkan direktori kerja
WORKDIR /app

# Menginstal dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin kode aplikasi
COPY . .

# Menentukan port yang akan diekspos
EXPOSE 8080

# Menjalankan aplikasi
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "$PGPORT"]