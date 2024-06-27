from django.conf.urls.static import static
from django.urls import path

from PixelCrypt import settings
from . import views

urlpatterns = [
    path('embed/', views.embed_message, name='embed_message'),
    path('extract/', views.extract_message, name='extract_message'),
    path('user-bmp-images/', views.user_bmp_images, name='user_bmp_images'),
    path('about_authors/', views.about_authors_view, name='about_authors'),
    path('', views.about_program_view, name='about_program'),
    path('user_manual/', views.user_manual_view, name='user_manual'),
    path('create_bmp/', views.create_bmp, name='create_bmp'),
    path('image/<int:image_id>/', views.image_detail, name='image_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
