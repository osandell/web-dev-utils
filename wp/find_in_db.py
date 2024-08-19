#!/usr/bin/env python3

import mysql.connector
import sys
from colorama import Fore, Style, init

# Initialize colorama
init()

def search_database(db_name, search_term):
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': db_name,
        'charset': 'utf8mb4',  # Set charset to utf8mb4
        'collation': 'utf8mb4_unicode_ci'  # Set collation to a compatible one
    }

    cnx = None
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

        query_generator = f"""
        SELECT CONCAT('SELECT `', COLUMN_NAME, '` AS column_value, "', TABLE_NAME, 
                      '" AS table_name FROM ', TABLE_NAME, ' WHERE `', COLUMN_NAME, 
                      '` LIKE ''%{search_term}%''') AS generated_query 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = '{db_name}' 
        AND DATA_TYPE IN ('char', 'varchar', 'text', 'longtext');
        """

        cursor.execute(query_generator)
        generated_queries = cursor.fetchall()

        for query in generated_queries:
            try:
                cursor.execute(query[0])
                results = cursor.fetchall()
                if results:
                    print(f"\n{Fore.GREEN}Results found in query: {Fore.YELLOW}{query[0]}{Style.RESET_ALL}")
                    for result in results:
                        print(result)
            except mysql.connector.Error as err:
                print(f"Error occurred: {err}")
                continue
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
    finally:
        if cnx and cnx.is_connected():
            cursor.close()
            cnx.close()

def main():
    if len(sys.argv) != 3:
        print("Usage: ./find_in_db.py [database_name] [search_term]")
        sys.exit(1)

    db_name = sys.argv[1]
    search_term = sys.argv[2]
    search_database(db_name, search_term)

if __name__ == "__main__":
    main()
