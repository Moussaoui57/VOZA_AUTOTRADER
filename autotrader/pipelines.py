# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy import signals
from csv import QUOTE_ALL
from scrapy.mail import MailSender
import datetime
from scrapy.utils.project import get_project_settings
import socket
import logging
from twisted.python.failure import Failure
from scrapy.utils.request import referer_str
import time
import pprint
from scrapy.exporters import CsvItemExporter
from csv import QUOTE_ALL

class AutotraderPipeline(object):
    def __init__(self):
        self.files = {}


    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):

        mailer = MailSender(mailfrom="h.moussaoui@autobiz.com")
        settings = get_project_settings()
        hostname = socket.gethostname()
        body='''-Crawl name: {0}\n-Cache directory: {1}\n-Hostname : {2} \n -Crawler_name: Missaoui hassib'''.format(settings.get('BOT_NAME'),settings.get('HTTPCACHE_DIR'),hostname,
        )
        mailer.send(to=["h.moussaoui@autobiz.com","a.bouyahya@autobiz.com","m.jami@autobiz.com","k.abidi@autobiz.com"], subject="The crawl of %s is %s " % (spider.name, "launched"), body=body )
        #mailer.send(to=["h.moussaoui@autobiz.com","a.bouyahya@autobiz.com"], subject="The crawl of %s is %s " % (spider.name, "launched"), body=body )


        file = open('%s.csv' % spider.name, 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file, delimiter=';', quotechar='"', quoting=QUOTE_ALL)
        self.exporter.start_exporting()
        self.exporter.fields_to_export = ["ANNONCE_LINK", "ANNONCE_DATE","ID_CLIENT", "GARAGE_ID",  "TYPE", "SITE", "MARQUE",   "MODELE",   "ANNEE",    "MOIS", "NOM",  "CARROSSERIE",  "OPTIONS",  "CARBURANT",    "CYLINDRE", "PUISSANCE",    "PORTE",    "BOITE",    "NB_VITESSE",   "PRIX", "KM",   "PLACE",    "COULEUR",  "PHOTO",    "LITRE",    "IMMAT",    "VN_IND",   "CONTACT",  "CONTACT_PRENOM",   "CONTACT_NOM",  "GARAGE_NAME",  "ADRESSE",  "VILLE",    "CP",   "DEPARTEMENT",  "PROVINCE", "COUNTRY",  "TELEPHONE",    "TELEPHONE_2",  "TELEPHONE_3",  "TELEPHONE_4",  "TELEFAX",  "EMAIL"]
    def spider_closed(self, spider,reason):
        mailer = MailSender()
        pige = 100000
        intro = "Summary stats from Scrapy spider: \n\n"
        stats = spider.crawler.stats.get_stats()
        comptage = stats.get('item_scraped_count')
        pourcentage = comptage * 100 /pige
        body = pprint.pformat(stats)
        body = spider.name+" is " + reason +"\n\n" +"Le comptage a atteint " + str(pourcentage) +"%\n" +intro 
        #mailer.send(to=["h.moussaoui@autobiz.com","a.bouyahya@autobiz.com","m.jami@autobiz.com","k.abidi@autobiz.com"], subject="The crawl of %s is %s " % (spider.name, reason), body=body )
        mailer.send(to=["h.moussaoui@autobiz.com","a.bouyahya@autobiz.com"],subject="The crawl of %s is %s " % (spider.name, reason), body=body )


        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()
    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
