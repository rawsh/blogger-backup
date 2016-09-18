import urllib, urllib2, json, os,shutil

from BeautifulSoup import BeautifulSoup
url = "http://washbourne.blogspot.com/feeds/posts/default?orderby=published&max-results=999&alt=json"
# url = "http://washbourne.blogspot.com/feeds/posts/default?orderby=published&max-results=999&alt=json&key=AIzaSyCX7XYXCAqUu2uVPqE0nGQCBJCtvprBUf8"

response = urllib2.urlopen(url)
data = json.loads(response.read())

print("Read json")

datalen = len(data.get("feed"))

urls = [data.get("feed")[x] for x in range(datalen)]

print("Got post urls")

# for x in range(datalen):
#     print "Find and replace html (for offline images) of " + str(urls[x])
#     originalSoup = BeautifulSoup(urllib2.urlopen(urls[x]))
#     cleanSoup = BeautifulSoup(str(originalSoup).replace("<br/>", replaceString))

images = []
for x in range(datalen):
    print "Parsing images in  " + str(urls[x])
    html = BeautifulSoup(urllib2.urlopen(urls[x]))
    images.append(html.findAll('img'))
    # page = urls[0].split('/')[-1].split('.')[0]


print("Downloading images")

if os.path.exists(os.getcwd()+"/images"):
    shutil.rmtree(os.getcwd()+"/images")
os.mkdir(os.getcwd()+"/images")

for x in range(datalen):
    print("Starting page "+ str(x+1)+" out of "+ str(datalen))
    page = urls[0].split('/')[-1].split('.')[0]
    os.makedirs(os.getcwd()+"/images/"+page)

    for a in range(len(images[x])):
        print("Downloaded image "+str(a+1)+" out of "+ str(len(images[x])))
        urllib.urlretrieve(images[x][a]["src"], os.getcwd() + "/images/"+page+"/"+images[x][a]["src"].split('/')[-1])

print("Done! Enjoy your backup.")
