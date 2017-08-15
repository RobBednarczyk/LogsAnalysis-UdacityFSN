# "News" database reporting tool

## General remarks

This python script provides a tool to answer three questions about the data
inside the "News" database. In particular:

1) What are the most popular three articles of all time?
2) Who are the most popular article authors of all time?
3) On which days did more than 1 percent of the requests lead to errors?

## System requirements

In order to run the program users must install the PostgreSQL database
server on their computer. Next they need to load the database which is included
in the newsdata.sql file.

## Database modifications

The code in the reportTool.py file relies on several views that have been
created on top of the original "news" database tables. In particular users
should run the following SQL code while connected to the database:

I assumed that the root path "/" is not a valid article
Valid articles' paths have the following format: "/articles/somePath"

CREATE VIEW clickedArticles AS
SELECT (regexp_matches(path, '/article/(.*$)'))[1] as slug,
ip, method, status, time, id
FROM log;

CREATE VIEW allArticleInfo AS
SELECT articles.title, clickedArticles.slug, clickedArticles.ip,
clickedArticles.status, clickedArticles.time, authors.name
FROM articles JOIN clickedArticles
ON articles.slug = clickedArticles.slug
JOIN authors on articles.author = authors.id;

CREATE VIEW dailyErrors AS
SELECT to_char(time, 'Month DD, YYYY') as day, count(*) as items
FROM log
WHERE status = '404 NOT FOUND'
GROUP BY day;

CREATE VIEW dailyOKs as
SELECT to_char(time, 'Month DD, YYYY') as day, count(*) as items
FROM log
WHERE status = '200 OK'
GROUP BY day;

Having done these modifications users can launch the script by typing
"python reportTool.py" in the command line.
