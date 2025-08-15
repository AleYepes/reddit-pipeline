# Reddit data pipeline

## Directory Structure

```
/
├── .env                  # Store secrets (DB credentials)
├── .gitignore
├── .gitattribute
├── praw.ini              # PRAW credentials
├── requirements.txt
├── README.md
├── test.ipynb            # Quick test file
|
└── docs/
|
└── src/
    ├── config.py         # Loads and manages configuration from .env and other files.
    ├── database.py       # Handles all database connections, session management, and schema setup.
    ├── models.py         # Defines the database tables using SQLAlchemy ORM.
    ├── scraper.py        # The core logic for fetching data from Reddit via PRAW.
    └── main.py           # The main entry point to start the application.
```

## Relational Database Schema (PostgreSQL)

### **Table: `subreddits`**
Stores information about each community.

```sql
CREATE TABLE subreddits (
    id VARCHAR(10) PRIMARY KEY, -- Reddit's base36 ID, e.g., '2qh1i'
    name VARCHAR(255) NOT NULL UNIQUE, -- e.g., 'python'
    created_utc TIMESTAMPTZ NOT NULL,
    description TEXT,
    subscribers INTEGER,
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT NOW() -- When we last scraped this subreddit's info
);
```

### **Table: `posts`**
Stores each post/submission.

```sql
CREATE TABLE posts (
    id VARCHAR(10) PRIMARY KEY, -- e.g., 'fj4czk'
    title TEXT NOT NULL,
    selftext TEXT,
    created_utc TIMESTAMPTZ NOT NULL,
    score INTEGER NOT NULL,
    upvote_ratio REAL, -- e.g., 0.98
    num_comments INTEGER NOT NULL,
    url TEXT,
    author VARCHAR(255), -- Storing author name, can be '[deleted]'
    subreddit_id VARCHAR(10) NOT NULL REFERENCES subreddits(id),
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT NOW() -- When we last scraped this post
);
```
*   **Index:** Create an index on `subreddit_id` for faster lookups of posts within a community.

### **Table: `comments`**
Stores individual comments, preserving the tree structure.

```sql
CREATE TABLE comments (
    id VARCHAR(10) PRIMARY KEY,
    body TEXT NOT NULL,
    created_utc TIMESTAMPTZ NOT NULL,
    score INTEGER NOT NULL,
    author VARCHAR(255),
    post_id VARCHAR(10) NOT NULL REFERENCES posts(id),
    parent_id VARCHAR(20), -- Can be a post ID (t3_...) or a comment ID (t1_...)
    fetched_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```
*   **Indexes:** Create indexes on `post_id` and `parent_id` to dramatically speed up queries for retrieving comment trees.

## Core Application Logic & Fault Tolerance

### **Configuration (`src/config.py`)**
*   Use libraries like `python-dotenv` to load your database URL and other secrets from the `.env` file.
*   This keeps sensitive information out of your version-controlled code.

### **Database Module (`src/database.py` and `src/models.py`)**
*   **Use SQLAlchemy:** This Object-Relational Mapper (ORM) is the industry standard. It simplifies database interactions, helps prevent SQL injection, and manages a "connection pool" for efficient reuse of database connections.
*   **`models.py`:** Define your tables as Python classes (e.g., `class Post(Base): ...`). This makes your code more readable and Pythonic.
*   **`database.py`:**
    *   Contain the logic to create the database engine and session.
    *   Write functions like `insert_post_and_comments(session, post_data, comments_data)`.
    *   **Transactions are Key:** The function to insert a post and its comments should be atomic. It should all succeed or all fail together. SQLAlchemy's session object handles this automatically: you `add` all your objects and then call `session.commit()` once. If any error occurs before the commit, the transaction is rolled back.

### **The Scraper (`src/scraper.py`)**
This module's only job is to get data from Reddit. It shouldn't know anything about the database.

*   Initialize PRAW here.
*   Create a function like `fetch_posts_for_subreddit(subreddit_name, limit=100)` that returns a list of PRAW `Submission` objects.
*   Create a function `fetch_comments_for_post(submission)` that traverses the comment tree (your `linearize_tree` logic can be adapted here) and returns a flat list of PRAW `Comment` objects.
*   **Error Handling:** Wrap all PRAW calls in `try...except` blocks to handle Reddit-specific issues like `praw.exceptions.RedditAPIException` (for things like rate limits) or network errors.

### **The Main Controller (`src/main.py`)**
This is the orchestrator.

1.  **Initialize:** Set up logging, load configuration, and establish a database session.
2.  **Define Scope:** Create a list of target subreddits to scrape.
3.  **Main Loop:**
    ```python
    # (Simplified Pseudocode)
    for subreddit_name in TARGET_SUBREDDITS:
        log.info(f"Starting scrape for r/{subreddit_name}")
        try:
            posts = scraper.fetch_posts_for_subreddit(subreddit_name)
            for post in posts:
                # Check if post already exists and is recent enough to skip
                if database.post_exists_and_is_fresh(session, post.id):
                    log.info(f"Skipping post {post.id}, already processed.")
                    continue

                comments = scraper.fetch_comments_for_post(post)
                
                # Transform PRAW objects into a format for our database
                post_data, comments_data = transform_data(post, comments)

                # Insert everything in one transaction
                database.insert_post_and_comments(session, post_data, comments_data)
                log.info(f"Successfully inserted post {post.id} with {len(comments)} comments.")

        except Exception as e:
            log.error(f"Failed to process r/{subreddit_name}: {e}")
            session.rollback() # Ensure DB is clean after an error
    ```

## Making it Fault-Tolerant

*   **Idempotent Inserts:** Your script will fail and be restarted. To prevent creating duplicate rows, use PostgreSQL's `ON CONFLICT` clause. With SQLAlchemy, this is called `on_conflict_do_update` or `on_conflict_do_nothing`. When you try to insert a post with an ID that already exists, you can choose to either update its `score` and `num_comments` or simply do nothing.
    *   **Example:** `INSERT INTO posts (...) VALUES (...) ON CONFLICT (id) DO UPDATE SET score = EXCLUDED.score;`

*   **Robust Logging:** Use Python's built-in `logging` module. Configure it to write to both the console and a file (`scraper.log`). This is your number one tool for debugging what went wrong when the script was running unattended.

*   **Retry Mechanism:** For temporary network failures or API rate limiting, blindly failing isn't ideal. Use a library like `tenacity` to wrap your PRAW fetch functions with a retry decorator (e.g., `@retry(wait=wait_exponential(...), stop=stop_after_attempt(5))`). This will make your scraper automatically wait and try again.

By following this plan, you will build a scalable and resilient data pipeline that can run continuously, handle failures gracefully, and populate your database with clean, structured Reddit data.