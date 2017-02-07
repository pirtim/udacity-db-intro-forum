from __future__ import print_function
#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach

## Database connection
## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    conn = psycopg2.connect("dbname=forum")
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts;")
    posts_db = cur.fetchall()
    posts = [{'content': post[1], 'time': post[2]} for post in posts_db]
    posts.sort(key=lambda row: row['time'], reverse=True)
    conn.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    conn = psycopg2.connect("dbname=forum")
    cur = conn.cursor()
    sanitized_content = bleach.clean(content)
    cur.execute("INSERT INTO posts (content) VALUES(%s);", (sanitized_content,))
    conn.commit()

    if sanitized_content != content:
        last_post = _GetLastPost(cur)
        last_post_id = last_post[0]

        conn_bad = psycopg2.connect("dbname=forum")
        cur_bad = conn_bad.cursor()
        cur_bad.execute("INSERT INTO posts_bad (id, unsanitized_content) VALUES(%s, %s);", 
            (last_post_id, content))
        conn_bad.commit()
        conn_bad.close()

    conn.close()

def _GetLastPost(cursor):
    cursor.execute("SELECT * FROM posts ORDER BY time DESC LIMIT 1;")
    return cursor.fetchone()
