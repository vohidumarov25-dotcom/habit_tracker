from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class KunTartibi(models.Model):
    """Foydalanuvchining kun tartibi (odati)"""
    nomi = models.CharField(max_length=100, verbose_name="Nomi")
    tavsif = models.TextField(blank=True, verbose_name="Tavsif")
    foydalanuvchi = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kun_tartiblari')
    yaratilgan_sana = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    rang = models.CharField(max_length=7, default='#4CAF50', verbose_name="Rang (hex)")
    faol = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        db_table = 'kun_tartibi'
        ordering = ['-yaratilgan_sana']
        verbose_name = 'Kun tartibi'
        verbose_name_plural = 'Kun tartiblari'

    def __str__(self):
        return self.nomi


class KunTartibiKunligi(models.Model):
    """Kun tartibi bo'yicha kunlik qayd"""
    kun_tartibi = models.ForeignKey(KunTartibi, on_delete=models.CASCADE, related_name='kunliklar')
    sana = models.DateField(default=timezone.now, verbose_name="Sana")
    bajarildi = models.BooleanField(default=True, verbose_name="Bajarildi")
    izoh = models.TextField(blank=True, verbose_name="Izoh")

    class Meta:
        db_table = 'kun_tartibi_kunligi'
        unique_together = ['kun_tartibi', 'sana']
        ordering = ['-sana']
        verbose_name = 'Kunlik qayd'
        verbose_name_plural = 'Kunlik qaydlar'

    def __str__(self):
        return f"{self.kun_tartibi.nomi} - {self.sana}"