from rest_framework import serializers
from django.contrib.auth.models import User
from .models import KunTartibi, KunTartibiKunligi
from django.utils import timezone


class FoydalanuvchiSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class KunTartibiKunligiSerializer(serializers.ModelSerializer):
    class Meta:
        model = KunTartibiKunligi
        fields = ['id', 'kun_tartibi', 'sana', 'bajarildi', 'izoh']
        read_only_fields = ['kun_tartibi']


class KunTartibiSerializer(serializers.ModelSerializer):
    kunliklar = KunTartibiKunligiSerializer(many=True, read_only=True)
    foydalanuvchi = serializers.ReadOnlyField(source='foydalanuvchi.username')
    bajarish_foizi = serializers.SerializerMethodField()

    class Meta:
        model = KunTartibi
        fields = ['id', 'nomi', 'tavsif', 'foydalanuvchi', 'yaratilgan_sana',
                  'rang', 'faol', 'kunliklar', 'bajarish_foizi']
        read_only_fields = ['foydalanuvchi']

    def get_bajarish_foizi(self, obj):
        umumiy_kunlar = (timezone.now().date() - obj.yaratilgan_sana.date()).days + 1
        bajarilgan_kunlar = obj.kunliklar.filter(bajarildi=True).count()
        if umumiy_kunlar == 0:
            return 0
        return round((bajarilgan_kunlar / umumiy_kunlar) * 100, 2)