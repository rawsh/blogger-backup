''' Program by Robert Washbourne http://devpy.me robert@devpy.me'''

from BeautifulSoup import BeautifulSoup #find images src and replace
import os.path #for relative paths
import urllib #for downloading, of course
import json #parse blogger json
import ssl #bullshit ssl hack for encrypted blogs
import os #make directories

#bullshit ssl hack
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print "Getting info on blog"

#change these values
attribution = True #displays a message with my name at the bottom of downloaded posts
max_results = 99999 #max number of posts to backup
blogurl = "yourblog.blogspot.com" #url of your blogger blog. no "http://". CHANGE THIS


url = "http://" + blogurl + "/feeds/posts/default?orderby=published&max-results="+str(max_results)+"&alt=json" #max-posts is how many this parses.
response = urllib.urlopen(url)
response = json.loads(response.read()) #read blog feed

print "Viewing post feed"

def DownloadImages(feed):
    ''' Download images from blogger given feed'''

    print "Downloading images, "+str(len(feed["entry"]))+" total posts."

    for entry in feed["entry"]: #for each entry in the json file
        print "Parsing images in " + entry["title"]["$t"].encode('ascii', 'ignore')

        if os.path.exists(os.getcwd()+"/"+feed["title"]["$t"]+" Backup"+"/images/"+entry["title"]["$t"]):
          print entry["title"]["$t"].encode("utf8") + " folder exists, skipping" #skip the entry if downloaded
        else:
            os.makedirs(os.getcwd()+"/"+feed["title"]["$t"]+" Backup"+"/images/"+entry["title"]["$t"])

            html = BeautifulSoup(entry["content"]["$t"]) #find images to download
            images = html.findAll('img')

            for i in range(len(images)):
                print "Downloaded " + str(i) + " out of " + str(len(images)) #download images
                urllib.urlretrieve(images[i]["src"], os.getcwd()+"/"+feed["title"]["$t"]+" Backup"+"/images/"+entry["title"]["$t"]+"/"+entry["author"][0]["name"]["$t"]+"_"+str(i)+".jpg", context=ctx)

def DownloadArticles(feed):
    ''' Download articles from blogger given feed'''

    print "Downloading articles, "+str(len(feed["entry"]))+" total posts."

    styles = '''<style>
                body {
                    padding: 50px;
                    max-width: 900px;
                    margin: auto;
                    font-size: 16px;
                }
                img {
                    display: block;
                }
              </style>'''.encode("utf8") #styles for downloaded viewing

    index = open(os.getcwd()+"/"+feed["title"]["$t"]+" Backup/index.html","w")
    index.truncate()
    index.write(styles)

    for entry in feed["entry"]: #for each entry in json
        index.write("<a href=\""+"./"+entry["title"]["$t"].encode("utf8")+".html\">"+entry["title"]["$t"].encode("utf8")+"</a><br/>")
        if os.path.isfile(os.getcwd()+"/"+feed["title"]["$t"]+" Backup/"+entry["title"]["$t"]+".html"): #skip if exists
            print entry["title"]["$t"] + " html exists, skipping"
        else:
            print "Downloading html from " + entry["title"]["$t"].encode("utf8")

            html = BeautifulSoup(entry["content"]["$t"])
            images = html.findAll('img')

            for i in range(len(images)): #replace src
                images[i]["src"] = "./images/"+entry["title"]["$t"]+"/"+entry["author"][0]["name"]["$t"]+"_"+str(i)+".jpg"

            target = open(os.getcwd()+"/"+feed["title"]["$t"]+" Backup/"+entry["title"]["$t"]+".html","ab")
            target.truncate()
            target.write(styles)
            target.write(html.prettify())
            if attribution:
                target.write("\n\n\n<hr><br>Blogger backup created by <a href='http://www.devpy.me'>Robert Washbourne</a>") #attribution
            target.close()

    if attribution:
        index.write("\n\n\n<hr><br>Blogger backup created by <a href='http://www.devpy.me'>Robert Washbourne</a>") #attribution
    index.close()

def PrintAllPosts(feed):
    ''' Grab blogger url feed and get ready for backup'''

    DownloadImages(feed["feed"]) #downloads images
    DownloadArticles(feed["feed"]) #downloads articles (just the text)

PrintAllPosts(response) #main loop
