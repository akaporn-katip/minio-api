# MinIO Flask API

This project provides a RESTful API for file upload, download, and listing using Flask and MinIO. The API is secured with an API key and allows anonymous download functionality. It is containerized with Docker and can be easily deployed using Docker Compose.

---

## Features

1. **Upload Files**: Upload files to a specific bucket in MinIO.
2. **Download Files**: Securely download files using an API key.
3. **List Files**: Retrieve a list of files stored in the bucket.
4. **Anonymous Download**: Pre-configured support for public access to certain buckets.
5. **Dockerized**: Fully containerized application using Docker and Docker Compose.
6. **API Key Security**: Secures all endpoints except anonymous download with an API key.

---

## Prerequisites

1. Docker and Docker Compose installed.
2. Python 3.9 or higher (if running locally).
3. MinIO installed and accessible.

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Environment Configuration

Create a `.env` file in the root directory with the following:

```env
# MinIO Configuration
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=test-bucket
MINIO_SECURE=false

# API Key for Secure Access
API_KEY=my-secure-api-key
```

---

## Usage

### 1. Build and Start the Application

Run the following command to build and start the application:

```bash
docker-compose up --build
```

### 2. API Endpoints

#### Upload File
- **Endpoint**: `/upload`
- **Method**: `POST`
- **Headers**:
  - `x-api-key`: API key for authentication.
- **Request Body**: File upload (`multipart/form-data`).

**Example (cURL):**
```bash
curl -X POST -H "x-api-key: my-secure-api-key" \
  -F "file=@/path/to/file.jpg" \
  http://localhost:5000/upload
```

#### Download File
- **Endpoint**: `/download/<filename>`
- **Method**: `GET`
- **Headers**:
  - `x-api-key`: API key for authentication.

**Example (cURL):**
```bash
curl -X GET -H "x-api-key: my-secure-api-key" \
  http://localhost:5000/download/file.jpg -O
```

#### List Files
- **Endpoint**: `/list-files`
- **Method**: `GET`
- **Headers**:
  - `x-api-key`: API key for authentication.

**Example (cURL):**
```bash
curl -X GET -H "x-api-key: my-secure-api-key" \
  http://localhost:5000/list-files
```

### 3. Anonymous Download
- Public files can be accessed directly without an API key.
- Example URL: `http://localhost:9000/test-bucket/<filename>`

---

## Project Structure

```
project-folder/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Dockerfile for the Flask app
├── docker-compose.yml     # Docker Compose configuration
├── .env                   # Environment variables
├── minio-init/            # MinIO initialization scripts
│   └── create-bucket.sh   # Script to create buckets and set policies
└── README.md              # Project documentation
```

---

## Development

### Local Development

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask app:
   ```bash
   python app.py
   ```

### Testing

- Use tools like `curl`, Postman, or automated testing frameworks to test API endpoints.

---

## Known Issues

- Ensure the bucket exists before uploading files.
- Restart the application if the MinIO server is restarted.

---

## Contributing

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit.
4. Push your branch and open a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Support

For any questions or issues, please create an issue in the GitHub repository.

