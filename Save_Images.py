import requests
from bs4 import BeautifulSoup
import urllib
import os
from re import sub, search

class AlmacenarImagen(object):
    
    def __init__(self):
        
        '''
        Crea la instancia para hacer web scrapping para algunas imagenes de
        League of Legends.
        '''
        
    def Campeon(self):
        
        '''
        return:
            Las imagenes de los campeones en League of Legends.
        '''

        URL = 'https://lan.leagueoflegends.com/es-mx/champions/'
        
        page = requests.get(URL)
        
        soup = BeautifulSoup(page.content, 'html.parser')
        
        results = soup.find(id='___gatsby')
        
        find_div_imgs = results.find('div', class_='style__List-ntddd-2 fqjuPM')
        
        find_a_imgs = find_div_imgs.findAll('a')
        
        dir = './imagenes_campeones/'

        if not os.path.exists(dir):
            os.mkdir(dir)
        
        for find_div_img in find_div_imgs:
            image_text = find_div_img.text
            if search("\W", image_text):
                sub(r'(.*)\W(.*)',r'\1\2',image_text)
            image_url = find_div_img.find('img')['src']
            print('Almacenando la imagen de: {}'.format(image_text))
            urllib.request.urlretrieve(
                image_url, os.path.join('imagenes_campeones', 
                                        image_text + '.png'))
            