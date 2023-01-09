import mysql.connector
import time
import sys
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.window import WindowTypes
from selenium.common.exceptions import NoSuchElementException
# os.environ['PS_KEY']
# if sys.platform in ['Windows', 'win32', 'cygwin']:
#     mydb = mysql.connector.connect(
#     host = "",
#     user = "",
#     password = "",
#     database = "",
#     port=
#     )
# else:
#     mydb = mysql.connector.connect(
#     host = os.environ['DB_HOST'],
#     user = os.environ['DB_USER'],
#     password = os.environ['DB_PASS'],
#     database = os.environ['DB_NAME'],
#     port=os.environ['DB_PORT']
    
#     )
#https://www.amazon.com/product-reviews/B0735PWRCY
#https://www.amazon.com/product-reviews/{asin}
#https://www.amazon.com/ask/questions/asin/{asin}
mydb = mysql.connector.connect(
    host = "database-1.criq1nathhcp.us-west-2.rds.amazonaws.com",
    user = "admin",
    password = "5HjTd1Fr7e3DS",
    database = "affiliate",
    port= 33360
   )
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

# DB new
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM product_url WHERE status = 0 LIMIT 1")
myresult = mycursor.fetchone()
producturl_get = get_formated_data(mycursor.description,myresult)
producturl =producturl_get['url'] 
print("\nProduct Url---",producturl) 

mycursor = mydb.cursor()
sql = "UPDATE product_url SET status = 1  WHERE id = '{0}' ".format(producturl_get['id'] )
mycursor.execute(sql)
mydb.commit()
 
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(driverUrl,chrome_options=chrome_options)
home =producturl
driver.get(home)
time.sleep(2)

# def visibil_element
def visibil_element(by, selector, wait=5):
        
        element = False
        if by == 'name':
            byselector = By.NAME
        if by == 'xpath':
            byselector = By.XPATH
        if by == 'css':
            byselector = By.CSS_SELECTOR
        if by == 'id':
            byselector = By.ID
        try:

            element = WebDriverWait(driver, wait).until(
                EC.visibility_of_element_located((byselector, selector)))
        except Exception as e:
            print(e)
            element = False
        if element == False:
            
            print("visibil_element not find: ", selector)
        else:
            print(selector)
        return element
 
###products Table start done
productsname=driver.find_element(By.XPATH, "//span[@id='productTitle']").text
productsreview_count_start=driver.find_element(By.XPATH, "//span[@id='acrCustomerReviewText']").text
productsreview_count_int=productsreview_count_start.replace("ratings", "")
productsreview_count_int_f=productsreview_count_int.replace(",", "")
productsreview_count=int(productsreview_count_int_f)
try:
   productsques_count_start=driver.find_element(By.XPATH, "//a[@id='askATFLink']").text
   productsques_count_int=productsques_count_start.split(" ")[0]
   productsques_count_int_f=productsques_count_int.replace(",", "")
   productsques_count=int(productsques_count_int_f)
except:
   productsques_count = 0

productsreview_average_start=driver.find_element(By.XPATH, '//span[@data-hook="rating-out-of-text"]').text
productsreview_average_float=productsreview_average_start.replace(" out of 5", "")
productsreview_average=float(productsreview_average_float)

try :
   productsDescription = driver.find_element(By.XPATH, "//div[@id='productDescription_feature_div' or @class='a-section a-spacing-medium a-spacing-top-small']").text
except:
   try:
      productsDescription=driver.find_element(By.XPATH, "//p[@class='description'] ").text
   except:
      productsDescription = "Empty"
productsurl=driver.current_url 
try:
   productsprice =driver.find_element(By.XPATH, '//span[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]').text
