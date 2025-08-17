import logging
import praw
import datetime
from src.database import SessionLocal, init_db, insert_data
from src import scraper
from src.config import TARGET_SUBREDDITS, SUBMISSION_LIMIT


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)

def transform_praw_objects(subreddit, submissions, all_comments):
    subreddit_data = {
        'name': subreddit.name,
        'display_name': subreddit.display_name,
        'created_utc': datetime.datetime.fromtimestamp(subreddit.created_utc, tz=datetime.timezone.utc),
        'description': subreddit.public_description,
        'subscribers': subreddit.subscribers,
        'over_18': subreddit.over18,
    }

    submissions_data = []
    for submission in submissions:
        submissions_data.append({
            'name': submission.name,
            'title': submission.title,
            'selftext': submission.selftext,
            'created_utc': datetime.datetime.fromtimestamp(submission.created_utc, tz=datetime.timezone.utc),
            'score': submission.score,
            'upvote_ratio': submission.upvote_ratio,
            'num_comments': submission.num_comments,
            'url': submission.url,
            'author': submission.author.name if submission.author else '[deleted]',
            'subreddit_name': subreddit.name,
            'locked': submission.locked,
            'over_18': submission.over_18,
            'flair_text': submission.link_flair_text,
        })

    comments_data = []
    for comment in all_comments:
        comments_data.append({
            'name': comment.name,
            'body': comment.body,
            'created_utc': datetime.datetime.fromtimestamp(comment.created_utc, tz=datetime.timezone.utc),
            'score': comment.score,
            'author': comment.author.name if comment.author else '[deleted]',
            'submission_name': comment.link_id,
            'parent_name': comment.parent_id,
        })
    
    return subreddit_data, submissions_data, comments_data

def main():
    logging.info("Initializing database...")
    init_db()
    logging.info("Database initialized.")

    reddit = praw.Reddit('bot1')
    session = SessionLocal()

    for subreddit_name in TARGET_SUBREDDITS:
        logging.info(f"Starting scrape for r/{subreddit_name}")
        try:
            subreddit = scraper.fetch_subreddit(reddit, subreddit_name)
            submissions = scraper.fetch_submissions_for_subreddit(subreddit, limit=SUBMISSION_LIMIT)
            all_comments = []
            
            for i, submission in enumerate(submissions):
                logging.info(f"Fetching comments for submission {i+1}/{len(submissions)}: '{submission.title}' (id: {submission.id})")
                comments = scraper.fetch_comments_for_submission(submission)
                all_comments.extend(comments)

            logging.info(f"Transforming data for r/{subreddit_name}...")
            subreddit_data, submissions_data, comments_data = transform_praw_objects(subreddit, submissions, all_comments)

            logging.info(f"Inserting data for r/{subreddit_name} into database...")
            insert_data(session, subreddit_data, submissions_data, comments_data)
            
            session.commit()
            logging.info(f"Successfully scraped and saved data for r/{subreddit_name}.")

        except Exception as e:
            logging.error(f"An error occurred while processing r/{subreddit_name}: {e}", exc_info=True)
            session.rollback()
        
    session.close()
    logging.info("Scraping run finished.")

if __name__ == "__main__":
    main()
