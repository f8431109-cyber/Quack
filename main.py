@app.route("/comments")
def comments_feed():
    url = "https://www.reddit.com/r/artificial/comments/.json"
    headers = {"User-Agent": "rss-generator/0.1"}
    data = requests.get(url, headers=headers).json()

    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "Reddit r/artificial comments"
    
    for item in data["data"]["children"]:
        comment = item["data"]
        entry = ET.SubElement(channel, "item")
        ET.SubElement(entry, "title").text = comment.get("body", "Comment")
        ET.SubElement(entry, "link").text = "https://reddit.com" + comment.get("permalink", "")
    
    xml_data = ET.tostring(rss, encoding="utf-8")
    return Response(xml_data, mimetype="application/rss+xml")
