# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.

"""HITAP Açık Süre Ekle

Hitap'a personelin açık süre bilgilerinin eklenmesini yapar.

"""

__author__ = 'H.İbrahim Yılmaz (drlinux)'

from ulakbus.services.personel.hitap.hitap_ekle import HITAPEkle

class HizmetAcikSureEkle(HITAPEkle):
    """
    HITAP Ekleme servisinden kalıtılmış Hizmet Açık Süre Bilgisi Ekleme servisi

    """

    def handle(self):
        """Servis çağrıldığında tetiklenen metod.

        Attributes:
            service_name (str): İlgili Hitap sorgu servisinin adı
            service_dict (dict): ''HizmetAcikSure'' modelinden gelen kayıtların alanları,
                    HizmetAcikSureInsert servisinin alanlarıyla eşlenmektedir.
                    Filtreden geçecek tarih alanları listede tutulmaktadır.
        """
        self.service_name = 'HizmetAcikSureInsert'

        self.service_dict = {
            'fields': {
                'tckn': self.request.payload['tckn'],
                'acikSekil': self.request.payload['acik_sekil'],
                'iadeSekil': self.request.payload['iade_sekil'],
                'hizmetDurum': self.request.payload['hizmet_durum'],
                'husus': self.request.payload['husus'],
                'acigaAlinmaTarih': self.request.payload['aciga_alinma_tarih'],
                'goreveSonTarih': self.request.payload['goreve_son_tarih'],
                'goreveIadeIstemTarih': self.request.payload['goreve_iade_istem_tarih'],
                'goreveIadeTarih': self.request.payload['goreve_iade_tarih'],
                'acikAylikBasTarihi': self.request.payload['acik_aylik_bas_tarih'],
                'acikAylikBitTarihi': self.request.payload['acik_aylik_bit_tarih'],
                'gorevSonAylikBasTarihi': self.request.payload['goreve_son_aylik_bas_tarih'],
                'gorevSonAylikBitTarihi': self.request.payload['goreve_son_aylik_bit_tarih'],
                'SYonetimKaldTarih': self.request.payload['s_yonetim_kald_tarih'],
                'aciktanAtanmaTarih': self.request.payload['aciktan_atanma_tarih'],
                'kurumOnayTarihi': self.request.payload['kurum_onay_tarihi']
            },
            'date_filter': ['acigaAlinmaTarih', 'goreveSonTarih', 'goreveIadeIstemTarih',
                            'goreveIadeTarih', 'acikAylikBasTarihi', 'acikAylikBitTarihi',
                            'gorevSonAylikBasTarihi', 'gorevSonAylikBitTarihi', 'SYonetimKaldTarih',
                            'aciktanAtanmaTarih', 'kurumOnayTarihi'],
            'required_fields': ['tckn','acikSekil','durum','hizmetDurum','husus','kurumOnayTarihi']
        }
        super(HizmetAcikSureEkle, self).handle()