except:
   try:
      price_ffind = driver.find_element(By.XPATH, '//td[contains(text(), "With Deal:") or contains(text(), "List Price:")]')
      productsprice =driver.find_element(By.XPATH, '(//table[@class="a-lineitem a-align-top"]//child::span[@data-a-size="b"])[2]').text
   except:
      try:
          productsprice = driver.find_element(By.XPATH, '(//table[@class="a-lineitem a-align-top"]//child::span[@id="snsDetailPagePrice"])').text
      except:
            try:
               price_ffind = driver.find_element(By.XPATH, '(//table[@class="a-lineitem a-align-top"])//child::span[contains(text(), "Count")]')
               productsprice =driver.find_element(By.XPATH, '(//table[@class="a-lineitem a-align-top"]//child::span[@data-a-size="b"])').text
            except:
               productsprice="00.0" 
try:
   productscatagory=driver.find_element(By.XPATH, '//ul[@class="a-unordered-list a-horizontal a-size-small"]//child::li[1]').text
except:
   productscatagory="Others"

brand= "Amazon's Choice"

print("Price---",productsprice, "\n\nCategory---",productscatagory,"\n\nDisc---",productsDescription,"\n\nBrand---",brand)
time.sleep(2)
store=driver.find_element(By.XPATH, '//a[@id="bylineInfo" or  text() ="Visit the Store" or text()= "Visit the" ]')
store.click()
productsstore_url = driver.current_url
time.sleep(4)
try:
   productsstore_name= driver.find_element(By.XPATH,  '//span[@itemprop="item"]').text
   productsstore_logo=  driver.find_element(By.XPATH, '//img[@class="style__heroImage__12q9C style__cover__2N0YX"]').get_attribute('src')
except:
   productsstore_name = "Amazon's Choice"
   productsstore_logo =  driver.find_element(By.XPATH, '//a[@id="nav-logo-sprites"]').get_attribute('href')
