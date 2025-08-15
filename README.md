## Create a `praw.ini` file with your credentials
```ini
[bot1]
client_id=YOUR_CLIENT_ID
client_secret=YOUR_CLIENT_SECRET
username=YOUR_REDDIT_USERNAME
password=YOUR_REDDIT_PASSWORD
user_agent=AGENT_NAME by u/YOUR_USERNAME
```

## Install libs for notebooks + git

1. Install nbstripout to Remove Unnecessary Jupyter Metadata

```
pip install nbstripout
nbstripout --install
```

2. Use nbdime for Better Diffs and Merging

```
pip install nbdime
nbdime config-git --enable
```

To manually compare two notebook versions:

```
nbdiff notebook_1.ipynb notebook_2.ipynb
```

To resolve conflicts interactively:

```
nbmerge notebook.ipynb
```