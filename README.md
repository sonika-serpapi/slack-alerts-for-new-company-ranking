# Build a Slack Bot That Alerts You When a New Company Ranks for Keywords
In this tutorial, we’ll build a simple system that detects when a new brand ranks for a tracked keyword and send an alert to a Slack channel.

Code examples for blog post: https://serpapi.com/blog/build-a-slack-bot-that-alerts-you-when-a-new-company-ranks-for-keywords/

## Getting Started

To start, you’ll need a SerpApi account, a Slack workspace (and a Slack Incoming Webhook URL), and Python installed.

### Create a Slack Webhook
1. Go to Slack → Apps
2. Search for Incoming Webhooks
3. Create a webhook for your channel

You will get a Webhook URL like: https://hooks.slack.com/services/XXXX/XXXX/XXXX

Save this, as we'll need it later.

### Code Related Setup Steps

1. Install SerpApi's new Python serpapi library, the python-dotenv library, tldextract library (for parsing the domains from URLs), and the schedule library in your environment:

```
pip install serpapi python-dotenv schedule tldextract
```

2. To begin scraping data, create a free account on serpapi.com. You'll receive 250 free search credits each month to explore the API. Get your SerpApi API Key from this page.

3. [Optional but Recommended] Set your API key in an environment variable, instead of directly pasting it in the code. Refer here to understand more about using environment variables. For this tutorial, I have saved the API key in an environment variable named "SERPAPI_API_KEY" in my .env file.

4. [Optional but Recommended] Set up your Slack Webhook URL as an an environment variable as well. In your .env file, this will look like this:

```
SERPAPI_API_KEY=<YOUR PRIVATE API KEY>
SLACK_WEBHOOK_URL=<YOUR PRIVATE WEBHOOK URL>
```
5. Set constants as needed in the code file `get_companies_ranking_for_keywords.py`:
```
SERPAPI_KEY = os.environ["SERPAPI_API_KEY"]  -> Set the environment variable OR replace with your API key if you're not using environment variables
queries = [] # List of queries for which you want to find the updated domains
DB_FILE = "known_domains.json"
SLACK_WEBHOOK = os.environ["SLACK_WEBHOOK_URL"] -> Set the environment variable OR replace with your API key if you're not using environment variables
```

## Run The Code

Head to the project folder and run the code file using `python get_companies_ranking_for_keywords.py`

This will start the scheduler. To keep the tasks running even after you close your terminal or IDE, you can choose to run the script as a persistent background process. For linux/macOS, use `disown` to detach the script from the terminal, e.g., `python3 script.py & disown`.

If you want to just test your implementation, comment the scheduler related lines and just add a line to call the `check_for_new_domains()` function. 

## Sample Output

I ran the code twice with QUERY_LIST = ["ai images tool", "ai image generators", "image creation ai tools"]

The first time, I got some new pages (because a few new companies started ranking for the queries since when I ran it last)
The next time, since all the webpages were already seen, I got a message letting me know that no new pages were detected.

These were the alerts I received:

<img width="1112" height="988" alt="image" src="https://github.com/user-attachments/assets/90f15bd3-9cff-484e-9b6c-4a79f2a450ec" />

You can use this to instantly find out when new companies start ranking for important keywords that matter for your brand. 
