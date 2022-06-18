def load(p_df_customers):
    print("LOAD..")
    p_df_customers.coalesce(1).write.csv(
        '/opt/spark-data/output', header='true')
