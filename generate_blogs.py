#!/usr/bin/python
import markdown
from pathlib import Path
import time
import datetime

class Post:
    def __init__(self, markdownFile):
        line1 = markdownFile.readline()
        line2 = markdownFile.readline()
        self.title = line2.replace("# ", "").replace("\n", "")
        self.pageName = self.title.replace(" ", "_").replace("?", "").replace("!", "").replace(".", "").lower()
        dateString = line1.replace("## ", "").replace("\n", "")
        try:
            self.date = datetime.datetime.strptime(dateString, "%B %d, %Y")
        except:
            raise Exception("Fix ya dates in \"" + self.title + "\"! Ya dummy!")
        markdownFile.seek(0)
        wholeFile = markdownFile.read()
        self.html = markdown.markdown(wholeFile)


class Blog:
    def __init__(self, rawDirectory, rawWebsiteLocation, imagesDirectory, finishedDirectory, finishedWebsiteLocation):
        self.rawDirectory = rawDirectory;
        self.rawWebsiteLocation = rawWebsiteLocation;
        self.imagesDirectory = imagesDirectory;
        self.finishedDirectory = finishedDirectory;
        self.finishedWebsiteLocation = finishedWebsiteLocation;
    def generate_blog(self):
        print("\tSearching for files in " + self.rawDirectory)
        matchRawBlogPostFiles = Path(self.rawDirectory).rglob('*')
        rawBlogPostFilenames = [x for x in matchRawBlogPostFiles]
        formattedPosts = []
        for rawBlogPostFilename in rawBlogPostFilenames:
            print("\t\tOpening file " + str(rawBlogPostFilename))
            rawBlogPostFile = open(rawBlogPostFilename, "r")
            thisPost = Post(rawBlogPostFile)
            formattedPosts.append(thisPost)
        print("\tSorting posts by date")
        formattedPosts.sort(key=lambda x: x.date, reverse=True)

        print("\tGenerating links sidebar")
        links = ""
        for post in formattedPosts:
            links += "<li><a href=\"/posts/" + post.pageName + ".html\">" + post.title + "</a></li>\n" # CHEATING ON THIS LINE W/ /POSTS

        print("\tOpening template page")
        templateFile = open(self.rawWebsiteLocation, "r")
        template = templateFile.read()
        finishedWebsite = template
        print("\tGenerating individual post pages")
        for post in formattedPosts:
            print("\t\tGenerating post \"" + post.title + "\" at " + self.finishedDirectory + post.pageName + ".html")
            newPostFile = open(self.finishedDirectory + post.pageName + ".html", "w")
            finishedWebsite = finishedWebsite.replace("POSTSGOHERE", post.html + "\n POSTSGOHERE")
            fullyFormattedPost = template.replace("POSTSGOHERE", post.html).replace("LINKSGOHERE", links)
            newPostFile.write(fullyFormattedPost)
            newPostFile.close()
        print("\tGenerating main posts page")
        finishedWebsite = finishedWebsite.replace("POSTSGOHERE", "").replace("LINKSGOHERE", links)
        finishedWebsiteFile = open(self.finishedWebsiteLocation, "w")
        finishedWebsiteFile.write(finishedWebsite)
        finishedWebsiteFile.close()


general = Blog("www/raw_posts/", "www/raw_index.html", "www/images/", "www/posts/", "www/index.html")
blogList = [general]

for blog in blogList:
    print("Generating blog at " + blog.finishedDirectory)
    blog.generate_blog()
    print("Blog at " + blog.finishedDirectory + " successfully generated")
