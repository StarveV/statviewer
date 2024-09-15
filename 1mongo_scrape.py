import pymongo
from pymongo import MongoClient
import asyncpraw
import datetime
import time
import asyncio

# settings for accessing MongoDB
client = MongoClient("mongodb+srv://starvevader:Aw255423@cluster0.lcwom3q.mongodb.net/?retryWrites=true&w=majority")
db = client["heatmap"]
collection = db["wsb_scrape"] 

# drop previous entry
collection.drop()

# Set the range of reddit post to scrape
no_days = 7
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=no_days)


# Time out for one request
timeout_time = 30

# Additional trial after not finding new submission
max_additional_trial = 10


async def make_request(scraped_post_ids, start_date, end_date):
    # Create an async PRAW client
    reddit = asyncpraw.Reddit(client_id='tIxG7ddAYJ-gqYMqju5aPw', client_secret='1VgZYIHZ4W8vHcBm03E2mbe089zwFA', user_agent='wsb.heatmap', timeoout = timeout_time)

    # Set a flag to track whether any new submissions have been found
    found_new_submission = False

    no_new_submissions_counter = 0

    # Retrieve a list of submissions in the subreddit
    subreddit = await reddit.subreddit("wallstreetbets")

    # Iterate over the submissions using the async for loop
    async for submission in subreddit.new(limit=None):
        # Convert the timestamp to a datetime object
        timestamp = datetime.datetime.fromtimestamp(submission.created_utc)
        
        # Check if the submission was made in the past `no_days` days from the start date
        if (start_date <= timestamp ):
            # Check if the submission has already been scraped
            if submission.id not in scraped_post_ids and timestamp <= end_date:
                # If the submission has not been scraped, add its ID to the list
                scraped_post_ids.append(submission.id)
                print (timestamp, submission.title )

                # Set the flag to True, to indicate that a new submission has been found
                found_new_submission = True
                # Add the data to the collection
                collection.insert_one({
                    "date": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "title": submission.title,
                    "score": submission.score,
                    "post body": submission.selftext,
                    "number of comments": submission.num_comments
                })
            else:
                # If the submission has already been scraped, do not scrape it again
                continue
        else:
            # If no new submissions are found, check the value of the flag
            if not found_new_submission:
                no_new_submissions_counter += 1
                
                if no_new_submissions_counter >= max_additional_trial:
                # If the maximum number of tries have been reached, break the loop
                    print (f'No new submission counter: {no_new_submissions_counter}')
                    break # If the flag is still False, exit the loop

    # Close the client session
    await reddit.close()

async def main_task():
    # Create an empty list to store the ID of the scraped submissions
    scraped_post_ids = []
    # Call the `make_request` function
    await make_request(scraped_post_ids, start_date, end_date)

# Start the timer
start_time = time.perf_counter()

# Create an event loop
loop = asyncio.get_event_loop()
# Run the main_task function
loop.run_until_complete(main_task())

#close the mongoDB client
client.close()

# Stop the timer
end_time = time.perf_counter()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print(f'Elapsed time: {elapsed_time:0.4f} seconds')