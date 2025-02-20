# Lipsync Project
Lipsync is a project focused on generating accurate lip movements synchronized with audio input. This project leverages machine learning techniques to analyze speech patterns and generate realistic facial animations.
## Overview
This project generates a lip-synced video by processing an image and an audio file (or a generated script). The core functionality is handled using Wav2Lip and ElevenLabs for text-to-speech generation.

## Prerequisites
- Python 3.8.20
- Virtual environment setup
- Required dependencies
- Django setup

## Setup Instructions

### 1. Create a Virtual Environment
```sh
python3 -m venv venv
```
Activate the virtual environment:
- On Windows:
  ```sh
  venv\Scripts\activate
  ```
- On macOS/Linux:
  ```sh
  source venv/bin/activate
  ```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Set Up Django Project
```sh
django-admin startproject lipsync_project
cd lipsync_project
python manage.py startapp lipsync
```

### 4. Configure Django Views
- Copy the `views.py` code into the `lipsync/views.py` file.
- Add routing in `lipsync/urls.py`:

```python
from django.urls import path
from .views import process_lipsync

urlpatterns = [
    path('lipsync/', process_lipsync, name='lipsync'),
]
```

- Include the app URLs in `lipsync_project/urls.py`:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lipsync.urls')),
]
```

### 5. Run the Project
```sh
python manage.py runserver
```

The application should now be accessible at `http://127.0.0.1:8000/lipsync/`.
