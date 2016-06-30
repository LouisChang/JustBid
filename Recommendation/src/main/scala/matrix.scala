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

   
       
   // compute user_id as key, item_id list as value
   var item_list = ticks.map(record => (record._1,record._2))
                                   .groupByKey()
                                   .distinct()

  

   // save the data back into HDFS
   item_list.saveAsTextFile("hdfs://ec2-52-204-162-4.compute-1.amazonaws.com:9000/bid/matrix_data_output_scala_2")
 }
    
}
