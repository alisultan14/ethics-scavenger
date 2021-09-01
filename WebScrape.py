#installing the BeautifulSoup lib, which is an HTML parser
import bs4
#installing the function urlopen from package urlib and module request
#the function has been named uReq
from urllib.request import urlopen as uReq
#installing the BeautifulSoup module from bs4 package, we will call it as soup
from bs4 import BeautifulSoup as soup
from bs4 import element
from numpy import maximum, nan, true_divide
#import pandas
import pandas as pd
#importing re
import re
#importing reqs
import requests
import time
import os
import re

#using absolute path, must change 
df = pd.read_csv("ethics-scavenger/Input.csv")

#defining the keyword dict
#privacy and security are given -1 since they appear on the GitHub footer
keywords = {"accoutabiliy":0,"accuracy":0,"auton":0,"bias":0,"consent":0,"cost":0,"criminal":0,"discrimin":0,"ethic":0,"freedom":0,"gender":0,"hate":0,"hazard":0,"inequality":0,"integrity":0,"liab":0,"malicious":0,"military":0,"misuse":0,"negative":0,"privacy":-1,"propaganda":0,"rights":0,"security":-2,"sex":0,"societ":0,"transpar":0,"trust":0,"unfairness":0,"violat":0}

def reset():
    keywords.update({"accoutabiliy":0,"accuracy":0,"auton":0,"bias":0,"consent":0,"cost":0,"criminal":0,"discrimin":0,"ethic":0,"freedom":0,"gender":0,"hate":0,"hazard":0,"inequality":0,"integrity":0,"liab":0,"malicious":0,"military":0,"misuse":0,"negative":0,"privacy":-1,"propaganda":0,"rights":0,"security":-2,"sex":0,"societ":0,"transpar":0,"trust":0,"unfairness":0,"violat":0})
    
def checkReadMe(url,index):

    try:
        if (index==len(df)-1):
            return
         #downloading the webpage after connecting
        uClient = uReq(url)

         #storing the html in a variable
        page_html = uClient.read()

         #close the client
        uClient.close()

         #directing the soup to use the html parser
        page_soup = soup(page_html, "html.parser")
        
        containers = page_soup.findAll("div",{"id":"readme"})
       
        page_soup_3 = soup(str(containers[0]),"html.parser")

        links = []
        for link in page_soup_3.findAll('a'):
           links.append(link.get('href'))

        for link in links:
            if ("github" or "#" or "openai" or "github.com" or "features" or "/openai/"  in link) or ("https" not in link):
                links.remove(link)
            
        link_output = ""
        for link in links:
            link_output = link_output + "|" + str(link)
        
        df.loc[index,'Links to other pages']=link_output
        
        text = page_soup.get_text()
        output=""

         #iterating over the words
        for word in keywords:
        
            #change to substring 
          if (word in text.lower()):


            keywords[word]+=1
            if (keywords[word.lower()]==1 ):
              output=output+"|"+word
               
        df.loc[index,'ReadMe']=output
      
        print ("Checked ReadMe of "+url)

    except:
        print("Done with"+str(index + 1)+ " repositories")
        df.to_csv("output_final.csv", encoding='utf-8', index=False)
        print("Output file has been generated!")
        quit()

       # time.sleep(5)
        #checkReadMe(url,index)

def searchIssues(url):
    
    #downloading the webpage after connecting

    try:
         uClient = uReq(url)

         #storing the html in a variable
         page_html = uClient.read()

         #close the client
         uClient.close()

         #directing the soup to use the html parser
         page_soup = soup(page_html, "html.parser")

         text = page_soup.get_text()
          # break into lines and remove leading and trailing space on each
         lines = (line.strip() for line in text.splitlines())
    
          # break multi-headlines into a line each
         chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    
          # drop blank lines
         text = '\n'.join(chunk for chunk in chunks if chunk)

          #refining the text
         final_text = re.split(' |\n', text)

          #method to return True or False depending on weather the keyword search was successfull
         if 'No' in final_text and 'results' in final_text and 'matched' in final_text and 'your' in final_text:
           return False
         else:
          return True
    
    except:
        
         time.sleep(5)
         searchIssues(url)
        
#method to go and search the issues one by one through keywords
def issues(list,url,index):
    output = ""
    for word in list:
        issue_url = url+"/issues?q="+word
        if ((searchIssues(issue_url))==True):
            output=output+"|"+word

    df.loc[index,'Issues']=output
    print("Checked Issues of "+url)

