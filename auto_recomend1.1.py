from selenium import webdriver
import pandas as pd
import time
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import datetime
import os

main_url = "https://www.naukri.com"

def extract_recommended_links(user,password):

    driver = webdriver.Chrome()
    driver.get(main_url)
    driver.maximize_window()

    wait = WebDriverWait(driver,10)
    
    # Click on Log-In
    log_in_layer = (By.XPATH,"//a[@id='login_Layer']")
    wait.until(EC.element_to_be_clickable(log_in_layer)).click()

    # Input your Detail
    username_deatails = (By.XPATH,"//input[@placeholder='Enter your active Email ID / Username']")
    password_details = (By.XPATH, "//input[@placeholder='Enter your password']")
    log_in_click = (By.XPATH,"//button[@type='submit']")

    wait.until(EC.visibility_of_element_located(username_deatails)).send_keys(user)
    wait.until(EC.visibility_of_element_located(password_details)).send_keys(password)
    wait.until(EC.element_to_be_clickable(log_in_click)).click()

    wait.until(EC.element_to_be_clickable((By.XPATH,"//li[@class='nI-gNb-custom-Jobs nI-gNb-menuItems']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@href='/mnjuser/recommendedjobs']//div[contains(text(),'Recommended jobs')]"))).click()

    # wait.until(EC.visibility_of_all_elements_located((By.XPATH,"//div/article")))

    ls = driver.find_elements(By.XPATH,"//div/article")
    ls1 = driver.find_elements(By.XPATH,"//p")
    ls2 = driver.find_elements(By.XPATH,"//div[@class='left-sec']//div//div[3]//article/div[2]/div/div[1]/div/span[1]")
    ls3 = driver.find_elements(By.XPATH,"//div[@class='left-sec']//div//div[3]//article/div[2]/div/div[1]/ul/li[1]")
    ls4 = driver.find_elements(By.XPATH,"//div[@class='left-sec']//div//div[3]//article/div[2]/div/div[1]/ul/li[3]")

    j_id = [ls[i].get_attribute('data-job-id') for i in range(len(ls))][:-1]
    j_id1 = [ls1[i].text for i in range(len(ls1))][:-1]
    j_id2 = [ls2[i].text for i in range(len(ls2))]
    j_id3 = [ls3[i].text for i in range(len(ls3))]
    j_id4 = [ls4[i].text for i in range(len(ls4))]

    driver.close()

    df = pd.DataFrame({'job_id':j_id,'job_title':j_id1,'company':j_id2,'experience':j_id3,'location':j_id4})

    def make_url(job_title,company,exe,loc,job_id):
        
        job_title = re.sub(r'[-_()|/, .&+!:;]+', '-', job_title.lower())
        
        company = re.sub(r'[-_()|/, .&+!:;]+', '-', company.lower())
        
        loc = re.sub(r'[-_()|/, .&/]+', '-', loc.lower()).replace('All Areas','location')
        
        exe = exe.replace('-','-to-').replace(' Yrs','-years')
        
        url = f"https://www.naukri.com/job-listings-{job_title}-{company}-{loc}-{exe}-{job_id}"
        
        URL = re.sub(r'[-]+', '-', url)
        
        return URL

    df['url'] = df.apply(lambda x: make_url(x['job_title'],x['company'],x['experience'],x['location'],x['job_id']),axis = 1)

    return df['url'].values


def auto_apply(user_first ,password_first, user_second, password_second):
    
    driver = webdriver.Chrome()
    driver.get(main_url)
    driver.maximize_window()

    wait = WebDriverWait(driver,5)

    # Click on Log-In
    log_in_layer = (By.XPATH,"//a[@id='login_Layer']")
    wait.until(EC.element_to_be_clickable(log_in_layer)).click()

    # Input your Detail
    username_deatails = (By.XPATH,"//input[@placeholder='Enter your active Email ID / Username']")
    password_details = (By.XPATH, "//input[@placeholder='Enter your password']")
    log_in_click = (By.XPATH,"//button[@type='submit']")

    wait.until(EC.visibility_of_element_located(username_deatails)).send_keys(user_first)
    wait.until(EC.visibility_of_element_located(password_details)).send_keys(password_first)
    wait.until(EC.element_to_be_clickable(log_in_click)).click()

    time.sleep(2)

    not_possible = []
    count_url = 0
    applied = 0 
    er=[]

    for url in extract_recommended_links(user_second, password_second):
        count_url +=1

        driver.get(url)
        
        try:
    # Wait up to 10 seconds for the button to be clickable
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[2]")))
            button = driver.find_element(By.XPATH, "//button[2]")
            if button.text == 'Apply':
                button.click()
                applied += 1
            else:
                not_possible.append([url, button.text])
        except Exception as e:
            er.append([url,e])
        
    not_possible_df = pd.DataFrame(not_possible)
    er_df =  pd.DataFrame(er)
    
    print(count_url)
    print(applied)
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%d%m%y_%I%M%p")

    filename = formatted_datetime+'.csv'
    path = r'C:\Users\Aditya\Desktop\Naukri\Auto Recommend'
    save_path = os.path.join(path,filename)
    not_possible_df.to_csv(save_path,index=False)
    er_df.to_csv(r"C:\Users\Aditya\Desktop\Naukri\Auto Recommend\error1.csv",index=False)


