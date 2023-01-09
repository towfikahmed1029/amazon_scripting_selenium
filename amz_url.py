import mysql.connector 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from pyvirtualdisplay import Display
import time
import sys
from selenium.webdriver.chrome.options import Options
product_input =input("Please Any Product name: ")
catgry =input("Please Any catgry name: ")
minimum_review_input = 10000
# minimum_review_input = input("Please input minimum review: ")
minimum_review =int(minimum_review_input)
# if sys.platform not in ['Windows', 'win32', 'cygwin']:
#     display = Display(visible=0, size=(1024, 768))
#     display.start()
if sys.platform in ['Windows', 'win32', 'cygwin']:
    driverUrl = 'chromedriver.exe'
else:
    driverUrl = '/usr/bin/chromedriver'
def get_formated_data(headers, data):
        try:
            data = dict(zip([c[0] for c in headers], data))
        except:
            data = None
        return data
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(driverUrl,chrome_options=chrome_options)
driver.get('https://www.amazon.com/s?k={0}&i={1}'.format(product_input,catgry))
time.sleep(5)
# try:
#     search= driver.find_element(By.XPATH, '//input[@id="twotabsearchtextbox"]')
#     search.send_keys(product_input)
#     search_f= driver.find_element(By.XPATH, '//input[@id="nav-search-submit-button"]')
#     search_f.click()
# except:
#     search= driver.find_element(By.XPATH, '//input[@id="nav-bb-search"]')
#     search.send_keys(product_input)
#     search_f= driver.find_element(By.XPATH, '//input[@type="submit"]')
#     search_f.click()

# time.sleep(5)
# os.environ['PS_KEY']
# if sys.platform in ['Windows', 'win32', 'cygwin']:
#     mydb = mysql.connector.connect(
#     host = "database-1.criq1nathhcp.us-west-2.rds.amazonaws.com",
#     user = "admin",
#     password = "5HjTd1Fr7e3DS",
#     database = "affiliate",
#     port=33360
#     )
# else:
#     mydb = mysql.connector.connect(
#     host = os.environ['DB_HOST'],
#     user = os.environ['DB_USER'],
#     password = os.environ['DB_PASS'],
#     database = os.environ['DB_NAME'],
#     port=os.environ['DB_PORT']
    
#     )
mydb = mysql.connector.connect(
   host = "database-1.criq1nathhcp.us-west-2.rds.amazonaws.com",
   user = "admin",
   password = "5HjTd1Fr7e3DS",
   database = "affiliate",
   port= 33360
   )
 
try:
    typea = driver.find_element(By.XPATH, '(//span[@class="a-size-base puis-light-weight-text s-link-centralized-style"])')
    typex = 1
except:
    typeb = driver.find_element(By.XPATH, '(//span[@class="a-size-base s-underline-text"])')
    typex = 0
print(typex)

if typex == 1:
    while True:
        typea = driver.find_element(By.XPATH, '(//span[@class="a-size-base puis-light-weight-text s-link-centralized-style"])')
        count_product = len(driver.find_elements(By.XPATH, '//span[@class="a-size-base puis-light-weight-text s-link-centralized-style"]'))
        print("Total product in this page---",count_product)
        product_amazon = 1
        for x in range(0,count_product):
            review=driver.find_element(By.XPATH, '(//span[@class="a-size-base puis-light-weight-text s-link-centralized-style"])[{0}]'.format(product_amazon)).text
            review_int=review.replace(",", "")
            review_int_f_f=int(review_int)
            review_int_f= review_int_f_f - 5
            if review_int_f > minimum_review:
                review_int_sql = review_int_f
                url_full = driver.find_element(By.XPATH, '(//span[@class="a-size-base puis-light-weight-text s-link-centralized-style"]//parent::a)[{0}]'.format(product_amazon)).get_attribute("href")
                url = url_full.split("?")[0]
                status = 0
                mycursor = mydb.cursor()
                mycursor.execute("SELECT * FROM product_url WHERE url = '{0}'".format(url))
                myresult = mycursor.fetchone()
                if myresult == None:
                    id= mycursor.lastrowid
                    sqlproduct_url=("Insert into product_url(id,url,status,review) values(%s,%s,%s,%s)")
                    sqlproduct_url_value=[id,url,status,review_int_sql]
                    mycursor.execute(sqlproduct_url,sqlproduct_url_value)
                    mydb.commit()
                    print("success---",review_int_sql, url) 
                else:
                    print("You have already this Url.") 
                product_amazon += 1
            else:
                print("sorry")
                product_amazon += 1

        try:
            next_text = driver.find_element(By.XPATH, "(//a[text()='Next'])").text
        except:
            next_text = 0
            
        if next_text == "Next":
            next = driver.find_element(By.XPATH, "(//a[text()='Next'])")
            driver.get(next.get_attribute('href'))
            print("top Collecting Next Page Products.")
            time.sleep(5)
        else:
            print("top End Products Url collecting.")
            driver.close()
            break
        exit()
    
else:
    while True:
        typeb = driver.find_element(By.XPATH, '(//span[@class="a-size-base s-underline-text"])')
        count_product = len(driver.find_elements(By.XPATH, '//span[@class="a-size-base s-underline-text"]'))
        print("Bottom Total product in this page---",count_product)
        product_amazon = 1
        for x in range(0,count_product):
            review=driver.find_element(By.XPATH, '(//span[@class="a-size-base s-underline-text"])[{0}]'.format(product_amazon)).text
            review_int=review.replace(",", "")
            review_int_f=int(review_int)
            if review_int_f > minimum_review:
                review_int_sql = review_int_f
                url_full = driver.find_element(By.XPATH, '(//span[@class="a-size-base s-underline-text"]//parent::a)[{0}]'.format(product_amazon)).get_attribute("href")
                url = url_full.split("?")[0]                
                status = 0
                mycursor = mydb.cursor()
                mycursor.execute("SELECT * FROM product_url WHERE url = '{0}'".format(url))
                myresult = mycursor.fetchone()
                if myresult == None:
                    id= mycursor.lastrowid
                    sqlproduct_url=("Insert into product_url(url,status,review) values(%s,%s,%s)")
                    sqlproduct_url_value=[url,status,review_int_sql]
                    mycursor.execute(sqlproduct_url,sqlproduct_url_value)
                    mydb.commit()
                    print("Bottom success",review_int_sql, url) 
                else:
                    print(" Bottom You have already this Url.") 
                product_amazon += 1
            else:
                print("Bottom sorry")
                product_amazon += 1
        try:
            next_text = driver.find_element(By.XPATH, "(//a[text()='Next'])").text
        except:
            next_text = 0

        if next_text == "Next":
            next = driver.find_element(By.XPATH, "(//a[text()='Next'])")
            driver.get(next.get_attribute('href'))
            print("Bottom Collecting Next Page Products.")
            time.sleep(5)
        else:
            print("Bottom End Products Url collecting.")
            driver.close()
            break
        exit()


