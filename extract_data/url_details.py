import requests
import mysql.connector

from extract_data.mysql_connection import connect


def read_article_names(articlefile):
    try:


        file = open(articlefile, "r")
        article_lists = file.read().split('\n')

        if len(article_lists) <= 1:

            raise Exception("article_name.txt file is empty")

        return article_lists
    except FileNotFoundError:
        print("Exception : article_names.txt this file is missing")
    except Exception:
        print("Exception : article_name.txt file is empty")

def consume_article_contents(article_title):
    url = "https://en.wikipedia.org/w/api.php"
    action = "query"
    prop = "extracts"
    explaintext = "explaintext"
    titles = article_title
    format = "json"
    PARAMS = {'action': action, "prop": prop, "explaintext": explaintext, "titles": titles, "format": format}
    response_str = requests.get(url=url, params=PARAMS)
    data = response_str.json()
    page_id = list(data["query"]["pages"].keys())[0]
    content = data["query"]["pages"][page_id]["extract"]
    return content


def save_to_db(article_name, article_content,sql_creatbl,sql_insrt):

    try:

        mysql_db = connect()
        my_cursor = mysql_db.cursor()


        val = (article_name, article_content)

        my_cursor.execute(sql_creatbl)
        my_cursor.execute(sql_insrt, val)
        mysql_db.commit()

    # disconnecting from server
        mysql_db.close()
    except mysql_db.Error:
        print("Exception with Mysql Connection")

def read_db(dbname, table_name,str_word):

    mysql_db = connect()
    cursor = mysql_db.cursor()
    cursor.execute("select * from {}.{}".format(dbname, table_name))
    result = cursor.fetchall()
    for res in result:

        word_occurrence(res,str_word)


def refresh_table(dbname, table_name,sql_alterdb,sql_creatdb):

    try:
        mysql_db = connect()
        cursor = mysql_db.cursor()

        cursor.execute(sql_creatdb)
        cursor.execute(sql_alterdb)
        cursor.execute("drop table if exists {}.{}".format(dbname, table_name))

    except Exception():

        print("Exception in refresh_table")

def word_occurrence(str_dict,str_word):
    count = 0
    str_spit = str_dict[1].split(' ')
    for word in str_spit:
        if str_word.__eq__(word):
            count = count+1
    print("occurrence of taxi in article {} {} times".format(str_dict[0], count))
