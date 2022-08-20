from importlib.metadata import files
from importlib.resources import path
from os import remove
from playwright.sync_api import sync_playwright
import pathlib

def get_food_menu():
    #Remover daqui depois...
    remove_files('pdf')
    remove_files('xlsx')

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://www.propaae.uefs.br/modules/conteudo/conteudo.php?conteudo=15")
        
        with page.expect_download() as download_info: 
            page.click("img[alt='Cardápio']")

        download = download_info.value
        if(download.url.find('.xlsx') >= 0):
            download.save_as("./input_files/xlsx/"+download.url[51:])
        elif (download.url.find('.pdf') >= 0):
            download.save_as("./input_files/pdf/"+download.url[51:])
            pdf_to_excel()
        
        

def pdf_to_excel():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.ilovepdf.com/pdf_to_excel")

        with page.expect_file_chooser() as fc_info:
            page.click("a[id='pickfiles']")
            
        file_chooser = fc_info.value
        file_chooser.set_files("./input_files/pdf/" + get_pdf_name())  
        page.click("button[id='processTask']")

        with page.expect_download() as download_info:
           
            page.click("a[id='pickfiles']")

        download = download_info.value
        
        download.save_as("./input_files/xlsx/cardapio.xlsx")

def get_pdf_name():
    files = pathlib.Path('./').glob('./input_files/pdf/*.pdf')
    file = files.__next__()
    return file.name

def remove_files(extension):
    files = pathlib.Path('./').glob(f'**/*.{extension}')
    for file in files:
        file.unlink()
       
pdf_to_excel()