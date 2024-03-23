# Django REST Framework Generative Service

## Setup

```bash
$ basename $(pwd)
django-rest-framework

$ mkdir generative_service

# Open generative_service with PyCharm and python3.10 virtual environment

(venv) $ pip install django djangorestframework transformers pip tensorflow
(venv) $ pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
(venv) $ django-admin startproject generative_service .
(venv) $ django-admin startapp generative_service_app
```
