import dbactions

def main():
    dbactions.dbget(
        db_name='tasks', table_name='todo'
    )
    

if __name__ == '__main__':
    main()
