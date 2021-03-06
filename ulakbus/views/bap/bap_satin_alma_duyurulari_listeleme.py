# -*-  coding: utf-8 -*-
# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
""" BAP Satın Alma Duyuruları Listeleme Modülü

 Bu modül Ulakbüs uygulaması için duyuruda olan bap satın alma duyurularının listelenmesi ve
 duyuruya ait detay bilgilerinin görüntülenmesi işlemlerini içerir.

"""
from zengine.views.crud import CrudView, obj_filter, list_query
from zengine.forms import JsonForm, fields
from zengine.lib.translation import gettext as _, gettext_lazy as __
from ulakbus.lib.common import get_file_url
from ulakbus.models import BAPButcePlani, BAPSatinAlma
from datetime import datetime


class BAPSatinAlmaDuyurulariListeleme(CrudView):
    class Meta:
        model = 'BAPSatinAlma'

    def object_id_kontrol(self):
        self.current.task_data['object_id'] = self.input.get('object_id', None)

    def satin_alma_duyurulari_list(self):
        """
        Koordinasyon birimi görevlisinin kendi üstünde bulunan duyuruda olan satın
        alma duyuruları listelenir.

        """
        self.current.output["meta"]["allow_search"] = False
        self.current.output["meta"]["allow_actions"] = True
        self.output['object_title'] = _(u"Satın Alma Duyuru Listesi")
        self.output['objects'] = [
            [_(u'Konu'), _(u'Yetkili'), _(u"Son Teklif")]
        ]
        form = JsonForm(title=__(u"Satın Alma Duyurularının Listesi"))
        objs = BAPSatinAlma.objects.filter(teklife_kapanma_tarihi__gt=datetime.today(),
                                           duyuruda=True).order_by('teklife_acilma_tarihi')
        for o in objs:
            self.output['objects'].append({
                "fields": [o.ad,
                           "%s %s" % (o.sorumlu.user.personel.ad, o.sorumlu.user.personel.soyad),
                           o.teklife_kapanma_tarihi.strftime("%d.%m.%Y")],
                "actions": [{'name': _(u'Detay'), 'cmd': 'detay', 'show_as': 'button'}],
                "key": o.key
            })
        self.form_out(form)

    def duyuru_detay_goruntule(self):
        """
        Seçili olan satın alma duyurusuna ait bütçe kalemi bilgileri listelenir. Şartname dosyası
        bulunan kalemlere indir butonu eklenir.

        """
        self.current.task_data['object_id'] = self.input.get('object_id', None)
        form = JsonForm(current=self.current, title=_(u'%s Satın Alma Duyurusu Bütçe Kalemleri'
                                                      % self.object.ad))
        form.geri = fields.Button(__(u"Geri Dön"), cmd='geri_don')
        self.current.output["meta"]["allow_actions"] = True
        self.output['objects'] = [
            [_(u'Ad'), _(u'Adet'), _(u'Birim'), _(u'Şartname')]]
        for kalem in self.object.ButceKalemleri:
            actions = [{'object_key': 'data_key'}]
            if kalem.butce.teknik_sartname.sartname_dosyasi:
                actions[0].update({'name': _(u'İndir'), 'cmd': 'indir', 'show_as': 'button'})
            list_item = {
                "fields": [kalem.butce.ad, str(kalem.butce.adet), "Adet",
                           kalem.butce.teknik_sartname.aciklama],
                "actions": actions,
                'key': kalem.butce.key}
            self.output['objects'].append(list_item)
        self.form_out(form)

    def belge_indir(self):
        """
        Teknik şartname dosyasını indirme işlemini gerçekleştirir.

        """
        bap_butce = BAPButcePlani.objects.get(self.input['data_key'])
        self.set_client_cmd('download')
        self.current.output['download_url'] = get_file_url(
            bap_butce.teknik_sartname.sartname_dosyasi)

    @obj_filter
    def satin_alma_duyurulari_actions(self, obj, result):
        """
        Duyuru bilgilerinin yanına detay butonu eklenir.

        """
        result['actions'] = [
            {'name': "Detay", 'cmd': "detay", "mode": "normal", "show_as": "button"}]

    @list_query
    def satin_alma_duyurularini_listele(self, queryset):
        """
        Sorumluya gösterilecek duyuruda olan satın alma duyuruları listelenir.

        """
        return queryset.filter(teklife_kapanma_tarihi__gt=datetime.today(),
                               duyuruda=True).order_by('teklife_acilma_tarihi')
