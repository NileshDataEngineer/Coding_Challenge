# importing the requests library
import requests
import mysql.connector


def extract_content(article_title):
    url = "https://en.wikipedia.org/w/api.php"
    action = "query"
    prop = "extracts"
    explaintext = "explaintext"
    titles = article_title
    format = "json"
    PARAMS = {'action': action, "prop": prop, "explaintext": explaintext, "titles": titles, "format": format}
    r = requests.get(url=url, params=PARAMS)
    data = r.json()
    page_id = list(data["query"]["pages"].keys())[0]
    content = data["query"]["pages"][page_id]["extract"]
    return content

def save_db(id,article_name,article_contetnt):
    mydb = mysql.connector.connect(
        host="localhost",
        user="freenow",
        password="freenow",
        database="assingment"
    )

    mycursor = mydb.cursor()
    sql = "INSERT INTO article (id,article_name,content) VALUES (%s, %s, %s)"
    val = (id,article_name,article_contetnt)

    mycursor.execute(sql, val)
    mydb.commit()

    print(mycursor.rowcount, "details inserted")

    # disconnecting from server
    mydb.close()

def read_db(dbname , tablename):
    mydb = mysql.connector.connect(
        host="localhost",
        user="freenow",
        password="freenow",
        database="assingment"
    )

    cursor=mydb.cursor()
    cursor.execute("select * from {}.{}".format(dbname,tablename))
    result=cursor.fetchall()
    for res in result:
        print(type(res))
        print('\n')
        wordoccurence(res[2])

def wordoccurence(str_tuple):
    str_py=""
    for tup in str_tuple:
        str_py=str_py  +tup

    print(type(str_py))
    print(str_tuple.count("Taxi"))
    print(str_py)


def main():
    print("Extract contect")
    #article_name="Python_(programming_language)"
    article_name="Free_Now_(service)"
    extract_contents= extract_content(article_name)
    print("Save db")
    save_db(1,article_name,extract_contents)
    print("db done")
    read_db("assingment","article")

# __name__
if __name__ == "__main__":
    main()