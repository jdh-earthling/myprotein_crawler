from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import io
from selenium.webdriver.common.action_chains import ActionChains

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

##open chrome and myprotein site
path ="C:\\Users\\jeong\\Documents\\github\\chromedriver.exe"
driver=webdriver.Chrome(path)
driver.get("https://www.myprotein.co.kr/nutrition.list")



#get product categories
protein=""" //*[@id="mainContent"]/div[3]/div/div[1]/a/div/h3 """
food=""" //*[@id="mainContent"]/div[3]/div/div[2]/a/div/h3 """
vitamin=""" //*[@id="mainContent"]/div[3]/div/div[3]/a/div/h3 """
amino=""" //*[@id="mainContent"]/div[3]/div/div[4]/a/div/h3 """
prepostworkout=""" //*[@id="mainContent"]/div[3]/div/div[5]/a/div/h3 """


#for (i:category)
#see products list on a new tab
category=driver.find_element_by_xpath(protein)
ActionChains(driver).key_down(Keys.CONTROL).click(category).key_up(Keys.CONTROL).perform()
driver.switch_to_window(driver.window_handles[1])
#wait until page is loaded
try:
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH , """ //*[@id="mainContent"]/div/div[1]/main/div[1]/div[1]/p """))
    )
except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

#prints out number of products of certain category
num_of_results= driver.find_element_by_xpath(""" //*[@id="mainContent"]/div/div[1]/main/div[1]/div[1]/p """)
print(num_of_results.text)
#print names of products


clicknext=1

plist=driver.find_elements_by_class_name("athenaProductBlock_productName")

#for product in plist[::10]:
for product in plist:
    print('PRODUCTNAME= ', product.text)
    ActionChains(driver).key_down(Keys.CONTROL).click(product).key_up(Keys.CONTROL).perform()
    driver.switch_to_window(driver.window_handles[2])
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH , """//*[@id="product-description-content-8"]/div/div"""))
        )
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    #expand

    info = driver.find_element_by_xpath("""//*[@id="product-description-content-8"]/div/div""")
    # //*[@id="product-description-content-lg-8"]/div/div
    serving_info=info.find_elements_by_xpath(".//p")
    nutritional_info=info.find_elements_by_xpath(".//table")

    print("SERVINGINFO1= ",serving_info[0].get_attribute('textContent'))
    print("SERVINGINFO2= ",serving_info[1].get_attribute('textContent'))

    for line in nutritional_info:
        a= line.tag_name
        info=line.get_attribute('textContent').strip().split()
        print("NUTINFO= ",info)
        #print(line.get_attribute('textContent'))
    driver.close()
    driver.switch_to_window(driver.window_handles[1])


#pagenumblock=driver.find_element_by_xpath("""//*[@id="mainContent"]/div/div[1]/main/div[4]/nav""")
#driver.find_element_by_xpath("""//*[@id="mainContent"]/div/div[1]/main/div[4]/nav/ul/li[3]/a""").click()


driver.quit()