def get_engine(param_db):
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy_utils import database_exists, create_database
    import psycopg2
    import sys 
    user   = "postgres"
    passwd = "pass_pgsql"
    host   = "172.20.0.6"
    port   = "5432"
    if param_db == 'postgres':
        db = "postgres"
    elif param_db == 'company':
        db = "company"
    else: 
        pass
    try:    
        url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
        if not database_exists(url):
            create_database(url)
        engine = create_engine(url, pool_size=50, echo=False)
        return engine
    except ValueError:
        print("Could not convert data to an integer.")    
    except Exception as exception:
        print("Unexpected error:", sys.exc_info()[0])
        print(exception.message)
    raise    
def create_table(engine):
    from sqlalchemy import create_engine,MetaData,Table, Column, Integer, String,Float
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy_utils import database_exists, create_database
    import sys 
    import sqlalchemy
    if sqlalchemy.inspect(engine).has_table("customers") != True :
        metadata_obj = MetaData()
        customers = Table('customers', metadata_obj,
            Column('RowNumber', Integer),
            Column('CustomerId', Integer, primary_key=True),
            Column('Surname', String(50)),
            Column('CreditScore', Integer),
            Column('Geography', String(50)),
            Column('Gender', String(50)),
            Column('Age', Integer),
            Column('Tenure', Integer),
            Column('Balance', Float),
            Column('NumOfProducts', Integer),
            Column('HasCrCard', Integer),
            Column('IsActiveMember', Integer),
            Column('EstimatedSalary', Float),
            Column('Exited', Integer),
        )
        customers.create(engine)

def insert_table(engine):
    import pandas as pd
    import sys
    from sqlalchemy.exc import DatabaseError
    df_customers = pd.read_csv("/opt/spark-data/pgsql_data.csv")
    try:
        df_customers.to_sql('customers',engine,if_exists='append' ,index=False)
    except:
        print("insert_table error:", sys.exc_info()[0])
def start_env():
    import pymongo
    import pandas as pd
    import os 
    # Starting mongodb environment. Data load..
    myclient = pymongo.MongoClient("mongodb://user_mongodb:pass_mongodb@172.20.0.7:27017")
    # mongo 172.20.0.7:27017/company -u user_mongodb -p pass_mongodb
    print(myclient)
    mydb = myclient["admin"]
    mycol = mydb["customers"]
    df_customers = pd.read_csv("/opt/spark-data/mongodb_data.csv")
    mydb.customers.remove({}) 
    mydb.customers.insert(df_customers.to_dict('records'))
    #Postgres..
    #create db company
    engine = get_engine("company")
    create_table(engine)
    insert_table(engine)

    os.system("rm -r /opt/spark-data/output")
