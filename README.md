# UCA Face Recognition Service

A Django-based face recognition service that provides API endpoints for face detection and recognition.

## Features

- Face detection and recognition using dlib and face_recognition libraries
- RESTful API endpoints for face processing
- Secure authentication and authorization
- Docker support for easy deployment
- Database integration for storing face data

## Prerequisites

- Python 3.9+
- Docker (optional, for containerized deployment)
- CMake 3.26+
- Other system dependencies (see Dockerfile for full list)

## Installation

### Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd UCAFaceRecognitionService
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with necessary configuration.

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

### Docker Deployment

1. Build and run using Docker Compose:
```bash
docker-compose -f test.yml up --build
```

The service will be available at `http://localhost:8101`

## Project Structure

```
UCAFaceRecognitionService/
├── api/                    # Main application code
│   ├── migrations/        # Database migrations
│   ├── models.py         # Database models
│   ├── serializers.py    # API serializers
│   ├── views.py          # API views
│   └── urls.py           # API URL routing
├── data/                  # Data processing scripts
├── face_recognition_service/  # Django project settings
├── fixtures/             # Database fixtures
├── media/               # Media files storage
├── static/              # Static files
└── venv/                # Virtual environment
```

## API Endpoints

The service provides RESTful API endpoints for face recognition operations. Detailed API documentation can be accessed at `/api/docs/` when the server is running.

### Code Style
The project follows PEP 8 guidelines for Python code style.

## Environment Variables

Create a `.env` file with the following variables:
```
# Add your environment variables here
```
