import redis
from django.db import transaction
from django.http import JsonResponse
from .models import Koltuk, Rezervasyon

# Redis bağlantısını kuruyoruz
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def koltuk_rezerve_et(request, koltuk_id):
    kilit_anahtari = f"koltuk_kilit_{koltuk_id}"

    # 1. ADIM: Redis Kontrolü (Veritabanını yormadan kapıdan çeviriyoruz)
    # Eğer bu koltuk için aktif bir kilit varsa işlem yapma.
    if redis_client.exists(kilit_anahtari):
        kalan_sure = redis_client.ttl(kilit_anahtari)
        dakika = kalan_sure // 60
        saniye = kalan_sure % 60
        return JsonResponse({'hata': f'Koltuk şu an başka birinin sepetinde. Lütfen {dakika} dakika {saniye} saniye sonra tekrar deneyin.'}, status=400)

    # 2. ADIM: Veritabanı Kilidi (Pessimistic Lock)
    with transaction.atomic():
        try:
            koltuk = Koltuk.objects.select_for_update().get(id=koltuk_id)

            # Koltuk tamamen satın alınmış mı?
            if not koltuk.koltuk_durumu:
                return JsonResponse({'hata': 'Bu koltuk zaten satılmış.'}, status=400)

            # Satılmamış ve sepet kilidi de yok. O zaman 10 dakikalık kilidi biz atıyoruz.
            # setex: Set with Expiration (Anahtar, Saniye Cinsinden Süre, Değer)
            redis_client.setex(kilit_anahtari, 600, "kilitli")

            # Veritabanında koltuk_durumu'nu bilerek False YAPMIYORUZ.
            # Sadece rezervasyon (sepet) kaydını oluşturuyoruz.
            Rezervasyon.objects.create(
                koltuk=koltuk,
                rezervasyon_durumu='beklemede'
            )

            return JsonResponse({'basari': f'{koltuk.koltuk_no} numaralı koltuk 10 dakikalığına size rezerve edildi!'})

        except Koltuk.DoesNotExist:
            return JsonResponse({'hata': 'Böyle bir koltuk bulunamadı.'}, status=404)
        
        
def satin_al(request, koltuk_id):
    kilit_anahtari = f"koltuk_kilit_{koltuk_id}"

    with transaction.atomic():
        try:
            # Yine pessimistic lock atıyoruz ki biz güncellerken başkası araya girmesin
            koltuk = Koltuk.objects.select_for_update().get(id=koltuk_id)

            # Eğer koltuk zaten daha önceden satılmışsa (durumu False ise) işlemi iptal et
            if not koltuk.koltuk_durumu:
                return JsonResponse({'hata': 'Bu koltuk zaten satın alınmış.'}, status=400)

            # Sepette bekleyen rezervasyon kaydını bul
            rezervasyon = Rezervasyon.objects.filter(koltuk=koltuk, rezervasyon_durumu='beklemede').first()

            if not rezervasyon:
                return JsonResponse({'hata': 'Aktif bir sepet kaydı bulunamadı. 10 dakikalık süreniz dolmuş olabilir.'}, status=400)

            # 1. Adım: Koltuğu kalıcı olarak doluya çek
            koltuk.koltuk_durumu = False
            koltuk.save()

            # 2. Adım: Rezervasyonun durumunu 'onaylandi' yap
            rezervasyon.rezervasyon_durumu = 'onaylandi'
            rezervasyon.save()

            # 3. Adım: Redis'teki geçici kilidi sil
            redis_client.delete(kilit_anahtari)

            return JsonResponse({'basari': f'{koltuk.koltuk_no} numaralı koltuğun ödemesi alındı ve biletiniz başarıyla kesildi!'})

        except Koltuk.DoesNotExist:
            return JsonResponse({'hata': 'Böyle bir koltuk bulunamadı.'}, status=404)