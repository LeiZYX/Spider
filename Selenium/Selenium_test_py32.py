from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq

browser =webdriver.Firefox()
wait=WebDriverWait(browser, 10)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))#'#'代表id
    html = browser.page_source
    doc=pq(html)
    items=doc('#mainsrp-itemlist .items .item').items()

    for item in items:
        if item.find('.pic .img').attr('src'):
            product={
                'image':item.find('.pic .img').attr('src'),#获取商品照片
                'id':re.findall(r"(\d+)",item.find('.pic .img').attr('id'),re.S)[0],#获取商品在淘宝上的（唯一）编号
                'price':float(re.findall(r"(\d+\.\d+)",item.find('.price').text(), re.S)[0]),#获取商品单价
                'deal':float(item.find('.deal-cnt').text()[:-3]),#获取商品成交量
                'title':item.find('.title').text().replace(' ',''),#获取商品标题
                'shop':item.find('.shop').text(),#获取商品所属的店铺信息
                'location':item.find('.location').text()#获取店铺的位置信息
            }
            print(product)

def search():
    try:

        browser.get('http://www.taobao.com')
        wait=WebDriverWait(browser, 10)
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))#'#J_TSearchForm > div.search-button > button'这些需要根据具体的网页具体分析
        input.send_keys('fenix3 HR')
        submit.click()
        total=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
    except TimeoutException:
        return search()

def next_page(page_number):
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)



#driver = webdriver.Firefox()
#driver.get("http://www.python.org")
#assert "Python" in driver.title
#elem = driver.find_element_by_name("q")
#elem.send_keys("python")
#elem.send_keys(Keys.RETURN)
#print(driver.page_source)
#driver.quit()




def main():
    total=search()
    total=int(re.compile('(\d+)').search(total).group(1))
    for i in range(2,total+1):
        next_page(i)#显示当前爬取网页的页数
        print ('搞定%d'%i)

if __name__=='__main__':
    main()

