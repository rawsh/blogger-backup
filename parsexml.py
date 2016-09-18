from BeautifulSoup import BeautifulSoup
from gdata import service
import urllib
import shutil
import gdata
import atom
import os

print "Logging in"

blogger_service = service.GDataService('rawashbourne@gmail.com', 'idog021)')
blogger_service.source = 'exampleCo-exampleApp-1.0'
blogger_service.service = 'blogger'
blogger_service.account_type = 'GOOGLE'
blogger_service.server = 'www.blogger.com'
blogger_service.ProgrammaticLogin()

print "Viewing post feed"

def PrintAllPosts(blogger_service, blog_id, max_results='99999'):
  query = service.Query()
  query.feed = '/feeds/' + blog_id + '/posts/default'
  query.max_results = max_results
  feed = blogger_service.Get(query.ToUri())

  if os.path.exists(os.getcwd()+"/"+feed.title.text+" Backup"):
      shutil.rmtree(os.getcwd()+"/"+feed.title.text+" Backup")
  os.mkdir(os.getcwd()+"/"+feed.title.text+" Backup")

  os.makedirs(os.getcwd()+"/"+feed.title.text+" Backup"+"/images/")

  for entry in feed.entry:
      print "Parsing images in " + entry.title.text
      os.makedirs(os.getcwd()+"/"+feed.title.text+" Backup"+"/images/"+entry.title.text)

      html = BeautifulSoup(entry.content.text)
      images = html.findAll('img')

      for i in range(len(images)):
          print "Downloaded " + str(i) + " out of " + str(len(images))
          urllib.urlretrieve(images[i]["src"], os.getcwd()+"/"+feed.title.text+" Backup"+"/images/"+entry.title.text+"/"+images[i]["src"].split('/')[-1])

PrintAllPosts(blogger_service, "912431127682594831")
