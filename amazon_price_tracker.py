import smtplib
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

practice_url = "https://appbrewery.github.io/instant_pot/"
live_url = "https://www.amazon.in/Hero-Xpulse-Booking-Ex-Showroom-Polestar/dp/B0D9DLZ2DJ/?_encoding=UTF8&pd_rd_w=yRgfw&content-id=amzn1.sym.5e88c7b1-d6dd-463e-95f7-24271869827e&pf_rd_p=5e88c7b1-d6dd-463e-95f7-24271869827e&pf_rd_r=Y2V838QG7T8DFWBKQNGZ&pd_rd_wg=ruT2c&pd_rd_r=94aaa749-8cd6-4ba1-bc48-07041340c773&ref_=pd_hp_d_btf_ls_gwc_pc_en4_"


header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Dnt": "1",
    "Priority": "u=0, i",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 OPR/118.0.0.0",
}


response = requests.get(live_url, headers= header)

soup = BeautifulSoup(response.content, "html.parser")
# print(soup.prettify())

# # Find the HTML element that contains the price
# price = soup.find(class_="a-price-whole").get_text()
#
# # Remove the dollar sign using split
# # price_without_currency = price.split("$")[1]
#
# # Convert to floating point number
# price_as_float = float(price)
# print(price_as_float)


price = soup.find(class_="a-price-whole").get_text()

# Remove commas or other non-numeric characters (except the dot)
price_clean = price.replace(',', '').strip()

# Convert to float
price_as_float = float(price_clean)
print(price_as_float)
# except ValueError:
#     print("Could not convert price to float:", price_clean)


# Get the product title
title = soup.find(id="productTitle").get_text().strip()
print(title)

# Set the price below which you would like to get a notification
BUY_PRICE = 1000000


if price_as_float < BUY_PRICE:
    message = f"{title} is on sale for {price}!"

    # ======================  SENDS EMAIL  ===========================

    with smtplib.SMTP(os.environ["SMTP_ADDRESS"], port=587) as connection:
        connection.starttls()
        result = connection.login(os.environ["EMAIL_ADDRESS"], os.environ["EMAIL_PASSWORD"])
        connection.sendmail(
            from_addr=os.environ["EMAIL_ADDRESS"],
            to_addrs=os.environ["EMAIL_ADDRESS"],
            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{live_url}".encode("utf-8")
        )

