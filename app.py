import requests
from bs4 import BeautifulSoup

base_url = "https://www.amazon.in/s"
search_query = "bags"
num_pages = 20  # Number of pages to scrape

product_info = []

def extract_product_info(product_url):
    response = requests.get(product_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        
        product_description_element = soup.find("div", {"id": "productDescription"})
        if product_description_element:
            product_description = product_description_element.get_text(strip=True)
        else:
            product_description = "Description not available"
        
        asin_element = soup.find("th", string="ASIN")
        if asin_element:
            asin = asin_element.find_next("td").text.strip()
        else:
            asin = "ASIN not available"
        
        product_details_element = soup.find("div", {"id": "productDetails_feature_div"})
        if product_details_element:
            product_description = product_details_element.get_text(strip=True)
        
        manufacturer_element = soup.find("a", {"id": "bylineInfo"})
        if manufacturer_element:
            manufacturer = manufacturer_element.get_text(strip=True)
        else:
            manufacturer = "Manufacturer not available"
        
        return {
            "Product Description": product_description,
            "ASIN": asin,
            "Product Details": product_details,
            "Manufacturer": manufacturer
        }
    else:
        return None

for page in range(1, num_pages + 1):
    params = {
        "k": search_query,
        "crid": "2M096C61O4MLT",
        "qid": 1653308124,
        "sprefix": "ba%2Caps%2C283",
        "ref": f"sr_pg_{page}",
        "page": page
    }

    response = requests.get(base_url, params=params)
    try:
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            product_list = soup.find_all("div", class_="sg-col-inner")

            for product in product_list:
                product_url_element = product.find("a", class_="a-link-normal")
                if product_url_element:
                    product_url = product_url_element.get("href")
                    product_data = extract_product_info(product_url)
                    product_info.append(product_data)
                else:
                    product_url = "URL not available"

                product_name_element = soup.find("span", class_="a-size-medium")
                if product_name_element:
                    product_name = product_name_element.text.strip()
                else:
                    product_name = "Product name not available"

                # Find the product price
                product_price_element = soup.find("span", class_="a-price-whole")
                if product_price_element:
                    product_price = product_price_element.text.strip()
                else:
                    product_price = "Product price not available"

                rating_element = product.find("span", class_="a-icon-alt")
                if rating_element:
                    rating = rating_element.text.split()[0]
                else:
                    rating = "No rating"

                num_reviews_element = product.find("span", class_="a-size-base")
                if num_reviews_element:
                    num_reviews: str = num_reviews_element.text.replace(",", "")
                    
                    if not num_reviews.isdigit():
                        num_reviews = "No reviews"
                else:
                    num_reviews = "No reviews"

                # print("Product Name:", product_name)
                # print("Product URL:", product_url)
                # print("Product Price:", product_price)
                # print("Rating:", rating)
                # print("Number of Reviews:", num_reviews)
                # print("-" * 50)

        else:
            print(f"Failed to retrieve page {page}")

    except Exception as e:
        print(e)


csv_filename = "amazon_product_data.csv"

# Write the data to a CSV file
try:
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["Product URL", "Product Description", "ASIN", "Manufacturer"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()
        
        # Write the data rows
        for row in data:
            writer.writerow(row)

    print(f"Data has been exported to {csv_filename}")
except Exception as e:
    print(e)