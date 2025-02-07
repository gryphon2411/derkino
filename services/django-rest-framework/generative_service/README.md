# Django REST Framework Generative Service

## Setup

```bash
$ basename $(pwd)
django-rest-framework

$ mkdir generative_service

# Open generative_service with PyCharm and python3.10 virtual environment

(venv) $ pip install uwsgi django djangorestframework requests huggingface_hub pika
(venv) $ django-admin startproject generative_service .
(venv) $ django-admin startapp generative_service_app
```

## Setup (Obsolete)

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

### Gemma

Gemma is provided under and subject to the Gemma Terms of Use found at [ai.google.dev/gemma/terms](ai.google.dev/gemma/terms).

#### Use Restrictions

You must not use any of the Gemma Services:

1. for the restricted uses set forth in the Gemma Prohibited Use Policy at [ai.google.dev/gemma/prohibited_use_policy](ai.google.dev/gemma/prohibited_use_policy) (“Prohibited Use Policy”), which is hereby incorporated by reference into this Agreement; or 
2. in violation of applicable laws and regulations.

To the maximum extent permitted by law, Google reserves the right to restrict (remotely or otherwise) usage of any of the Gemma Services that Google reasonably believes are in violation of this Agreement.