user1 = 'a.mulay9501@gmail.com'
password1 = 'Aditya@2201'

user2 = 'adi221800@gmail.com'
password2 = '5zJV!&zCSw6pGdA'

print(auto_apply(user_first=user2,password_first=password2, user_second=user2,password_second=password2))


def get_job_without_login(jobdesgn,yrsexp,fresh):
    driver = webdriver.Chrome()
    driver.get(main_url)
    driver.maximize_window()

    wait = WebDriverWait(driver,10)
    chain = ActionChains(driver)

    # Input Designation
    search = (By.XPATH,"(//input[contains(@placeholder,'Enter skills / designations / companies')])[1]")
    wait.until(EC.element_to_be_clickable(search)).send_keys(jobdesgn)

    # Click on Search
    search_click = (By.CSS_SELECTOR, ".qsbSubmit")
    wait.until(EC.element_to_be_clickable(search_click)).click()
    
    if fresh == 'recent':
        driver.execute_script("window.scrollBy(0,1700)","")

        freshness = (By.XPATH,"//input[@id='filter-freshnessFor']")
        wait.until(EC.element_to_be_clickable(freshness)).click()
        wait.until(EC.element_to_be_clickable(freshness)).click()

        job_posted = (By.XPATH,"//div[@id='dp_filter-freshness'][1]//div/ul/li[5]")
        wait.until(EC.visibility_of_element_located(job_posted))
        chain.move_to_element(driver.find_element(By.XPATH,"//div[@id='dp_filter-freshness'][1]//div/ul/li[5]")).click().perform()
    else:
        pass

    wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='inside']")))
    dragger=driver.find_element(By.XPATH,"//div[@class='inside']")
    chain.move_to_element(dragger).click_and_hold().pause(1).drag_and_drop_by_offset(dragger,(((yrsexp)*7)-210),0).perform()

    wait.until(EC.visibility_of_element_located((By.XPATH, "/html[1]/body[1]/div[1]/div[4]/div[1]/div[1]/section[2]/div[1]/div[1]/span[1]")))
    total_listing = driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[4]/div[1]/div[1]/section[2]/div[1]/div[1]/span[1]").text
    pages = int(int(total_listing.split(" ")[-1])/(int(total_listing.split(' ')[2])))

    print(f'Total Job postings are {total_listing.split(" ")[-1]}')

    job_link = []

    i=0

    while i<pages:
        
        jobs_wait = (By.XPATH,"//article")
        wait.until(EC.visibility_of_all_elements_located(jobs_wait))
        
        jobs = driver.find_elements(By.XPATH,"//article")

        for j in range(len(jobs)):
            
            total_jobs = ['Data Scientist', 'Data Analyst', 'ML', 'AI', 'Power BI','Tableau ','BI Analyst', 
            'Machine Learning', 'Artificial Intelligence','Python Developer','Data Visualization','Data Analysis']
            
            if jobdesgn.lower() in driver.find_element(By.XPATH, f'//article[{j+1}]/div[1]/div[1]/a[1]').text.lower() or any(z.lower() in driver.find_element(By.XPATH, f'//article[{j+1}]/div[1]/div[1]/a[1]').text.lower() for z in total_jobs):
                
                job_link.append(driver.find_element(By.XPATH, f'//article[{j+1}]/div[1]/div[1]/a[1]').get_attribute('href'))

        driver.execute_script("window.scrollBy(0,4800)","")
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH,"//a[@class='fright fs14 btn-secondary br2']"))).click()
        except:
            pass

        i+=1
    print(f"relevant jobs {len(job_link)}")
    return job_link

def search_apply(userid,secure,jobdesgn,yrsexp,fresh):
    
    driver = webdriver.Chrome()
    driver.get(main_url)
    driver.maximize_window()

    wait = WebDriverWait(driver,10)

    # Click on Log-In
    log_in_layer = (By.XPATH,"//a[@id='login_Layer']")
    wait.until(EC.element_to_be_clickable(log_in_layer)).click()

    # Input your Detail
    username_deatails = (By.XPATH,"//input[@placeholder='Enter your active Email ID / Username']")
    password_details = (By.XPATH, "//input[@placeholder='Enter your password']")
    log_in_click = (By.XPATH,"//button[@type='submit']")

    wait.until(EC.visibility_of_element_located(username_deatails)).send_keys(userid)
    wait.until(EC.visibility_of_element_located(password_details)).send_keys(secure)
    wait.until(EC.element_to_be_clickable(log_in_click)).click()

    time.sleep(2)
    try_something = []
    for joburl in get_job_without_login(jobdesgn,yrsexp,fresh):
        
        driver.get(joburl)
        try:
            button = driver.find_element(By.XPATH,"//div[@class='apply-button-container']//button[@class='apply-button'][normalize-space()='Apply']")
            if button.text == 'Apply':
                button.click()
        except:
            try_something.append(joburl)
    print(len(try_something))
    return try_something
    
# print(search_apply(user2,password2,'Machine Learning',4,'recent'))
            
