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
    ET.SubElement(channel, "title").text = f"Reddit r/{subreddit} - Latest Comments"

    for item in data["data"]["children"]:
        post = item["data"]

        # Build an entry for each submission (post)
        post_title = post.get("title", "Untitled Post")
        post_link = "https://reddit.com" + post.get("permalink", "")
        submission_id = post.get("id")

        # Fetch the comments for this submission
        comments_url = f"https://www.reddit.com/r/{subreddit}/comments/{submission_id}.json?limit=5"
        comments_data = requests.get(comments_url, headers=headers).json()

        if len(comments_data) < 2:
            continue  # skip if no comments section

        comments = comments_data[1]["data"]["children"]

        for c in comments:
            if c["kind"] != "t1":  # only process actual comments
                continue

            comment = c["data"]
            comment_body = comment.get("body", "[deleted]")
            comment_link = "https://reddit.com" + comment.get("permalink", "")

            parent_id = comment.get("parent_id", "")
            if parent_id.startswith("t3_"):
                parent_type = "Post"
            else:
                parent_type = "Comment"

            entry = ET.SubElement(channel, "item")
            ET.SubElement(entry, "title").text = f"Comment on: {post_title}"
            ET.SubElement(entry, "link").text = comment_link
            ET.SubElement(entry, "description").text = (
                f"<b>Parent:</b> {parent_type}<br/>"
                f"<b>Post:</b> {post_title}<br/><br/>"
                f"{comment_body}"
            )

    xml_data = ET.tostring(rss, encoding="utf-8")
    return Response(xml_data, mimetype="application/rss+xml")

# Replit requires this host/port
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
