import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os

env_accept_language = os.environ['ENV_Accept_Language']
env_user_agent = os.environ['ENV_User_Agent']

url = "https://www.amazon.com/JBL-T750BTNC-Wireless-Headphones-Cancellation/dp/B0818P1Q7L/ref=sr_1_11?dchild=1&keywords=headphones&qid=1631520559&sr=8-11"
headers_ = {
    "User-Agent": env_user_agent
    , "Accept-Language": env_accept_language
}

r = requests.get(url, headers=headers_)
soup = BeautifulSoup(r.text, "lxml")
# print(soup.prettify())

min_price = 79.95 #lowest price come from camelcamelcamel.com
price = soup.find(id="priceblock_ourprice", class_="a-size-medium a-color-price priceBlockBuyingPriceString")
current_price = price.getText()[1:]
product_name = soup.find(id="productTitle").getText().strip()


#Mail set_up

server = smtplib.SMTP('smtp.gmail.com.')
server.starttls()
username = os.environ['ENV_MAIL_F']
password = os.environ['ENV_PW']
to_email = os.environ['ENV_MAIL_T']

subject = 'LOWEST PRICE FROM AMAZON'
content = f'The product {product_name} at ${current_price} compare to lowest price ${min_price}. Buy Now!!!'

if float(current_price) <= min_price:
    body = content
    server.login(user=username, password=password)
    server.sendmail(from_addr=username
                    , to_addrs=to_email
                    , msg=f'Subject: {subject}\n\n {body} \nLink here: {url} ')



print('Process Done')
