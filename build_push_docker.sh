#!/bin/bash
# Pastikan Anda sudah login ke ghcr.io sebelumnya:
# echo "TOKEN_GITHUB_ANDA" | docker login ghcr.io -u khensin166 --password-stdin

IMAGE_NAME="ghcr.io/khensin166/palm-classification-api:latest"

echo "Membangun Docker Image: $IMAGE_NAME"
# Masuk ke folder backend karena Dockerfile ada di sana
cd backend
docker build -t $IMAGE_NAME .

echo "Mendorong Image ke GHCR..."
docker push $IMAGE_NAME

echo "Selesai! Image berhasil di-push. Watchtower di VPS Anda akan otomatis mengambilnya jika dikonfigurasi."
