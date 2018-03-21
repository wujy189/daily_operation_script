# -*- coding=utf-8 -*-
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import lit
import json

#for RDD map funcation
def f(x):
    line = x[1].split('\n')
    # result = ['0','0',0.0,'0'] #用于指定顺序存放结果
    # index = [200,200,200,200]  #用于判断hbase每条记录，是否存在4个完整的索取值
    # for k,v in enumerate(line):
    #     if (json.loads(v)['qualifier'] =='cdmselldate'):
    #         index[0],result[0] = k,json.loads(v)['value'][0:10]
    #     elif (json.loads(v)['qualifier'] =='cdmno'):
    #         index[1],result[1] = k,json.loads(v)['value']
    #     elif (json.loads(v)['qualifier'] == 'cdmxfje'):
    #         index[2],result[2] = k,float(json.loads(v)['value'])
    #     elif (json.loads(v)['qualifier'] == 'cdmxfmktid'):
    #         index[3],result[3] = k,json.loads(v)['value']
    # if (200 in index):
    #     return ['0','0',0.0,'0']
    # else:
    #     return result

    result = ['0', '0', 0.0, '0']  # 用于指定顺序存放结果
    for k, v in enumerate(line):
        if (json.loads(v)['qualifier'] == 'cdmselldate'):
            result[0] = json.loads(v)['value'][0:10]
        elif (json.loads(v)['qualifier'] == 'cdmno'):
            result[1] = json.loads(v)['value']
        elif (json.loads(v)['qualifier'] == 'cdmxfje'):
            result[2] = float(json.loads(v)['value'])
        elif (json.loads(v)['qualifier'] == 'cdmxfmktid'):
            result[3] = json.loads(v)['value']
    return result

    # result = []
    # for i in line:
    #     i = json.loads(i)
    #     if i['qualifier'] == 'cdmselldate':
    #         result.append(i['value'][0:10])
    #     elif i['qualifier'] == 'cdmno':
    #         result.append(i['value'])
    #     elif i['qualifier'] == 'cdmxfje':
    #         result.append(float(i['value']))
    #     elif i['qualifier'] == 'cdmxfmktid':
    #         result.append(i['value'])

    # index,result = (10,19,20),[]   #10-会员卡号，19-消费金额，20,-消费门店
    # #12-消费日期
    # result.append(json.loads(line[12])['value'][0:10])
    # result.append(json.loads(line[10])['value'])
    # result.append(float(json.loads(line[19])['value']))
    # result.append(json.loads(line[20])['value'])
    # return result
spark = SparkSession.builder\
    .master("yarn-client")\
    .config("spark.serializer","org.apache.spark.serializer.KryoSerializer")\
    .config("spark.mongodb.output.uri", "mongodb://192.168.105.70/renly.daily_statis") \
    .appName("statistics")\
    .getOrCreate()
hbaseconf = {"hbase.zookeeper.quorum":'192.168.103.112',\
             "hbase.mapreduce.inputtable":'custsellday', \
             "hbase.mapreduce.scan.columns": 'info'}
keyConv = "org.apache.spark.examples.pythonconverters.ImmutableBytesWritableToStringConverter"
valueConv = "org.apache.spark.examples.pythonconverters.HBaseResultToStringConverter"
hbase_rdd = spark.sparkContext.newAPIHadoopRDD(\
"org.apache.hadoop.hbase.mapreduce.TableInputFormat",\
"org.apache.hadoop.hbase.io.ImmutableBytesWritable",\
"org.apache.hadoop.hbase.client.Result",\
keyConverter=keyConv, valueConverter=valueConv, conf=hbaseconf)
# print(hbase_rdd.count())

# result = hbase_rdd.first()
# for item in result[1].split('\n'):
#     print(item)

# print(hbase_rdd.map(f).first())

schema = StructType([
        StructField("cdmselldate", StringType(), True),
        StructField("cdmno", StringType(), True),
        StructField("cdmxfje", DoubleType(), True),
        StructField("cdmxfmktid", StringType(), True)
    ])
rdd_filtered = hbase_rdd.map(f)
df = spark.createDataFrame(rdd_filtered,schema)  #RDD to DataFrame
df.createOrReplaceTempView("custsellday")
df_total_jybs = spark.sql("select cdmselldate,count(*) as jybs from custsellday group by cdmselldate")
df_total_jyje = spark.sql("select cdmselldate,sum(cdmxfje) as jyje from custsellday group by cdmselldate")
df_total_hyzs = spark.sql("select cdmselldate,count(DISTINCT cdmno) as hyzs from custsellday group by cdmselldate")
df_tmp = df_total_jybs.join(df_total_jyje,df_total_jybs["cdmselldate"] == df_total_jyje["cdmselldate"])\
        .drop(df_total_jyje["cdmselldate"]) #删除join之后的重复列
df_statis = df_tmp.join(df_total_hyzs,df_tmp["cdmselldate"] == df_total_hyzs["cdmselldate"])\
            .drop(df_total_hyzs["cdmselldate"])
print(df_statis.first())
df_statis.write.format("com.mongodb.spark.sql.DefaultSource")\
                .mode("overwrite")\
                .save()