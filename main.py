from flask import Flask, Response
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route("/<subreddit>/comments")
def comments_feed(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/comments/.json"
    headers = {"User-Agent": "rss-generator/0.1"}
    data = requests.get(url, headers=headers).json()
    
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = f"Reddit r/{subreddit} comments"
    
    for item in data["data"]["children"]:
        comment = item["data"]
        entry = ET.SubElement(channel, "item")
        ET.SubElement(entry, "title").text = comment.get("body", "Comment")
        ET.SubElement(entry, "link").text = "https://reddit.com" + comment.get("permalink", "")
    
    xml_data = ET.tostring(rss, encoding="utf-8")
    return Response(xml_data, mimetype="application/rss+xml")

# Important: Replit runs on its own port, don’t hardcode 3000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
