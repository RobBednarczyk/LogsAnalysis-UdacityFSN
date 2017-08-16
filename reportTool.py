#!/bin/env python2.7

"""
The scope of this script is to connect to a database and to extract and
analyze the data inside it. The tool will provide answers to the following
questions:

1) What are the most popular three articles of all time?
2) Who are the most popular article authors of all time?
3) On which days did more than 1 percent of the requests lead to errors?
"""

# create a clickedArticles view
# CREATE VIEW clickedArticles as
# SELECT (regexp_matches(path, '/article/(.*$)'))[1] as slug,
# ip, method, status, time, id
# FROM log;

# create an allArticleInfo VIEW
# CREATE VIEW allArticleInfo AS
# SELECT articles.title, clickedArticles.slug, clickedArticles.ip,
# clickedArticles.status, clickedArticles.time, authors.name
# FROM articles JOIN clickedArticles
# ON articles.slug = clickedArticles.slug
# JOIN authors on articles.author = authors.id;

# CREATE VIEW dailyErrors AS
# SELECT to_char(time, 'Month DD, YYYY') as day, count(*) as items
# FROM log
# WHERE status = '404 NOT FOUND'
# GROUP by day;

# CREATE VIEW dailyOKs as
# SELECT to_char(time, 'Month DD, YYYY') as day, count(*) as items
# FROM log
# WHERE status = '200 OK'
# GROUP BY day;

# first question query:

# SELECT title, count(*) as totViews from allArticleInfo
# GROUP BY title
# ORDER BY totViews DESC
# LIMIT 3;

# second question query:

# SELECT name, count(*) as totViews from allArticleInfo
# GROUP BY name
# ORDER BY totViews DESC;

# third question query:

# SELECT dailyErrors.day,
# round(100.0 * (dailyErrors.items::numeric/dailyOKs.items), 1) as percError
# FROM dailyErrors join dailyOKs
# ON dailyErrors.day = dailyOKs.day
# WHERE (dailyErrors.items::numeric/dailyOKs.items) > 0.01;

# change date formatting:
# select to_char(time, 'Month DD, YYYY') from allArticleInfo;

import psycopg2

DBNAME = "news"

top3ArticlesQuery = """
SELECT title, count(*) as totViews from allArticleInfo
group by title
order by totViews DESC
limit 3;
"""

topAuthorsQuery = """
SELECT name, count(*) as totViews from allArticleInfo
group by name
order by totViews DESC;
"""

errPercentageQuery = """
SELECT dailyErrors.day,
round(100.0 * (dailyErrors.items::numeric/dailyOKs.items), 1) as percError
FROM dailyErrors join dailyOKs
ON dailyErrors.day = dailyOKs.day
WHERE (dailyErrors.items::numeric/dailyOKs.items) > 0.01;
"""


def connect(database_name=DBNAME):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Connection Error. Please retry.")


def top3Articles():
    """Return the top three articles with the most views"""
    # connect to the database and create a cursor
    db, cursor = connect()
    cursor.execute(top3ArticlesQuery)
    return cursor.fetchall()
    db.close()


def topAuthors():
    """Return the list of the authors whose articles had the most views"""
    # connect to the database and create a cursor
    db, cursor = connect()
    cursor.execute(topAuthorsQuery)
    return cursor.fetchall()
    db.close()


def errPercentage():
    """Return the days in which the error percentage is higher than 1.0"""
    # connect to the database and create the cursor
    db, cursor = connect()
    cursor.execute(errPercentageQuery)
    return cursor.fetchall()
    db.close()


if __name__ == "__main__":

    print("---------------THE QUERY RESULTS---------------")
    print("")
    print("1. What are the most popular three articles of all time?")
    print("")
    for article in top3Articles():
        print(article[0] + " - " + str(article[1]) + " views")
    print("")
    print("2. Who are the most popular article authors of all time? ")
    print("")
    for author in topAuthors():
        print(author[0] + " - " + str(author[1]) + " views")
    print("")
    print("3. On which days did more than 1% of requests lead to errors?")
    print("")
    for day in errPercentage():
        print(str(day[0]) + " - " + str(day[1]) + "% errors")
