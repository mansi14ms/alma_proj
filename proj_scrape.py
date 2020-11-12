from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import numpy
username = str(input("Enter organization name"))
top_n=int(input("Enter  the top n results that you want"))
inside_m=int(input("Enter  the top m commitees and their commint counts that you want"))

url = "https://github.com/"+username+"?tab=repositories"
chromedriver_path = 'C:\\Users\\mansi\\Downloads\\chromedriver_win32\\chromedriver.exe' # Change this to your own chromedriver path!
driver = webdriver.Chrome(executable_path=chromedriver_path)
driver.get(url)
data_strings = []
data_numbers = []
index = 0
time.sleep(30)
driver.find_element_by_xpath("//summary[@class='btn select-menu-button']").click()
driver.find_elements_by_xpath("//label[@class='select-menu-item']")[2].click()
time.sleep(5)

while index < top_n:
    for i in range(0, top_n+1):
        repoName = driver.find_elements_by_xpath("//a[@itemprop='name codeRepository']")[i].text
        print(repoName)
        data_strings.append(repoName)
        forks = driver.find_elements_by_xpath("//a[@class='muted-link mr-3']")[i].text
        print(forks)
        try:
            data_numbers.append(int(forks.replace(',', '')))
        except ValueError:
            print("")

    try:
        index += 1
        print("Next Page " + str(index))
        driver.find_element_by_xpath("//a[@class='next_page']").click()
        time.sleep(2)
    except NoSuchElementException:
        break

print("Numbers are " + str(data_numbers))
in_arr = numpy.array(data_numbers)
sorted_index = numpy.argsort(in_arr)

print(data_strings[sorted_index[sorted_index.size-1]]+", "+data_strings[sorted_index[sorted_index.size-2]]+", "+data_strings[sorted_index[sorted_index.size-3]])

for it in range(1,top_n+1):
    driver.get("https://github.com/google/"+data_strings[sorted_index[sorted_index.size-it]])
    outer_box = driver.find_element_by_xpath("//div[@class='Box mb-3']")
    print("Repo Name : " + data_strings[sorted_index[sorted_index.size-it]])
    print("Repo Forks : " + str(data_numbers[sorted_index[sorted_index.size-it]]))

    inner = outer_box.find_element_by_xpath("//div[@class='flex-shrink-0']")
    commit = outer_box.find_element_by_xpath("//div[@class='flex-shrink-0']").text.splitlines()

    print("Repo Commits : " + commit[1])
