#!/bin/bash

# Wait for MinIO server to be ready
echo "Waiting for MinIO server..."
until curl -s http://localhost:9000/minio/health/live >/dev/null; do
  sleep 1
done

echo "MinIO server is ready!"

# Set environment variables
export MC_HOST_myminio="http://$MINIO_ROOT_USER:$MINIO_ROOT_PASSWORD@localhost:9000"

# Create the bucket if it doesn't exist
BUCKET_NAME="test-bucket"
echo "Creating bucket: $BUCKET_NAME"
mc alias set myminio http://localhost:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"
mc mb --ignore-existing myminio/$BUCKET_NAME

# Apply public read-only policy to the bucket
echo "Applying anonymous download policy to bucket: $BUCKET_NAME"
mc anonymous set download myminio/$BUCKET_NAME

echo "Bucket $BUCKET_NAME is ready for anonymous downloads!"
