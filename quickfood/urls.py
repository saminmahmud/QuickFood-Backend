from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from users.views import CustomTokenObtainPairView, CustomTokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('order/', include('order.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
