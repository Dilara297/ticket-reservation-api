from django.db import models
from django.contrib.auth.models import User

class Sefer(models.Model):
    kalkis_yeri = models.CharField(max_length=100)
    varis_yeri = models.CharField(max_length=100)
    hangi_otobus = models.CharField(max_length=100)
    kalkis_zamani = models.DateTimeField()

    def __str__(self):
        return f"{self.kalkis_yeri} - {self.varis_yeri} ({self.hangi_otobus})"

class Koltuk(models.Model):
    sefer = models.ForeignKey(Sefer, on_delete=models.CASCADE, related_name='koltuklar')
    koltuk_no = models.CharField(max_length=10)
    koltuk_tipi = models.CharField(max_length=50)  # Örn: Tekli Cam Kenarı
    bilet_fiyati = models.DecimalField(max_digits=6, decimal_places=2)
    koltuk_durumu = models.BooleanField(default=True)  # True: Boş, False: Dolu

    def __str__(self):
        return f"{self.sefer.kalkis_yeri} -> {self.sefer.varis_yeri} | Koltuk: {self.koltuk_no}"

class Rezervasyon(models.Model):
    DURUM_SECENEKLERI = [
        ('beklemede', 'Sepette Bekliyor (Kilitli)'),
        ('onaylandi', 'Satın Alındı'),
        ('iptal', 'İptal Edildi / Süresi Doldu')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rezervasyonlar', null=True, blank=True)
    koltuk = models.ForeignKey(Koltuk, on_delete=models.CASCADE, related_name='rezervasyonlar')
    rezervasyon_durumu = models.CharField(max_length=20, choices=DURUM_SECENEKLERI, default='beklemede')
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.koltuk.koltuk_no} Numaralı Koltuk - {self.get_rezervasyon_durumu_display()}"