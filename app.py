import os
from flask import Flask, request, jsonify, send_file
from minio import Minio
from io import BytesIO
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY", "my-secure-api-key")

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "test-bucket")
MINIO_SECURE = os.getenv("MINIO_SECURE", "false").lower() == "true"

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=MINIO_SECURE
)

if not minio_client.bucket_exists(MINIO_BUCKET_NAME):
    minio_client.make_bucket(MINIO_BUCKET_NAME)

def require_api_key(func):
    """
    Decorator to enforce API key authentication.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = request.headers.get("x-api-key")
        if not key or key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return func(*args, **kwargs)
    return wrapper

@app.route('/upload', methods=['POST'])
@require_api_key
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        minio_client.put_object(
            MINIO_BUCKET_NAME,
            file.filename,
            file.stream,
            length=-1,
            part_size=10 * 1024 * 1024
        )
        return jsonify({"message": f"File '{file.filename}' uploaded successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
@require_api_key
def download_file(filename):
    try:
        response = minio_client.get_object(MINIO_BUCKET_NAME, filename)
        return send_file(
            BytesIO(response.read()),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/list-files', methods=['GET'])
@require_api_key
def list_files():
    try:
        objects = minio_client.list_objects(MINIO_BUCKET_NAME)
        files = [obj.object_name for obj in objects]
        return jsonify({"files": files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

