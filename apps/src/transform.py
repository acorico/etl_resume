def transform(p_df_customers,p_spark):
    from pyspark.sql.functions import udf
    from pyspark.sql.types import StringType
    def upperCase(str):
        return str.upper()
    print("TRANSFORM..")
    upperCaseUDF = udf(upperCase, StringType())
    p_spark.udf.register("upperCaseUDF", upperCaseUDF)
    p_df_customers.createOrReplaceTempView('temp_customers')
    p_df_customers =p_spark.sql("select  upperCaseUDF(Geography) as Geography" +
                                      ", upperCaseUDF(Gender) as Gender" +
                                      ", count(*) as Num_of_Customers " + 
                                      ", sum(NumOfProducts) as Num_of_Products " +
                                      "from temp_customers" + 
                                      " where CreditScore > 500 " +
                                      " group by Geography,Gender " +
                                      " having sum(NumOfProducts) < 1900 " +
                                      " order by Geography,Gender " 
                                      )
    return p_df_customers