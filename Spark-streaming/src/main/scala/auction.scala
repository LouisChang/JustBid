import kafka.serializer.StringDecoder

import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka._
import org.apache.spark.SparkConf
import org.apache.spark.rdd.RDD
import org.apache.spark.SparkContext
import org.apache.spark.sql._
import java.util.Calendar
import com.datastax.spark.connector._

import scala.util.parsing.json._

object BidDataStreaming {
  def main(args: Array[String]) {

    val SPARK_MASTER = "ec2-52-204-162-4.compute-1.amazonaws.com"
    val brokers = SPARK_MASTER + ":9092"
    //can have several topics
    val topics = "my-topic-1" 
    val topicsSet = topics.split(",").toSet 

    // Create context with 2 second batch interval
    val sparkConf = new SparkConf().setAppName("bid").set("spark.cassandra.connection.host", SPARK_MASTER)
    val ssc = new StreamingContext(sparkConf, Seconds(2))

    // Create direct kafka stream with brokers and topics
    val kafkaParams = Map[String, String]("metadata.broker.list" -> brokers)
    val messages = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](ssc, kafkaParams, topicsSet)

    // Get the lines and show results
    messages.foreachRDD { rdd =>

        val sqlContext = SQLContextSingleton.getInstance(rdd.sparkContext)
        import sqlContext.implicits._

        val lines = rdd.map(_._2)
        // get the data you want
        val bidsStreaming = lines.map( rawBid => {

                                var json:Option[Any] = JSON.parseFull(rawBid)
                                val bid:Map[String,Any] = json.get.asInstanceOf[Map[String, Any]]
                                val item:Long = bid.get("itemInSession").get.asInstanceOf[Double].toLong
                                    
                                val user:Long = bid.get("sessionId").get.asInstanceOf[Double].toLong
                                var bidprice:Long = 0
                                if (bid.contains("length")) {
                                    bidprice = bid.get("length").get.asInstanceOf[Double].toLong
                                    
                                }
                                val today = Calendar.getInstance.getTime.toString
                                val time = Calendar.getInstance.getTime 
                                (item,user,bidprice,today,time)
                                })
        bidsStreaming.saveToCassandra("justbid","bidding3", SomeColumns("item_id","user_id","bid_price","current_time","time"))
        bidsStreaming.saveToCassandra("justbid","bidding_user", SomeColumns("item_id","user_id","bid_price","current_time","time"))

    }


    // Start the computation
    ssc.start()
    ssc.awaitTermination()
  }
}
