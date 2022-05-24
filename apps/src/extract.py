def extract(p_spark):
    print("EXTRACT..")
    df_customer_mongo_db = p_spark.read\
                            .format('com.mongodb.spark.sql.DefaultSource')\
                            .option( "uri", "mongodb://user_mongodb:pass_mongodb@172.20.0.7:27017/admin.customers") \
                            .load()    
    # Read Postgres    
    df_customer_pgsql = p_spark.read \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://172.20.0.6:5432/company") \
        .option("dbtable", "customers") \
        .option("user", "postgres") \
        .option("password", "pass_pgsql") \
        .option("driver", "org.postgresql.Driver") \
        .load()

    #Order Columns..
    df_customer_mongo_db.createOrReplaceTempView('temp_customers_mongo')
    df_customer_mongo_db =p_spark.sql("select RowNumber,CustomerId,Surname,CreditScore,Geography,Gender,Age," +
                                      "Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary,Exited " +
                                      "from temp_customers_mongo")
    #Return union between mongo and pgsql
    return df_customer_mongo_db.union(df_customer_pgsql)