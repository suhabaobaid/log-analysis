#!/usr/bin/env python2
import psycopg2

DBNAME = "news"
QUESTION_1 = "1. What are the most popular three articles of all time?"
QUESTION_2 = "2. Who are the most popular article authors of all time?"
QUESTION_3 = "3. On which days did more than 1% of requests lead to errors?"


def runQuery(query):
    '''
        Connect to the db, runs the query passed and returns the result
    '''
    # 1. Connect to the db
    db = psycopg2.connect(database=DBNAME)
    # 2. Open the cursor
    cur = db.cursor()
    # 3. Execute the command
    cur.execute(query)
    # 4. Get the result
    result = cur.fetchall()
    # 5. Close connection
    db.close()
    # 6. return results
    return result


def printResult(question, result, resultIndex):
    '''
        Prints the question and the result, resultIndex indicates the location
        of the views
    '''
    print("\n" + question + "\n")
    for item in result:
        print("{}\t- {} views".format(item[0], item[resultIndex]))


def printErrorResult(question, result):
    '''
        Prints the result for the 3rd question
    '''
    print("\n" + question + "\n")
    for error in result:
        print("{} - {} % errors".format(
            error[0].strftime('%B %d, %Y'),
            str(round(error[1] * 100, 3))))


def getMostPopularArticles():
    '''
        Prints the top 3 most popular articles of all times
        with the number of views
    '''
    # 1. Build the query
    query = """
        SELECT title, author, views
        FROM articles_view
        LIMIT 3
    """
    # 2. Run the query and get the result
    result = runQuery(query)
    # 3. print result
    printResult(QUESTION_1, result, 2)


def getMostPopularAuthors():
    '''
        Prints the top most popular authors of all times
        with the number of views
    '''
    # 1. Build the query
    query = """
        SELECT authors.name, sum(views) as author_views
        FROM articles_view, authors
        WHERE articles_view.author = authors.id
        GROUP BY authors.name
        ORDER BY author_views desc
    """
    # 2. Run the query and get the result
    result = runQuery(query)
    # 3. print result
    printResult(QUESTION_2, result, 1)


def getErroneousDays():
    '''
        Prints the days where the days lead to more than 1%
        of erroneous requests
    '''
    # 1. Build the query
    query = """
        SELECT t1.day, ROUND((error_num * 1.0 / req_num), 4) AS percent
        FROM (
        SELECT date_trunc('day', time) as day, count(*) AS req_num
        FROM log
        GROUP BY(day) ) t1
        JOIN (
        SELECT date_trunc('day', time) AS day, count(*) AS error_num
        FROM log
        WHERE status >= '400'
        GROUP BY(day)
        ) t2
        ON t1.day = t2.day
        WHERE (ROUND((error_num * 1.0 / req_num), 4) > 0.01)
        ORDER BY percent DESC;
    """
    # 2. Run the query and get the result
    result = runQuery(query)
    # 3. Print result
    printErrorResult(QUESTION_3, result)


if __name__ == '__main__':
    print("\nCalculating results")
    getMostPopularArticles()
    getMostPopularAuthors()
    getErroneousDays()
    print("\nDONE\n")
