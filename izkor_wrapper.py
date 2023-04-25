import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# This is the wrapper for the izkor website.

class izkor_wrapper:
    izkor_url = 'https://izkorcdn.azureedge.net/'

    @classmethod
    def get_halalim_by_name(instance, first_name='', last_name='', father='', mother='', year_of_fall='', beit_kvarot = ''):
        url = 'https://izkorcdn.azureedge.net/Search.aspx'
        data = {
        'ctl00$ctl00$MainContent$MainContent$TextBoxLastname': last_name,
        'ctl00$ctl00$MainContent$MainContent$TextBoxQuick': first_name,
        'ctl00$ctl00$MainContent$MainContent$TextBoxFather': father,
        'ctl00$ctl00$MainContent$MainContent$TextBoxMother': mother,
        'ctl00$ctl00$MainContent$MainContent$RadTxtBxLessMore': 'same',
        'ctl00_ctl00_MainContent_MainContent_RadCmbBxBateyKvarot_ClientState': '',
        'ctl00$ctl00$MainContent$MainContent$ButtonSearch': 'איתור שם נופל',
        'ctl00$ctl00$MainContent$MainContent$RadTxtBxYearEnd': 22000101 if year_of_fall == '' else year_of_fall,
        'ctl00$ctl00$MainContent$MainContent$RadTxtBxYearStart': 18000101 if year_of_fall == '' else year_of_fall,
        'ctl00$ctl00$MainContent$MainContent$RadTxtBxYear' : year_of_fall,
        'ctl00$ctl00$MainContent$MainContent$RadCmbBxBateyKvarot' : beit_kvarot,
        'ctl00_ctl00_MainContent_MainContent_RadScriptManager1_TSM': ';;System.Web.Extensions, Version=3.5.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:16997a38-7253-4f67-80d9-0cbcc01b3057:ea597d4b:b25378d2;Telerik.Web.UI, Version=2011.3.1115.35, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:d841c84c-68bb-4f5c-b77b-50f39a462ac8:16e4e7cd:f7645509:ed16cbdc:24ee1bba:f46195d3:5f39f986:1e771326:aa288e2d:58366029:4cacbc31;AjaxControlToolkit, Version=3.0.30512.17815, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:c6756652-1352-4664-9356-b246b450e2d0:b14bb7d5:dc2d6e36:5acd2e8e:13f47f54:4cda6429',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': '',
        '__VIEWSTATEGENERATOR': '',
        }   
        response = requests.post(url, data=data)
        # with open('res.html', 'wb') as f:
        #     f.write(response.content)
        soup = BeautifulSoup(response.text, 'html.parser')
        halalim_elems = filter(lambda x: 'id' in x.attrs and 'ctl00_ctl00_MainContent_MainContent_RadGridResult_ctl00__' == x.attrs['id'][:-1] , soup.find_all('tr'))
        halalim = []
        
        for x in halalim_elems:
            beit_kvarot = instance.clean_string( x.contents[1].string )
            cheil = instance.clean_string( x.contents[2].string )
            year_of_fall = instance.clean_string( x.contents[3].string )
            parents = x.contents[4].string.split(' ו')
            father = instance.clean_string( parents[1] )
            mother = instance.clean_string( parents[0] )
            first_name = instance.clean_string( x.contents[5].string )
            last_name = instance.clean_string( x.contents[6].string )
            id = instance.clean_string( x.contents[6].find('a').attrs['href'].split('id=')[1] )
            halalim.append(halal_light(id, first_name, last_name, father, mother, year_of_fall, beit_kvarot, cheil))
        return halalim

    def get_halal_by_id(instance, id):
        about_halal_url = instance.izkor_url + 'HalalKorot.aspx?id=' + id
        halal_page_url = instance.izkor_url + 'HalalView.aspx?id=' + id
        

    @classmethod
    def clean_string(instance, text):
        text_parts = text.replace('\n', '').replace('\r', '').split(' ')
        final = []
        for part in text_parts:
            if part != '':
                final.append(part)
        return ' '.join(final)


class halal_light:
    def __init__(self, id, first_name, last_name, father, mother, year_of_fall, beit_kvarot, cheil):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.father = father
        self.mother = mother
        self.year_of_fall = year_of_fall
        self.beit_kvarot = beit_kvarot
        self.cheil = cheil

    def __str__(self):
        return f'{self.id} {self.first_name} {self.last_name} {self.father} {self.mother} {self.year_of_fall} {self.beit_kvarot} {self.cheil}'
    
    def get_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
    
    def get_dict(self):
        return self.__dict__

class halal(halal_light):
    def __init__(self, id, first_name, last_name, father, mother, year_of_fall, beit_kvarot, cheil, about):