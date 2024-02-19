from bs4 import BeautifulSoup
import requests
class Scrape_Model:
    def get_url(self,prod,strr):
        #url = 'https://www.flipkart.com/search?sid=6bo%2Cb5g&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_11_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_11_na_na_na&as-pos=1&as-type=HISTORY&suggestionId=laptop+sony%7CLaptops&requestId=16edb031-0a25-4dd5-b6a0-2c66b2d2d9f3&q=laptop%20'+str
        link = "https://www.flipkart.com/search?q="+prod
        url = link+strr
        print(url)
        return url
    def get_response(self,prod,strr):
        response = requests.get(self.get_url(prod,strr))
        return response
    def __init__(self,prod,strr):
        #self.set_product(prod)
        #print("link",self.link)
        h=self.get_response(prod,strr).text
        soup = BeautifulSoup(h,'html.parser')
        # print("soup : ",soup)
        data = soup.find_all('a',class_='_1fQZEK')
        # print("data : ",data)
        links = data
        linker_file = open("linker.txt","w", encoding="utf-8")
        for i in links:
            linker_file.write(str(i)+"\n")
        linker_file.close()
        urls_list = []
        for i in data:
            # print(i.get('href'))
            urls_list.append('https://www.flipkart.com'+i.get('href'))
        # print(urls_list)
        a = open('a.txt', 'w',encoding='utf-8')
        for url in urls_list:
            response = requests.get(url)
            h = response.text
            soup = BeautifulSoup(h, 'html.parser')
            # print("soup :",soup)
            # break
            data = soup.find_all('div', class_='t-ZTKy')
            # print(data)
            review_texts = {}
            try:
                title = soup.find('title').string
                # print(title)
                for i in data:
                    if title not in review_texts:
                        review_texts[title] = []
                        a.write("\n"+title+"####")
                    # print("writing content")
                    review_texts[title].append(i.text)
                    a.write("::::"+i.text)
                    a.flush()
            except Exception as e:
                print("exceptipon e")
        a.close()
class create_comment_file:
    def __init__(self):
        prod = input("enter product : ")
        print("enter the models you are interested in : ")
        a = list(map(str,input().split()))
        for i in a:
            scraper = Scrape_Model(prod.lower(),i.lower())
comment_creator = create_comment_file()
