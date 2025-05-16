# 📉 Amazon Price Tracker

This Python script tracks the price of a specific Amazon product and sends an email alert when the price drops below a target amount.

---

## 🛠 Files Included

1. `amazon_price_tracker.py` – The main Python script that performs web scraping and sends email alerts.  
2. `.env` – Stores sensitive data like your email credentials and SMTP server address securely.

---

## ⚙️ How It Works

### 1. Importing Libraries
```python
import smtplib
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
```

These libraries handle:
- HTTP requests (`requests`)
- HTML parsing (`BeautifulSoup`)
- Email sending (`smtplib`)
- Secure environment variable handling (`dotenv`)

---

### 2. Load Environment Variables
```python
load_dotenv()
```

This loads your credentials and configuration (e.g. email and SMTP server) from a `.env` file.

---

### 3. Set Product URL and Request Headers
```python
live_url = "https://www.amazon.in/..."
headers = {
  "User-Agent": "...",
  ...
}
```

We use a `User-Agent` header to avoid being blocked by Amazon (they block bots that don’t look like real browsers).

---

### 4. Scrape the Product Data
```python
response = requests.get(live_url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")
```

Makes an HTTP GET request and parses the returned HTML using BeautifulSoup.

---

### 5. Extract Product Price and Title
```python
price = soup.find(class_="a-price-whole").get_text()
    # We have to remove the comas from between the nos or else the less than operator will not work and it will give str error
price_clean = price.replace(',', '').strip()
price_as_float = float(price_clean)

title = soup.find(id="productTitle").get_text().strip()
```

- Extracts the price and removes formatting characters like commas    
- Converts the price to a float for comparison
- Gets the product name for use in the email

---

### 6. Compare Price and Send Alert
```python
      # Change the price to what u want to buy, so that u get notified when the price drops.
BUY_PRICE = 1000000
if price_as_float < BUY_PRICE:
    message = f"{title} is on sale for {price}!"
```

Sends an alert if the product's current price is less than the defined threshold (`BUY_PRICE`).

---

### 7. Send Email Notification
```python
with smtplib.SMTP(os.environ["SMTP_ADDRESS"], port=587) as connection:
    connection.starttls()
    result = connection.login(os.environ["EMAIL_ADDRESS"], os.environ["EMAIL_PASSWORD"])
    connection.sendmail(
        from_addr=os.environ["EMAIL_ADDRESS"],
        to_addrs=os.environ["EMAIL_ADDRESS"],
        msg=f"Subject:Amazon Price Alert!\n\n{message}\n{live_url}".encode("utf-8")
    )
```

This securely logs in to your email account and sends a notification to yourself.

---

## 🔐 Example `.env` File
```
EMAIL_ADDRESS=youremail@example.com
EMAIL_PASSWORD=yourpassword
SMTP_ADDRESS=smtp.gmail.com
```

Keep this file private and never commit it to version control (GitHub).

---

## ▶️ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/amazon-price-tracker.git
   cd amazon-price-tracker
   ```

2. Install dependencies:
   ```bash
   pip install requests beautifulsoup4 python-dotenv
   ```

3. Create a `.env` file in the root directory with your email config.

4. Run the script:
   ```bash
   python price_tracker.py
   ```

---

## 📧 Email Alert Example

You will receive an email like this:

```
Subject: Amazon Price Alert!

[Product Name] is on sale for ₹99,999!
https://www.amazon.in/your-product-link
```

---

## 🧠 Skills Demonstrated

- Web scraping with BeautifulSoup
- Working with environment variables for secure configuration
- Email automation with `smtplib`
- HTTP requests and browser header simulation
- Simple automation logic and alert systems

---

