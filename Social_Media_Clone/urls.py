from django.contrib import admin
from django.urls import path, include
from auth_app.views import landing, about_us
# ----------------------------------------------------
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing, name='landing-page'),
    path('about-us', about_us, name='about-us'),
    path('auth/', include('auth_app.urls')),
    path('profile/', include('profile_app.urls'))]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)