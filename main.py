import os
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime


def check_numbers(number1, number2, city_list, dir_name):
    driver = webdriver.Chrome('driver/chromedriver')
    driver.get("https://web.whatsapp.com")
    print("QR kodu taratıp Enter'a basın")
    input()
    print("Giris Yapildi")
    for number in range(int(number1), int(number2)):
        try:
            driver.get(f'https://web.whatsapp.com/send?phone={number}&text&app_absent=0')
            time.sleep(7)
            invalid_number_message_element = driver.find_elements(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')
            if len(invalid_number_message_element) > 0:
                print(f'Gecersiz Numara: {number}')
            else:
                see_details_element = driver.find_elements(By.XPATH, '//*[@id="main"]/header/div[2]/div/div/span')
                if len(see_details_element) > 0:
                    see_details_element[0].click()
                    time.sleep(2)
                    is_business_account = driver.find_elements(By.XPATH, '//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[1]/div[3]/div[2]')
                    if len(is_business_account) > 0:
                        address = driver.find_elements(By.XPATH, '//*[@id="app"]/div/div/div[2]/div[3]/span/div/span/div/div/section/div[3]/div[3]/span')
                        if address:
                            address = address[0].text.lower()
                            for city in city_list:
                                x = re.findall(city[:-1], address)
                                if len(x) > 0:
                                    with open(dir_name + '/' + city[:-1] + '.txt', 'a') as c:
                                        c.write(str(number) + '\n')
                                        print(f'Business Hesap: {number} | Sehir: {city}'),
                                    continue
                        else:
                            print(f'Business Hesap: {number} | Sehir bilgisi bulunamadi'),
                    else:
                        print(f'Normal Hesap: {number}')
        except:
            print(f'Hata: {number}')


if __name__ == '__main__':
    dir_name = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    os.mkdir(dir_name)
    sehirler_filename = 'sehirler.txt'
    numaralar_filename = 'numaralar.txt'
    with open(sehirler_filename) as f:
        city_list = f.readlines()
    with open(numaralar_filename) as f:
        numbers_between = f.readlines()
        if numbers_between:
            number1 = numbers_between[0].split('-')[0]
            number2 = numbers_between[0].split('-')[1]
            city_list = [city.lower() for city in city_list]
            check_numbers(number1, number2, city_list, dir_name)
