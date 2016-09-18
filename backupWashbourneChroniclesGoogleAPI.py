''' Program by Robert Washbourne http://devpy.me robert@devpy.me'''

from BeautifulSoup import BeautifulSoup
from gdata import service
import os.path
import urllib
import shutil
import gdata
import atom
import os

print "Logging in"

blogger_service = service.GDataService('', '')
blogger_service.service = 'blogger'
blogger_service.account_type = 'GOOGLE'
blogger_service.server = 'www.blogger.com'
blogger_service.ProgrammaticLogin()

attribution = True
blogurl = "washbourne.blogspot.com"

print "Viewing post feed"

def DownloadImages(feed):
    ''' Download images from blogger given feed'''

    print "Downloading images"

    if os.path.exists(os.getcwd()+"/"+feed.title.text+" Backup/"):
      shutil.rmtree(os.getcwd()+"/"+feed.title.text+" Backup/")
    os.mkdir(os.getcwd()+"/"+feed.title.text+" Backup/")
    os.mkdir(os.getcwd()+"/"+feed.title.text+" Backup/images")

    for entry in feed.entry:
        print "Parsing images in " + entry.title.text
        os.makedirs(os.getcwd()+"/"+feed.title.text+" Backup"+"/images/"+entry.title.text)

        html = BeautifulSoup(entry.content.text.decode('utf-8', 'ignore'))
        images = html.findAll('img')

        for i in range(len(images)):
            print "Downloaded " + str(i) + " out of " + str(len(images))
            urllib.urlretrieve(images[i]["src"], os.getcwd()+"/"+feed.title.text+" Backup"+"/images/"+entry.title.text+"/"+entry.author[0].name.text+"_"+str(i)+".jpg")

def DownloadArticles(feed):
    ''' Download articles from blogger given feed'''

    print "Downloading articles"

    styles = "<style>\
    body {\
    padding: 50px;\
    max-width: 900px;\
    margin: auto;\
    font-size: 16px;\
    }\
    img { \
    display: block; \
    }\
  </style>\n"

    index = open(os.getcwd()+"/"+feed.title.text+" Backup/index.html","w")
    index.truncate()
    index.write(styles)

    for entry in feed.entry:
        index.write("<a href=\""+"./"+entry.title.text+".html\">"+entry.title.text+"</a><br/>")
        if os.path.isfile(os.getcwd()+"/"+feed.title.text+" Backup/"+entry.title.text+".html"):
            print entry.title.text + " html exists, skipping"
        else:
            print "Downloading html from " + entry.title.text

            html = BeautifulSoup(entry.content.text.decode('utf-8'))
            images = html.findAll('img')

            for i in range(len(images)):
                images[i]["src"] = "./images/"+entry.title.text+"/"+entry.author[0].name.text+"_"+str(i)+".jpg"

            target = open(os.getcwd()+"/"+feed.title.text+" Backup/"+entry.title.text+".html","ab")
            target.truncate()
            target.write(styles)
            target.write(html.prettify())
            target.write("\n\n\n<br>Blogger backup created by <a href='http://www.devpy.me'>Robert Washbourne</a>")
            target.close()

    index.write("\n\n\n<br>Blogger backup created by <a href='http://www.devpy.me'>Robert Washbourne</a>")
    index.close()

def PrintAllPosts(blogger_service, blog_id, max_results='99999'):
    ''' Grab blogger url feed and get ready for backup'''

    query = service.Query()
    query.feed = '/feeds/' + blog_id + '/posts/default'
    query.max_results = max_results
    feed = blogger_service.Get(query.ToUri())

    #DownloadImages(feed)
    DownloadArticles(feed)



PrintAllPosts(blogger_service, "912431127682594831")
