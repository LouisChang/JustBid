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
    
            
    def Jaccard(list1Values: Seq[Iterable[String]], list2Values: Seq[Iterable[String]]) = {
    val col1 = list1Values.toSet
    val col2 = list2Values.toSet

    val jSimilarity = (col1 & col2).size / (col1 ++ col2).size.toDouble
    jSimilarity
  }
     
   // map each record into a tuple consisting of (user_id,item_id)
   val bids = file.map(line => {
                        val record = line.split(" ")
                       (record(0), record(1))
                                })
       
   // compute user_id as key, item_id list as value, item_list is a RDD
   var item_list = bids.map(record => (record._1,record._2))
                                   .groupByKey()
                                   .distinct()
    
       // form a HashMap of (user -> items) key value pairs.
       // keep as an RDD, but have as a key value pair
       
   // get all the users, users is a RDD
   var users = item_list.map(record => record._1)
                             .distinct()
       
   // calculate user cross, usercross is a RDD
   var usercross = users.cartesian(users)
   
   //var 
   var sim = usercross.map(tuple => Jaccard(item_list.lookup(tuple._1),item_list.lookup(tuple._2)).toDouble)
       

   // save the data back into HDFS
   item_list.saveAsTextFile("hdfs://ec2-52-204-162-4.compute-1.amazonaws.com:9000/bid/matrix_data_output_scala_22")
   sim.saveAsTextFile("hdfs://ec2-52-204-162-4.compute-1.amazonaws.com:9000/bid/matrix_data_output_scala_3")   
 }
    
}
