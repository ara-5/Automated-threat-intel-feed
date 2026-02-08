from dotenv import load_dotenv
load_dotenv()  # This loads the .env file

import feedparser
import requests
import os
from openai import OpenAI
from datetime import datetime

# Configuration
KEYWORDS = ["zero-day", "ransomware", "breach", "exploit", "vulnerability", "malware"]
RSS_FEEDS = [
    "https://feeds.feedburner.com/TheHackersNews",
    "https://www.bleepingcomputer.com/feed/",
    "https://www.darkreading.com/rss.xml",
]

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def fetch_articles():
    """Fetch articles from RSS feeds"""
    articles = []
    for feed in RSS_FEEDS:
        try:
            parsed = feedparser.parse(feed)
            for entry in parsed.entries[:5]:
                articles.append({
                    "title": entry.title,
                    "link": entry.link,
                    "summary": entry.get("summary", "")
                })
            print(f"✓ Fetched {len(parsed.entries[:5])} articles from {feed}")
        except Exception as e:
            print(f"✗ Error fetching {feed}: {e}")
    return articles

def filter_articles(articles):
    """Filter articles by threat keywords"""
    filtered = []
    for article in articles:
        content = (article["title"] + article["summary"]).lower()
        if any(keyword in content for keyword in KEYWORDS):
            filtered.append(article)
    return filtered

def summarize(articles):
    """Generate AI summary of filtered articles"""
    if not articles:
        return "No major cybersecurity threats detected today. ✅"
    
    # Format articles with links
    text = "\n\n".join([
        f"Title: {a['title']}\nLink: {a['link']}\nSummary: {a['summary'][:200]}..."
        for a in articles
    ])
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a cybersecurity analyst. Create a brief summary (150 words) of the main threats, then list each article title with its link in markdown format."
                },
                {"role": "user", "content": text}
            ],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"✗ OpenAI error: {e}")
        return "Error generating summary. Check logs."

def send_to_discord(message):
    """Post summary to Discord channel"""
    MAX_LENGTH = 1900
    
    if len(message) > MAX_LENGTH:
        message = message[:MAX_LENGTH] + "\n\n... (truncated)"
    
    try:
        payload = {
            "content": f"🛡️ **Daily Threat Intel Report - {datetime.now().strftime('%B %d, %Y')}**\n\n{message}"
        }
        response = requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
        response.raise_for_status()
        print("✓ Successfully sent to Discord")
    except Exception as e:
        print(f"✗ Discord error: {e}")

def main():
    """Main automation workflow"""
    # Validate environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY not set")
        return
    
    if not os.getenv("DISCORD_WEBHOOK"):
        print("❌ ERROR: DISCORD_WEBHOOK not set")
        return
    
    print(f"\n{'='*60}")
    print(f"🤖 Threat Intel Automation - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # Execute workflow
    articles = fetch_articles()
    print(f"\n📰 Total articles fetched: {len(articles)}")
    
    filtered = filter_articles(articles)
    print(f"🎯 Threat-related articles: {len(filtered)}")
    
    if filtered:
        print("\n🔍 Filtered Articles:")
        for a in filtered:
            print(f"  • {a['title']}")
    
    summary = summarize(filtered)
    print(f"\n📝 Generated Summary:\n{summary}\n")
    
    send_to_discord(summary)
    
    print(f"\n{'='*60}")
    print("✅ Automation Complete")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()