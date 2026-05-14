from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import KunTartibiViewSet, FoydalanuvchiViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'kun-tartibi', KunTartibiViewSet, basename='kun-tartibi')
router.register(r'foydalanuvchilar', FoydalanuvchiViewSet, basename='foydalanuvchi')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/kirish/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token-yangilash/', TokenRefreshView.as_view(), name='token_refresh'),
]