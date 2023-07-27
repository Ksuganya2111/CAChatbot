from undetected_chromedriver import Chrome
import time 
from selenium.webdriver.common.by import By
import bs4
driver = Chrome() 
driver.get("https://in.indeed.com/") 
driver.maximize_window() 
time.sleep(10) 
what = driver.find_element("id", "text-input-what")
where = driver.find_element("id", "text-input-where")
what.send_keys("AI/ML")
where.send_keys("Coimbatore")
time.sleep(10)
l = driver.find_element(By.CLASS_NAME, "yosegi-InlineWhatWhere-primaryButton")
driver.execute_script("arguments[0].click();", l)
loc_url = driver.current_url
driver.get(loc_url)
job_title_xp = """//div[@id="mosaic-jobResults"]//h2//span"""
job_titles = driver.find_elements(By.XPATH, job_title_xp)
job_titles = [job_title.text for job_title in job_titles]
xpath = """//div[@class="css-1m4cuuf e37uo190"]//h2/a/@href"""
elements = driver.find_elements(By.XPATH, """//div[@class="css-1m4cuuf e37uo190"]//h2/a""")
hrefs = [element.get_attribute("href") for element in elements]
print(hrefs)
with open("links.txt", "w") as f:
    for href in hrefs:
        f.write(href)
        f.write("\n")
def extract_data(url, id, title):
    driver.get(url)
    comp_name = """//div[@class= "jobsearch-CompanyInfoContainer"]//a"""
    company_name = driver.find_element(By.XPATH, comp_name).text
    # print(company_name)
    loc = """//div[@class= "jobsearch-CompanyInfoContainer"]/div/div/div/div"""
    location = driver.find_elements(By.XPATH, loc)[1].text
    # print(location)
    soup=bs4.BeautifulSoup(driver.page_source, 'html.parser')
    names=soup.findAll('title')
    with open("jobs.txt", "a", encoding="utf-8") as f:
       f.writelines("###ID ")
       f.writelines(id)
       f.writelines("\n")
       f.writelines("###TITLE")
       f.writelines(title)
       f.writelines("\n")
       f.writelines("###COMPANYNAME")
       f.writelines(company_name)
       f.writelines("\n")
       f.writelines("###LOCATION")
       f.writelines(location)
       f.writelines("\n")
    for i in names:
       print(i.text)
       # print(names.text)
       with open("jobs.txt", "a", encoding="utf-8") as f:
           f.writelines(i.text )
       with open("jobs.txt", "a", encoding="utf-8") as f:
           f.writelines("\n" )
    div_bs4 = soup.find('div', id = "jobDescriptionText")
    for div in div_bs4:
        print(div.text)
        with open("jobs.txt", "a", encoding="utf-8") as f:
           f.writelines(div.text)
        with open("jobs.txt", "a", encoding="utf-8") as f:
           f.writelines("\n" )
    with open("jobs.txt", "a", encoding="utf-8") as f:
           f.writelines("\n\n\n\n\n\n" )
with open("links.txt", "r") as f:
    links = f.readlines()
print(links[0][:-2])
# cleaned_links = [link[:-2] for link in links]
id = 0
for link,title in zip(links, job_titles):  
    # print(link)
    extract_data(link, str(id), title)
    id+=1
driver.close()

# name = """//div[@class= "jobsearch-CompanyInfoContainer"]//a"""
# driver.get("https://in.indeed.com/viewjob?jk=07cc2af1ab2ea2e7&from=serp&vjs=3")
# company_name = driver.find_element(By.XPATH, name).text
# print(company_name)
# loc = """//div[@class= "jobsearch-CompanyInfoContainer"]/div/div/div/div"""
# location = driver.find_elements(By.XPATH, loc)[1].text
# print(location)
# driver.close()
# soup=bs4.BeautifulSoup(driver.page_source, 'html.parser')
# div_bs4 = soup.find('div', {"class" : "jobsearch-CompanyInfoContainer"})
# texts = [r.text.strip() for r in div_bs4]
# print(texts)