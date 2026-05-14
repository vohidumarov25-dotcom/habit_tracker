from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import KunTartibi, KunTartibiKunligi
from .serializers import KunTartibiSerializer, KunTartibiKunligiSerializer, FoydalanuvchiSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class FoydalanuvchiViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = FoydalanuvchiSerializer
    permission_classes = [permissions.AllowAny]


class KunTartibiViewSet(viewsets.ModelViewSet):
    serializer_class = KunTartibiSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return KunTartibi.objects.filter(foydalanuvchi=self.request.user, faol=True)

    def perform_create(self, serializer):
        serializer.save(foydalanuvchi=self.request.user)

    @action(detail=True, methods=['post'])
    def bajarildi_belgila(self, request, pk=None):
        """Kun tartibini bajarilgan deb belgilash"""
        kun_tartibi = self.get_object()
        sana = request.data.get('sana', timezone.now().date())
        izoh = request.data.get('izoh', '')

        kunlik, yaratildi = KunTartibiKunligi.objects.get_or_create(
            kun_tartibi=kun_tartibi,
            sana=sana,
            defaults={'bajarildi': True, 'izoh': izoh}
        )

        if not yaratildi:
            kunlik.bajarildi = True
            kunlik.izoh = izoh
            kunlik.save()

        return Response({
            'holat': 'qayd_etildi',
            'kun_tartibi': KunTartibiSerializer(kun_tartibi).data
        })

    @action(detail=True, methods=['post'])
    def utkazib_yubor(self, request, pk=None):
        """Kunni o'tkazib yuborish"""
        kun_tartibi = self.get_object()
        sana = request.data.get('sana', timezone.now().date())

        kunlik, yaratildi = KunTartibiKunligi.objects.get_or_create(
            kun_tartibi=kun_tartibi,
            sana=sana,
            defaults={'bajarildi': False, 'izoh': "O'tkazib yuborildi"}
        )

        return Response({'holat': "o'tkazib_yuborildi"})

    @action(detail=False, methods=['get'])
    def statistika(self, request):
        """Umumiy statistika"""
        kun_tartiblari = self.get_queryset()
        jami_kun_tartiblari = kun_tartiblari.count()
        bugun_bajarilgan = sum(1 for kt in kun_tartiblari
                               if kt.kunliklar.filter(sana=timezone.now().date(), bajarildi=True).exists())

        return Response({
            'jami_kun_tartiblari': jami_kun_tartiblari,
            'bugun_bajarilgan': bugun_bajarilgan,
            'bajarish_foizi': round((bugun_bajarilgan / jami_kun_tartiblari * 100) if jami_kun_tartiblari > 0 else 0, 2)
        })