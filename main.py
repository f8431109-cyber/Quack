from flask import Flask, Response
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route("/<subreddit>/comments")
def comments_feed(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/comments/.json?limit=10"
    headers = {"User-Agent": "rss-generator/0.2"}
    data = requests.get(url, headers=headers).json()
    
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = f"Reddit r/{subreddit} comments"
    
    for item in data["data"]["children"]:
        if item["kind"] == "t1":  # comments only
            comment = item["data"]

            post_title = comment.get("link_title", "Unknown Post")
            author = comment.get("author", "Unknown")
            body = comment.get("body", "Comment")
            link = "https://reddit.com" + comment.get("permalink", "")

            entry = ET.SubElement(channel, "item")
            ET.SubElement(entry, "title").text = post_title
            ET.SubElement(entry, "description").text = f'Comment by u/{author}: "{body}"'
            ET.SubElement(entry, "link").text = link
    
    xml_data = ET.tostring(rss, encoding="utf-8")
    return Response(xml_data, mimetype="application/rss+xml")

# Important: Replit runs on port 8080
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
