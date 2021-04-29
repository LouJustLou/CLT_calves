#packages for selenium time functions, pandas and seaborn for histograms.
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd 

import seaborn as sns

# create a list to store the comments in
data=[]

#Call the Chrome Driver application to start the chrome testing interface. Also lists the youtube page for 
#video. I'm going to send the END key 40 times and copy the comment value from the page.
#the time.sleep(15) is a crude way to pause for the screen to update but it works in this example
#best to try more concrete ways to verify update and gracefully exit if it does not.

with Chrome(executable_path=r'C:\Users\Dell T3600\Downloads\chromedriver_win32\chromedriver.exe') as driver:
    wait = WebDriverWait(driver,15)
    driver.get("https://www.youtube.com/watch?v=pjMUieLXe4Q")
    
    for i in range(40): 
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
        time.sleep(15)
        
    for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
        data.append(comment.text)

                

#convert the list to a pandas data frame with one column called comment.

df = pd.DataFrame(data, columns=['comment'])
df.head()


#some cleaning and extracting here. Using a regulular expression to pull only numbers
#convert the com_num text value to numberic using pd.to_numeric
#Cleaning up numeric values for just those that are reasonable guesses. 20 to 200 Some 
#comment had years or values that were not guesses.

df["com_num"] = df["comment"].str.extract("(\d*\.?\d+)", expand=True)
df.head()
df.dtypes
df["com_int"] = pd.to_numeric(df["com_num"])
df.dtypes

df1 = df.query('com_int > 20 & com_int < 200')


#plot the values to see if we have a normal - ish distribution
#the assumption of independent guesses may not apply since everyone
#potentially could see others guesses.

sns.set_style('whitegrid')
sns.distplot(df1['com_int'], kde = False, color ='red', bins = 30)

print('Mean : ', df1['com_int'].mean(skipna='True'))
print('Max : ', df1['com_int'].max(skipna='True'))
print('Min :',  df1['com_int'].min(skipna='True'))
print('Median :', df1['com_int'].median(skipna='True'))

# How does our estimate compare to the actual value of 65 pounds.

acc = df1['com_int'].mean(skipna='True') / 65

print('Your guess was :',  "{:.2%}".format(acc)  , ' accurate.' )

