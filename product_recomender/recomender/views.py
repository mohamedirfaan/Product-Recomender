from django.shortcuts import render,redirect

from .emotion import model
from bs4 import BeautifulSoup
import requests
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
    def __init__(self,p,b):
        prod = p
        print("enter the models you are interested in : ")
        a = b
        for i in a:
            scraper = Scrape_Model(prod.lower(),i.lower())
# comment_creator = create_comment_file()

#comment_creator = create_comment_file()



# Create your views here.
def home(request):
    if(request.method=="POST"):
        print("in post")
        product = request.POST.get('product')
        product = str(product)
        print("product name : ",product)
        brands = request.POST.get('brand')
        brands = str(brands).split(",")
        print("brands : ",brands)
        comment_creator = create_comment_file(product,brands)
        file = open("a.txt",'r',encoding='utf-8')
        contents = file.read()
        contents = contents.split("\n")
        titles = []
        comment_count=[]
        
        comment_file = open("a.txt","r",encoding='utf-8')
        #if(len(comment_file.read())==0):
        #from webscrape import comment_creator


        print(model.accuracy)
        for i in contents:
            count = 0
            c=i.split("####")
            titles.append(c[0])
            comment = ("".join(c[1:]).split("::::"))
            for i in comment:
                vectorized_comment = model.vectorize_values([i])
                prediction = model.predictive_function(vectorized_comment)
                if(prediction == 'positive'):
                    count+=1
            comment_count.append(count/len(comment))
        '''for i in range(len(comment_count)):
            print(titles[i],comment_count[i])'''
        links = open("linker.txt","r", encoding="utf-8")
        link_tags = links.read().split("\n")
        for i in range(len(comment_count)):
            print(titles[i],comment_count[i])
        print("\n\nthe best product to buy is : ",titles[comment_count.index(max(comment_count))],"\n\n\n")
        print(link_tags[comment_count.index(max(comment_count))])
        context={}
        a_tag=link_tags[comment_count.index(max(comment_count))]
        soup = BeautifulSoup(a_tag,'html.parser')
        a_tag = soup.find_all('a',class_='_1fQZEK')
        print(type(a_tag))
        print(a_tag)
        freff = a_tag[0]['href']
        a_tag[0]['href']="https://www.flipkart.com"+freff
        a_tag = str(a_tag)
        context["linked"]="".join(a_tag)
        return render(request,"recomender.html",context)
    else:
        return render(request,"recomender.html")