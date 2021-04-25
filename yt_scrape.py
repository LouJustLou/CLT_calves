
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 

import seaborn as sns

  
data=[]

with Chrome(executable_path=r'C:\Users\Dell T3600\Downloads\chromedriver_win32\chromedriver.exe') as driver:
    wait = WebDriverWait(driver,15)
    driver.get("https://www.youtube.com/watch?v=pjMUieLXe4Q")
    
    for i in range(40): 
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(15)
        
    for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
        data.append(comment.text)

                

df = pd.DataFrame(data, columns=['comment'])
df.head()



df["com_num"] = df["comment"].str.extract("(\d*\.?\d+)", expand=True)
df.head()
df.dtypes
df["com_int"] = pd.to_numeric(df["com_num"])
df.dtypes

df1 = df.query('com_int > 20 & com_int < 200')



sns.set_style('whitegrid')
sns.distplot(df1['com_int'], kde = False, color ='red', bins = 30)

print('Mean : ', df1['com_int'].mean(skipna='True'))
print('Max : ', df1['com_int'].max(skipna='True'))
print('Min :',  df1['com_int'].min(skipna='True'))
print('Median :', df1['com_int'].median(skipna='True'))

acc = df1['com_int'].mean(skipna='True') / 65

print('Your guess was :',  "{:.2%}".format(acc)  , ' accurate.' )

