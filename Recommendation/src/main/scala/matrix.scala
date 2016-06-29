import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
    
object matrix_data{
        def main(args: Array[String]) {

   // setup the Spark Context named sc
   val conf = new SparkConf().setAppName("MatrixDataExercise")
   val sc = new SparkContext(conf)

   // file on HDFS to pull the data from
   val file_name = "hdfs://ec2-52-204-162-4.compute-1.amazonaws.com:9000/bid/output.txt"

   // read in the data from HDFS
   val file = sc.textFile(file_name)

   // map each record into a tuple consisting of (user_id,item_id)
   val ticks = file.map(line => {
                        val record = line.split(" ")
                       (record(0).toLong, record(1).toLong)
                                })

   // apply the time conversion to the time portion of each tuple and persist it memory for later use
   //val ticks_min30 = ticks.map(record => (convert_to_30min(record._1),
   //                                       record._2,
   //                                       record._3)).persist

   // compute the average price for each 30 minute period
   //val price_min30 = ticks_min30.map(record => (record._1, (record._2, 1)))
   //                             .reduceByKey( (x, y) => (x._1 + y._1,
   //                                                      x._2 + y._2) )
   //                             .map(record => (record._1,
   //                                             record._2._1/record._2._2) )
       
   // compute user_id as key, item_id list as value
   var item_list = ticks.map(record => (record._1,record._2))
                                   .groupByKey()
                                   .distinct()

   // compute the total volume for each 30 minute period
   //val vol_min30 = ticks_min30.map(record => (record._1, record._3))
   //                           .reduceByKey(_+_)

   // join the two RDDs into a new RDD containing tuples of (30 minute time periods, average price, total volume)
   //val price_vol_min30 = price_min30.join(vol_min30)
   //                                 .sortByKey()
   //                                 .map(record => (record._1,
   //                                                 record._2._1,
   //                                                 record._2._2))

   // save the data back into HDFS
   item_list.saveAsTextFile("hdfs://ec2-52-204-162-4.compute-1.amazonaws.com:9000/bid/matrix_data_output_scala_2")
 }
    
}
