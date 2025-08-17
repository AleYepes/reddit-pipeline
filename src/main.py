
import logging
import datetime
from src.database import SessionLocal, init_db, insert_data
from src import scraper
from src.config import TARGET_SUBREDDITS, POST_LIMIT

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)

def transform_praw_objects(subreddit, posts, all_comments):
    """Transforms PRAW objects into dictionaries for database insertion."""
    subreddit_data = {
        'id': subreddit.id,
        'name': subreddit.display_name,
        'created_utc': datetime.datetime.fromtimestamp(subreddit.created_utc, tz=datetime.timezone.utc),
        'description': subreddit.public_description,
        'subscribers': subreddit.subscribers
    }

    posts_data = []
    for post in posts:
        posts_data.append({
            'id': post.id,
            'title': post.title,
            'selftext': post.selftext,
            'created_utc': datetime.datetime.fromtimestamp(post.created_utc, tz=datetime.timezone.utc),
            'score': post.score,
            'upvote_ratio': post.upvote_ratio,
            'num_comments': post.num_comments,
            'url': post.url,
            'author': post.author.name if post.author else '[deleted]',
            'subreddit_id': subreddit.id
        })

    comments_data = []
    for comment in all_comments:
        comments_data.append({
            'id': comment.id,
            'body': comment.body,
            'created_utc': datetime.datetime.fromtimestamp(comment.created_utc, tz=datetime.timezone.utc),
            'score': comment.score,
            'author': comment.author.name if comment.author else '[deleted]',
            'post_id': comment.submission.id,
            'parent_id': comment.parent_id
        })
    
    return subreddit_data, posts_data, comments_data

def main():
    logging.info("Initializing database...")
    init_db()
    logging.info("Database initialized.")

    session = SessionLocal()

    for subreddit_name in TARGET_SUBREDDITS:
        logging.info(f"Starting scrape for r/{subreddit_name}")
        try:
            subreddit = scraper.fetch_subreddit(subreddit_name)
            posts = scraper.fetch_posts_for_subreddit(subreddit, limit=POST_LIMIT)
            all_comments = []
            
            for i, post in enumerate(posts):
                logging.info(f"Fetching comments for post {i+1}/{len(posts)}: '{post.title}' (id: {post.id})")
                comments = scraper.fetch_comments_for_post(post)
                all_comments.extend(comments)

            logging.info(f"Transforming data for r/{subreddit_name}...")
            subreddit_data, posts_data, comments_data = transform_praw_objects(subreddit, posts, all_comments)

            logging.info(f"Inserting data for r/{subreddit_name} into database...")
            insert_data(session, subreddit_data, posts_data, comments_data)
            
            session.commit()
            logging.info(f"Successfully scraped and saved data for r/{subreddit_name}.")

        except Exception as e:
            logging.error(f"An error occurred while processing r/{subreddit_name}: {e}", exc_info=True)
            session.rollback()
        
    session.close()
    logging.info("Scraping run finished.")

if __name__ == "__main__":
    main()
