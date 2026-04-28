import heapq
import collections

class MetroAgi:
    def __init__(self):
        """
        Metro ağı sınıfı. İstasyonları ve bağlantıları saklar.
        """
        self.istasyonlar = {}
    
    def istasyon_ekle(self, isim):
        """Yeni bir istasyon ekler."""
        if isim not in self.istasyonlar:
            self.istasyonlar[isim] = {}
    
    def baglanti_ekle(self, baslangic, bitis, sure):
        """İki istasyon arasında bağlantı ekler ve süreyi belirtir."""
        self.istasyon_ekle(baslangic)
        self.istasyon_ekle(bitis)
        self.istasyonlar[baslangic][bitis] = sure
        self.istasyonlar[bitis][baslangic] = sure
    
    def en_az_aktarma_bul(self, baslangic, hedef):
        """BFS algoritması ile en az aktarma içeren rotayı bulur."""
        kuyruk = collections.deque([(baslangic, [baslangic])])
        ziyaret_edilen = set()
        
        while kuyruk:
            mevcut, yol = kuyruk.popleft()
            if mevcut == hedef:
                return yol  # Hedefe ulaşıldığında yol döndürülür
            
            if mevcut not in ziyaret_edilen:
                ziyaret_edilen.add(mevcut)
                for komsu in self.istasyonlar[mevcut]:
                    if komsu not in ziyaret_edilen:
                        kuyruk.append((komsu, yol + [komsu]))
        return []  # Hedefe ulaşılamadıysa boş liste döndürülür
    
    def en_hizli_rota_bul(self, baslangic, hedef):
        """Dijkstra algoritması kullanarak en hızlı rotayı bulur."""
        if baslangic not in self.istasyonlar or hedef not in self.istasyonlar:
            print(f"Hata: '{baslangic}' veya '{hedef}' istasyonu bulunamadı.")
            return [], 0
        
        oncelik_kuyrugu = [(0, baslangic, [baslangic])]
        ziyaret_edilen = {}
        
        while oncelik_kuyrugu:
            sure, mevcut, yol = heapq.heappop(oncelik_kuyrugu)
            if mevcut == hedef:
                return yol, sure  # En kısa sürede hedefe ulaşan rota ve süre döndürülür
            
            if mevcut not in ziyaret_edilen or ziyaret_edilen[mevcut] > sure:
                ziyaret_edilen[mevcut] = sure
                for komsu, komsu_sure in self.istasyonlar[mevcut].items():
                    heapq.heappush(oncelik_kuyrugu, (sure + komsu_sure, komsu, yol + [komsu]))
        return [], 0  # Eğer hedefe ulaşılamadıysa boş liste ve 0 döndürülür

if __name__ == "__main__":
    # Metro ağı oluşturuluyor
    metro = MetroAgi()
    metro.baglanti_ekle("AŞTİ", "Kızılay", 5)
    metro.baglanti_ekle("Kızılay", "Ulus", 6)
    metro.baglanti_ekle("Ulus", "Demetevler", 8)
    metro.baglanti_ekle("Demetevler", "OSB", 4)
    metro.baglanti_ekle("Batıkent", "Demetevler", 5)
    metro.baglanti_ekle("Demetevler", "Gar", 6)
    metro.baglanti_ekle("Gar", "Keçiören", 7)  # Tekrarlı bağlantı kaldırıldı
    metro.baglanti_ekle("Gar", "Sıhhiye", 3)
    metro.baglanti_ekle("Sıhhiye", "Kızılay", 2)

    # Test senaryoları
    print("=== Test Senaryoları ===")

    print("\n1. AŞTİ'den OSB'ye:")
    en_az_aktarma = metro.en_az_aktarma_bul("AŞTİ", "OSB")
    en_hizli_rota, sure = metro.en_hizli_rota_bul("AŞTİ", "OSB")
    print(f"   En az aktarmalı rota: {' -> '.join(en_az_aktarma)}")
    print(f"   En hızlı rota ({sure} dakika): {' -> '.join(en_hizli_rota)}")

    print("\n2. Batıkent'ten Keçiören'e:")
    en_az_aktarma = metro.en_az_aktarma_bul("Batıkent", "Keçiören")
    en_hizli_rota, sure = metro.en_hizli_rota_bul("Batıkent", "Keçiören")
    print(f"   En az aktarmalı rota: {' -> '.join(en_az_aktarma)}")
    print(f"   En hızlı rota ({sure} dakika): {' -> '.join(en_hizli_rota)}")

    print("\n3. Keçiören'den AŞTİ'ye:")
    en_az_aktarma = metro.en_az_aktarma_bul("Keçiören", "AŞTİ")
    en_hizli_rota, sure = metro.en_hizli_rota_bul("Keçiören", "AŞTİ")
    print(f"   En az aktarmalı rota: {' -> '.join(en_az_aktarma)}")
    print(f"   En hızlı rota ({sure} dakika): {' -> '.join(en_hizli_rota)}")
