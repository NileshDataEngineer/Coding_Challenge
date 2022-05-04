from extract_data.mysql_connection import connect
from extract_data.url_details import consume_article_contents, save_to_db, read_db, refresh_table, read_article_names
from jproperties import Properties



def main():
    # read wikipedia article names from text file

    try:
        configs = Properties()
        with open('config.properties', 'rb') as read_prop:
            configs.load(read_prop)

        dbname = {configs.get("database.name").data}.pop()

        table_name = {configs.get("database.tablename").data}.pop()
        articlefile = {configs.get("database.articlefilename").data}.pop()
        sql_alterdb = {configs.get("database.alterdbsql").data}.pop()
        sql_creatdb = {configs.get("database.createdbsql").data}.pop()
        sql_creatbl = {configs.get("database.createtablesql").data}.pop()
        sql_insrt = {configs.get("database.insertsql").data}.pop()
        str_word = {configs.get("database.searchword").data}.pop()
        article_names = read_article_names(articlefile)

        refresh_table(dbname, table_name,sql_alterdb,sql_creatdb)
        print("wikipedia pages consumed in wikipedia.wikipedia_contents started")
        for article_name in article_names:
            article_content = consume_article_contents(article_name)

            save_to_db(article_name, article_content, sql_creatbl,sql_insrt)

        print("wikipedia pages consumed in wikipedia.wikipedia_contents completed \n")
        print("checking occurrence of word in wiki page contents \n")
        read_db(dbname, table_name,str_word)

        print("\n Program execution ended ")

    except:
        pass

if __name__ == '__main__':
    print(" Program execution started \n")
    main()