driver.back()
time.sleep(2)
###products Table end
### DB products
mycursor = mydb.cursor()
sqlproducts_value=[productsname,productsreview_count,productsreview_average,productsDescription,productsurl,productsprice,productsstore_name,productsstore_url,productsstore_logo,productscatagory,brand,productsques_count]
sqlproducts=("Insert into products(name,review_count,review_average,Description,url,price,store_name,store_url,store_logo,catagory,brand,ques_count) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
mycursor.execute(sqlproducts,sqlproducts_value)
productid= mycursor.lastrowid
mydb.commit()
 
###product_info Table start
product_infoname_count = len(driver.find_elements(By.XPATH, '(//table[contains(@id, "productDetails" ) or @id="technicalSpecifications_section_1"]//child::th)'))
print("\nTotal info count---",product_infoname_count,"\n")
product_infovalue_f_format= 1
for info_table in range(0,product_infoname_count):
    product_infoname_f=driver.find_element(By.XPATH, '(//table[contains(@id, "productDetails")or @id="technicalSpecifications_section_1"]//child::th)[{0}]'.format(product_infovalue_f_format)).text
    product_infovalue_f=driver.find_element(By.XPATH, '(//table[contains(@id, "productDetails")or @id="technicalSpecifications_section_1"]//child::td)[{0}]'.format(product_infovalue_f_format)).text
    product_infovalue_f_format += 1

    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SELECT type FROM products_infos WHERE name = '{0}'".format(product_infoname_f))
    p_name = mycursor.fetchone()
    if p_name == None:
        p_type = "Technical Information"
    else:
        p_type = p_name[0]
    print("Type---",p_type,"Name---", product_infoname_f,"Value---",product_infovalue_f)
### DB products_info
    mycursor = mydb.cursor(buffered=True)
    sqlproduct_info="Insert into products_infos(product_id,type,name,value) values(%s,%s,%s,%s)"
    sqlproduct_info_value=(productid,p_type,product_infoname_f,product_infovalue_f)

    mycursor.execute(sqlproduct_info,sqlproduct_info_value)
    product_info_id= mycursor.lastrowid
    mydb.commit()

imagesurl = driver.find_element(By.XPATH, '//img[contains(@class, "a-dynamic-image")]').get_attribute('src')
print("\nProduct Img url---", imagesurl)
### DB image
mycursor = mydb.cursor()
sqlimages_value=[productid,imagesurl]
sqlimages=("Insert into product_images(product_id,url) values(%s,%s)")
mycursor.execute(sqlimages,sqlimages_value)
mydb.commit()
###images Table end

###reviews Table start

review=driver.find_element(By.XPATH, '(//a[@data-hook="see-all-reviews-link-foot"])')
review.click()
time.sleep(2)
while True:
    try:
        # next_page_url=driver.find_element(By.XPATH, '//ul[@class="a-pagination"]//child::li[2]//child::a')
        review_count=len(driver.find_elements(By.XPATH, '(//div[@data-hook="review"])'))
        print("\nReview Count---",review_count)
        reviewsuser_name_format = 1
        for x in range(0,review_count):
            time.sleep(2)
            try:
                reviewshelpful_format = 1
                reviewshelpfulx=visibil_element('xpath', '(//span[@class="a-size-base a-color-tertiary cr-vote-text"])[{1}]'.format(reviewshelpful_format)).text
                reviewshelpful=int(reviewshelpfulx.split(" ")[0])
                reviewshelpful_format += 1
            except:
                reviewshelpful=0
            reviewsuser_name=driver.find_element(By.XPATH, '(//span[@class="a-profile-name"])[{0}]'.format(reviewsuser_name_format)).text
            reviewscountry_namex=driver.find_element(By.XPATH, '(//span[@class="a-size-base a-color-secondary review-date"])[{0}]'.format(reviewsuser_name_format)).text
            reviewscountry_namey = reviewscountry_namex.split("the")[1]
            reviewscountry_name = reviewscountry_namey.split("on")[0]
            reviewsdatex=driver.find_element(By.XPATH, '(//span[@class="a-size-base a-color-secondary review-date"])[{0}]'.format(reviewsuser_name_format)).text
            reviewsdate=reviewsdatex.split("on")[1]
            reviewstext=driver.find_element(By.XPATH, '(//span[@class="a-size-base review-text review-text-content"]//child::span)[{0}]'.format(reviewsuser_name_format)).text
            try:
                reviewsstarsx=driver.find_element(By.XPATH, '(//i[@data-hook="review-star-rating-view-point" or @data-hook="review-star-rating"]//child::span)[{0}]'.format(reviewsuser_name_format)).text
                reviewsstars = float(reviewsstarsx.split(" ")[0])
            except:
                reviewsstars = 3.0
            reviewsuser_url_u=driver.find_element(By.XPATH, '(//a[@class="a-profile"])[{0}]'.format(reviewsuser_name_format))
            reviewsuser_url_u.click()
            time.sleep(2)
            review_user_url =  driver.current_url
            reviewsuser_img=driver.find_element(By.XPATH, '//img[@id="avatar-image"]').get_attribute('src')
            reviewsuser_name_format += 1
            driver.back()
            print("Successfully collect Review ---",x)
            # DB reviews
            mycursor = mydb.cursor()
            sqlreviews_value=[productid,reviewshelpful,reviewsuser_name,reviewscountry_name,reviewsdate,review_user_url,reviewstext,reviewsstars,reviewsuser_img]
            sqlreviews="Insert into reviews(product_id,helpful,user_name,country_name,date,user_url,text,stars,user_img) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(sqlreviews,sqlreviews_value)
            mydb.commit()

    except:
        pass

        # next_page_url=driver.find_element(By.XPATH, '//ul[@class="a-pagination"]//child::li[2]')
        # next_page_url.click()
        # time.sleep(2)

    # except NoSuchElementException:
    #     home_page_url=driver.get(home)
    #     review=driver.find_element(By.XPATH, '(//a[@data-hook="see-all-reviews-link-foot"])')
    #     review.click()
    #     review_count=len(driver.find_elements(By.XPATH, '(//div[@data-hook="review"])'))
    #     reviewshelpful_format_except = 1
    #     reviewsuser_name_format_except = 1
    #     for x in range(0,review_count):
            # try:
            #     reviewshelpful_format = 1
            #     reviewshelpfulx=visibil_element('xpath', '(//span[@class="a-size-base a-color-tertiary cr-vote-text"])[{1}]'.format(reviewshelpful_format)).text
            #     reviewshelpful=int(reviewshelpfulx.split(" ")[0])
            #     reviewshelpful_format += 1
            # except:
            #     reviewshelpful=0
    #         time.sleep(2)
            # reviewsuser_name=driver.find_element(By.XPATH, '(//span[@class="a-profile-name"])[{0}]'.format(reviewsuser_name_format_except)).text
            # reviewscountry_namex=driver.find_element(By.XPATH, '(//span[@class="a-size-base a-color-secondary review-date"])[{0}]'.format(reviewsuser_name_format)).text
            # reviewscountry_namey = reviewscountry_namex.split("the")[1]
            # reviewscountry_name = reviewscountry_namey.split("on")[0]
            # reviewsdatex=driver.find_element(By.XPATH, '(//span[@class="a-size-base a-color-secondary review-date"])[{0}]'.format(reviewsuser_name_format)).text
            # reviewsdate=reviewsdatex.split("on")[1] 
            # reviewstext=driver.find_element(By.XPATH, '(//span[@class="a-size-base review-text review-text-content"]//child::span)[{0}]'.format(reviewsuser_name_format_except)).text
            # try:
            #     reviewsstarsx=driver.find_element(By.XPATH, '(//i[@data-hook="review-star-rating-view-point" or @data-hook="review-star-rating"]//child::span)[{0}]'.format(reviewsuser_name_format)).text
            #     reviewsstars = float(reviewsstarsx.split(" ")[0])
            # except:
                # reviewsstars = 3.0
            # reviewsuser_url_u=driver.find_element(By.XPATH, '(//a[@class="a-profile"])[{0}]'.format(reviewsuser_name_format_except))
            # reviewsuser_url_u.click()
            # review_user_url =  driver.current_url
            # time.sleep(2)
            # reviewsuser_img=driver.find_element(By.XPATH, '//img[@id="avatar-image"]').get_attribute('src')
            # time.sleep(2)
            # reviewsuser_name_format_except += 1
            # driver.back()

           # DB reviews
        #     mycursor = mydb.cursor()
        #     sqlreviews_value=[productid,reviewshelpful,reviewsuser_name,reviewscountry_name,reviewsdate,review_user_url,reviewstext,reviewsstars,reviewsuser_img]
        #     sqlreviews="Insert into reviews(product_id,helpful,user_name,country_name,date,user_url,text,stars,user_img) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        #     mycursor.execute(sqlreviews,sqlreviews_value)
        #     mydb.commit()
    break

###question & answers Table start
driver.get(home)
print("\nQuestion count start")
time.sleep(10)
try:
    all_ques_dd =driver.find_element(By.XPATH, ('//span[@class="a-button a-button-base askSeeMoreQuestionsLink"]//child::a'))
    paggee = 1
except:
    paggee = 00

if 1 == paggee:
    all_ques_dd =driver.find_element(By.XPATH, ('//span[@class="a-button a-button-base askSeeMoreQuestionsLink"]//child::a'))
    all_ques =driver.find_element(By.XPATH, ('//span[@class="a-button a-button-base askSeeMoreQuestionsLink"]//child::a')).get_attribute("href")
    driver.get(all_ques)
    time.sleep(2)
    page_li_count = len(driver.find_elements(By.XPATH, ('//ul[@class="a-pagination"]//child::li')))
    page_li_count_c = page_li_count -1
    page_count_b = driver.find_element(By.XPATH, ('(//ul[@class="a-pagination"]//child::li)[{}]'.format(page_li_count_c))).text
    page_count = int(page_count_b) - 1
    print("\nQuestion & Answers page count---",page_count)

    ### Comment out this line 
    # for x in range(0,page_count):
    for x in range(0,1):
        ques_count=len(driver.find_elements(By.XPATH, '//div[@class="a-fixed-left-grid a-spacing-small" and contains(@id, "question-")]'))
        answerIndex= 2
        quesIndex = 1
        for x in range(0,ques_count):
            questionvotes=00
            time.sleep(2)
            questionquestion=driver.find_element(By.XPATH, '(//div[@class="a-fixed-left-grid a-spacing-small" and contains(@id, "question-")])[{0}]'.format(quesIndex)).text
            
            ### DB question
            mycursor = mydb.cursor()
            sqlquestion="Insert into questions(product_id,votes,question) values(%s,%s,%s)"
            sqlquestion_value=[productid,questionvotes,questionquestion]
            mycursor.execute(sqlquestion,sqlquestion_value)
            questionid = mycursor.lastrowid
            mydb.commit()

            ###answers Table start
            answerstext=driver.find_element(By.XPATH, '(//div[@class="a-fixed-left-grid-col a-col-right" and @style="padding-left:0%;float:left;"])[{}]'.format(answerIndex)).text
            answerIndex += 2
            answersdate=driver.find_element(By.XPATH, '(//span[@class="a-color-tertiary aok-align-center"])[{0}]'.format(quesIndex)).text
            answersuser_name= driver.find_element(By.XPATH, '(//span[@class="a-profile-name"])[{0}]'.format(quesIndex)).text
            answershelpful="yes"
            quesIndex +=1
            time.sleep(2)
            ### DB Answers
            mycursor = mydb.cursor()
            sqlanswers="Insert into answers(question_id,text,date,user_name,helpful) values(%s,%s,%s,%s,%s)"
            sqlanswers_value=[questionid,answerstext,answersdate,answersuser_name,answershelpful]
            mycursor.execute(sqlanswers,sqlanswers_value)
            mydb.commit()
            print("Successfully collect Ques---",x)

        time.sleep(2)

        if 1 == (page_count + 1):
            pass
        else:
            next = driver.find_element(By.XPATH, "//a[text()='Next']").get_attribute('href')
            driver.get(next)
        time.sleep(2)
    driver.close()
    print("\n Your Product ID---", productid)
    print("\n Successfully Collected product details","\n BYE!!")

else :
    ques_count=len(driver.find_elements(By.XPATH, '//div[@class="a-fixed-left-grid a-spacing-small" and contains(@id, "question-")]'))
    answerIndex= 2
    quesIndex = 1
    for xyz in range(0,ques_count):
        questionvotes=00
        time.sleep(2)
        questionquestion=driver.find_element(By.XPATH, '(//div[@class="a-fixed-left-grid a-spacing-small" and contains(@id, "question-")])[{0}]'.format(quesIndex)).text
        
        ### DB question
        mycursor = mydb.cursor()
        sqlquestion="Insert into questions(product_id,votes,question) values(%s,%s,%s)"
        sqlquestion_value=[productid,questionvotes,questionquestion]
        mycursor.execute(sqlquestion,sqlquestion_value)
        questionid = mycursor.lastrowid
        mydb.commit()
        ###answers Table start
        answerstext=driver.find_element(By.XPATH, '(//div[@class="a-fixed-left-grid-col a-col-right" and @style="padding-left:0%;float:left;"])[{}]'.format(answerIndex)).text
        answerIndex += 2
        answersdatex=driver.find_element(By.XPATH, '(//span[@class="a-color-tertiary a-nowrap"])[{0}]'.format(quesIndex)).text           
        answersdate = answersdatex.split("on")[1]
        answersuser_namex=answersdatex.split("on")[0]
        answersuser_name = answersuser_namex.replace("by","")
        quesIndex +=1
        answershelpful="yes"
        time.sleep(2)
        ### DB Answers 
        mycursor = mydb.cursor()
        sqlanswers="Insert into answers(question_id,text,date,user_name,helpful) values(%s,%s,%s,%s,%s)"
        sqlanswers_value=[questionid,answerstext,answersdate,answersuser_name,answershelpful]
        mycursor.execute(sqlanswers,sqlanswers_value)
        mydb.commit()
        print("Per Ques count---",xyz)
    driver.close()
    print("\n Your Product ID---", productid)
    print("\n Successfully Collected product details","\n BYE!!")

###answers Table end
###question Table end
