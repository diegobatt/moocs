package stackoverflow

import org.scalatest.{FunSuite, BeforeAndAfterAll}
import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.rdd.RDD
import java.io.File

@RunWith(classOf[JUnitRunner])
class StackOverflowSuite extends FunSuite with BeforeAndAfterAll {


  lazy val testObject = new StackOverflow {
    override val langs =
      List(
        "JavaScript", "Java", "PHP", "Python", "C#", "C++", "Ruby", "CSS",
        "Objective-C", "Perl", "Scala", "Haskell", "MATLAB", "Clojure", "Groovy")
    override def langSpread = 50000
    override def kmeansKernels = 45
    override def kmeansEta: Double = 20.0D
    override def kmeansMaxIterations = 120
  }

  import StackOverflow._
  val q1 = Posting(1, 1, Some(2), None, 5, Some("PHP"))
  val ans1 = Posting(2, 2, None, Some(1), 10, None)
  val ans2 = Posting(2, 3, None, Some(1), 15, None)
  val q2 = Posting(1, 4, None, None, 20, Some("Python"))
  val postings = Seq(q1, ans1, ans2, q2)
  // Inner join leaves q2 out
  val grouped = Seq((1, Iterable((q1, ans1), (q1, ans2))))
  val scored = Seq((q1, 15))

  override def afterAll(): Unit = {
    sc.stop()
  }


  test("testObject can be instantiated") {
    val instantiatable = try {
      testObject
      true
    } catch {
      case _: Throwable => false
    }
    assert(instantiatable, "Can't instantiate a StackOverflow object")
  }

  test("Test grouping") {
    val grouped_ = groupedPostings(sc.parallelize(postings)).collect()
    assert(grouped === grouped_, "groupedPostings fail")
  }

  test("Test highcore") {
    val scored_ = scoredPostings(sc.parallelize(grouped)).collect()
    assert(scored === scored_, "scoredPostings fail")
  }

  test("Test vectors") {
    val vectors_ = vectorPostings(sc.parallelize(scored)).collect()
    assert(Seq((2 * langSpread, 15)) === vectors_, " vectorPostings fail")
  }

  test("Test Kmeans") {
    val vectors = sc.parallelize(Seq((2*langSpread, 15), (2*langSpread, 30)))
    val means = 
    // median is 15 or 30 ? has to return an int
    assert(Array(("PHP", 1.0D, 2, 30)) === results, " ClustrResults fail")
  }

  test("Test Results") {
    val vectors = sc.parallelize(Seq((2*langSpread, 15), (2*langSpread, 30)))
    val results = clusterResults(Array((10000, 15)), vectors)
    // median is 15 or 30 ? has to return an int
    assert(Array(("PHP", 1.0D, 2, 30)) === results, " ClustrResults fail")
  }

}
// Posting(
//   postingType: Int,
//   id: Int,
//   acceptedAnswer: Option[Int],
//   parentId: Option[QID],
//   score: Int,
//   tags: Option[String])