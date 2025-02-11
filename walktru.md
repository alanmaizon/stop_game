1. Set Up Your Django Project

mkdir fileupload
cd fileupload
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install django psycopg2

2. Start a Django Project
django-admin startproject file_app .

3. Change permissions on your postgres database
-- Run the following commands using pgadmin, psql
-- replace 'library_pm6c' with your Render database name
-- replace 'library_pm6c_user' with your Render postgres user name
\c library_pm6c -- connect to the database (Do not need this if you right click the database and then choose psql
ALTER ROLE library_pm6c_user SET client_encoding TO 'utf8';
ALTER ROLE library_pm6c_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE library_pm6c_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE library_pm6c TO library_pm6c_user;

4. Setup postgres database in settings.python
pip install dj-database-url
Set Up the DATABASES Configuration: Modify your settings.py to use the DATABASE_URL environment variable:
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://<username>:<password>@localhost:5432/<dbname>'
    )
}
Replace the username, password and dbname with your Render details. Or just copy your Render external URL

5. Note for deployment, store the Render postgres Database url as an environment variable and call it like below
// update this 
DATABASES = {
    'default': dj_database_url.config()
}

6. create a new Django App called file_manager
python manage.py startapp file_manager (make sure you are in the same directory as manage.py)

7. Add file_manager to INSTALLED_APPS in settings.py:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'file_manager',
]

8. Define the Model in file_manager/models.py
from django.db import models

class File(models.Model):
    name = models.CharField(max_length=255)  # File name
    content = models.BinaryField()  # Binary file data
    content_type = models.CharField(max_length=100)  # File MIME type
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return self.name

9. Apply migrations
python manage.py makemigrations
python manage.py migrate

10. Create forms and views
In file_manager/forms.py, create a form for file uploads:
from django import forms
from django.core.exceptions import ValidationError

ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

class FileUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']

        # Check file type
        if uploaded_file.content_type not in ALLOWED_IMAGE_TYPES:
            raise ValidationError('Invalid file type. Only image files are allowed.')

        # Check file size
        if uploaded_file.size > MAX_FILE_SIZE:
            raise ValidationError(f'File size exceeds the limit of {MAX_FILE_SIZE // (1024 * 1024)} MB.')

        return uploaded_file


11. Views for Uploading and Retrieving Files
In file_manager/views.py, create views for file upload and file retrieval:
from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import FileUploadForm
from .models import File

# Allowed image MIME types
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']

# Maximum file size (in bytes)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

# File upload view
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            File.objects.create(
                name=uploaded_file.name,
                content=uploaded_file.read(),
                content_type=uploaded_file.content_type,
            )
            messages.success(request, 'File uploaded successfully!')
            return redirect('upload_file')
    else:
        form = FileUploadForm()
    files = File.objects.all().order_by('-id')[:5]
    return render(request, 'file_manager/upload.html', {'form': form, 'files':files})

# File download view
def download_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    response = HttpResponse(file.content, content_type=file.content_type)
    response['Content-Disposition'] = f'attachment; filename="{file.name}"'
    return response

def display_image(request, file_id):
    file = get_object_or_404(File, id=file_id)
    return HttpResponse(file.content, content_type=file.content_type)



12. Create templates
Upload Form Template (file_manager/templates/file_manager/upload.html):
<!DOCTYPE html>
<html>
<head>
    <title>Upload Image</title>
</head>
<body>
    {% if messages %}
    <div class="messages">
        {% for message in messages %}
            <div class="alert {% if message.tags %}alert-{{ message.tags }}{% endif %}">
                {{ message }}
            </div>
        {% endfor %}
    </div>
    {% endif %}
    <h1>Upload an Image</h1>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Upload</button>
    </form>

    <h2>Uploaded Images</h2>
    {% for file in files %}
        <div>
            <h3>{{ file.name }}</h3>
            <img src="/file/{{ file.id }}" alt="{{ file.name }}" style="max-width: 200px;">
        </div>
    {% endfor %}
</body>
</html>


13. Configure URLs
In file_manager/urls.py, define routes for file upload and download:
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('file/<int:file_id>/', views.display_image, name='display_image'),
]

14. In the main file_app/urls.py, include the app's URLs:
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('file_manager.urls')),
]

15. Run the server and test
python manage.py runserver

point your browser to http://127.0.0.1:8000/upload/ 
Things to try: 
upload valid images which confirm to the file type and size
Note only the latest 5 images are displayed

