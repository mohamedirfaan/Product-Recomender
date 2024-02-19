file = open("a.txt",'r',encoding='utf-8')
contents = file.read()
contents = contents.split("\n")
titles = []
comment_count=[]
from emotion import model
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