#method which goes through all the URLS and collects information
def scrape(dataframe):
    for i in range(0,len(df)):
        t_url=dataframe.loc[i,'URL']
        checkReadMe(t_url,i)
        reset()
        issues(keywords,t_url,i)

#call the method
#scrape(df)
#recursive helper method which will be used in the program afterwards



    





def otherFiles(url,i):

    try:
        uClient = uReq(url)
   
     #storing the html in a variable
        page_html = uClient.read()
    #close the client
        uClient.close()

     #directing the soup to use the html parser
        page_soup = soup(page_html, "html.parser")

    #getting all the links to the other files found in the Navigation box
        containers = page_soup.findAll("a",{"class":"js-navigation-open Link--primary"})
        links = []

        for link in containers:
          links.append("https://github.com"+link.get('href'))

        if (len(links)==0):
          text = page_soup.get_text()
          output=""

         #iterating over the words
          for word in keywords:
        
            #change to substring 
           if (word in text.lower()):
            keywords[word]+=1
            if (keywords[word.lower()]==1 ):
              output=output+"|"+word
           reset()
           if (len(output)!=0):
            str1 = "Found in " + url +" "+ output
            str2 = str(df.loc[i,'Other'])
            str3 = str1 +  " | " + str2
            df.loc[i,'Other']=str3
            reset()
            return
            

        
                


        
        else:
          for l in links:
            print("looking at" + l)
            otherFiles(l,i)
    
    except:
        df.to_csv('OutPut_Others.csv', index=False)
        quit()
        



         




  
    

def adder(dataframe):
    for i in range(100 ,101):
        t_url=dataframe.loc[i,'URL']
        print(t_url)
        otherFiles(t_url,i)
        reset()
        
#adder(df)
#print(df)


#df.loc[0,'Other']=str(df.loc[0,'Other'])+ "Hey"


#df.to_csv('OutPut_Others.csv', index=False)  
#print(df.loc[0,'Other'])

# string = 'Found in https://github.com/openai/gen/blob/master/SECURITY_CONTACTS |violat | Found in https://github.com/openai/gen/blob/master/LICENSES |liab | Found in https://github.com/openai/gen/blob/master/openapi/custom_objects_spec.json |negative | Found in https://github.com/openai/gen/blob/master/openapi/openapi-generator/Dockerfile |trust | nan'

# a = re.search(r'\b(LICENSES)\b', string)
# print(a)


# #end_index= a.end()


# c = string[0:end_index+1]
# print(c)

# d =c.rindex('Found in')

# e = string[d:end_index+1]
# print(e)

# new_string = string.replace(e,"")
# print(new_string)



# for i in range(0 ,len(df)):
#     complete = 


#getting rid of the license field and putting it in a seperate field
for i in range(0,len(df)):
    complete = df.loc[i,'Other']
    try:
        if (re.search(r'\b(README)\b', complete))!= None:
         a = (re.search(r'\b(README)\b', complete))
         end_index_licence = a.end()
         first_half = complete[0:end_index_licence]
         # checking if the licencse field was the last entity
         second_half = complete[end_index_licence:len(complete)]
        if "Found in" in second_half:
            end_extract = second_half.index('Found in')
        else:
            end_extract = len(complete)
        start_index_license = first_half.rindex('Found in')
        first_half_extract = first_half[start_index_license:len(first_half)]
        second_half_extract = second_half[0:end_extract]
        extract = first_half_extract + second_half_extract
        #df.loc[i,'LICENSE']=extract
        new = complete.replace(extract,"")
        df.loc[i,'Other']=new
    except:
        continue


# for i in range(0,len(df)):
#     try:
#         raw = df.loc[i,'Links to other pages']
#         links = raw.split('|')
#         print(links)
#         for link in links:
#          if "#" in link or ".png" in link or ("https" not in link) or 'LICENSE' in link:
#             links.remove(link)
    
#         new_raw = ""
#         for r_link in links:
#             if '#' in r_link:
#                 continue
#             else:
#                 new_raw= "|" + r_link
           
#         df.loc[i,'Links to other pages']=new_raw
#     except:
#         continue
    
    

    


       


# for i in range(0,len(df)):
#     raw = str(df.loc[i,'Other'])
#     if raw !="":
#         try:
#              end_desired = raw.rindex('|')
#              print(end_desired)
#              cut_off = raw[end_desired+1:len(raw)]
#              new_raw = raw.replace(cut_off,"")
#              df.loc[i,'Other']= new_raw
#         except:
#             continue
       
    





    




df.to_csv('OutPut_Others.csv', index=False)






