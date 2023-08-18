import requests
from bs4 import BeautifulSoup
import lxml
import smtplib

MY_EMAIL = "big_bob_roof@mail.ru"
APP_PASSWORD = "some password"
MAIL_SMTP = "smtp.mail.ru"

url = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
response = requests.get(url=url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "ru-RU,ru;q=0.6"})
response.raise_for_status()
amz_webpage = response.text

soup = BeautifulSoup(amz_webpage, "lxml")
price_raw = soup.find(name="span", class_="a-offscreen").getText().lstrip("$")
price_final = float(price_raw)
product_title = soup.find(name="span", id="productTitle").getText().encode('utf-8').strip()

if price_final < 100:
    with smtplib.SMTP(MAIL_SMTP) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=APP_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs="shaken.bolatuly@fizmat.kz",
                            msg=f"Subject:Amazon Price Alert!\n\n{product_title} is now {product_title}\n {url}")
        print("Email sent")