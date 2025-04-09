from selenium import webdriver
from selenium.webdriver.common.by import By
import time, os, requests


###### BY AKESHIIV 

query = "your search query"
folder_name = "folder name. example: images"

def find_urls(query, print_urls=False):
    # query -- your search query, e.g. "birds", "dog"
    # print urls -- 'True' will print out every image url found.
    url = f"https://www.google.com/search?q={query}&tbm=isch"

    driver = webdriver.Chrome()
    driver.get(url)

    # scroll + load more images
    for i in range(10):  # change the range() no. for more images
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # getting the image urls
    images = driver.find_elements(By.TAG_NAME, "img")
    image_urls = []

    for image in images:
        url = image.get_attribute("src")
        # to avoid base64-encoded images (data:image/...) or any imgs that r 
        # more of placeholders / work only on the site; empty links
        name = image.get_attribute("alt")
        if url and "images?q=tbn" in url: 
            image_urls.append(url)
            if print_urls:
               print(url)

    driver.quit()

    print(f"Found {len(image_urls)} images")
    return image_urls

def download_img(query, folder_name):
    # navigate into curr directory (see your terminal) -> create new directory within
    try:
        path = os.path.join(os.getcwd(), folder_name)
        os.makedirs(path)
    except:
        raise Exception("Unable to create directory.")

    # cd into folder_name folder, basically, & download all images
    os.chdir(path)
    urls = find_urls(query)
    for i, url in enumerate(urls):
        fname = f"image_{i}"
        with open(f"{fname}.png", "wb") as f:
            img = requests.get(url)
            f.write(img.content)
    return f"Images successfully downloaded."

download_img(query, folder_name)
