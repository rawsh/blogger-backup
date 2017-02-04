# Blogger Backup

Backs up your blog from blogger using python.

This will download all posts as simple html (without website markup) and all images, then point the local posts to the local images. This will help you get past the (bull)shit that google does with their images service (e.g. converts to webp, downsizes, has weird urls etc.)

### How to use:

- Download with `git clone https://github.com/rawsh/blogger-backup.git` or with the [Releases Page.](https://github.com/rawsh/blogger-backup/releases)
- Edit `backupBlogger.py` and change the blogurl variable on line 20.
- The program pulls the name of your blog from blogspot. `${Blog Name}`
- Run the program
- The image files will show in `./${Blog Name} Backup/images` and the html will be in `./${Blog Name} Backup`.
- Open `./${Blog Name} Backup/index.html` in a browser to get a list of links to downloaded posts.

Inspired by broken wget that wouldn't download external recourses, and screwed up all the folders.
