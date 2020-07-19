package timeusage

import TimeUsage._

import org.apache.spark.sql.{ColumnName, Column, DataFrame, Row}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types.{
  DoubleType,
  StringType,
  StructField,
  StructType
}
import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner
import org.scalatest.{BeforeAndAfterAll, FunSuite}

import scala.util.Random

@RunWith(classOf[JUnitRunner])
class TimeUsageSuite extends FunSuite with BeforeAndAfterAll {

  test("Test DataFrame schema") {
    val schema = StructType(List(
      StructField("name", StringType, false),
      StructField("val1", DoubleType, false),
      StructField("val2", DoubleType, false)
    ))
    val schema_ = dfSchema(List("name", "val1", "val2"))
    assert(schema === schema_, "Failed to create schema")
  }

  test("Test row creation") {
    val r = Row("aux", 1.0, 2.1)
    val r_ = row(List("aux", "1.0", "2.1"))
    assert(r === r_, "Failed to create row")
  }

  test("Test columns classification") {
    val names = List("t01", "t02", "t03", "t04", "t05")
    val classify = (
      List(col("t01"), col("t03")),
      List(col("t05")),
      List(col("t02"), col("t04"))
    )
    val classify_ = classifiedColumns(names)
    assert(classify === classify_, "Failed to classify columns correctly")
  }

  // test("Auxiliar test") {
  //   val (columns, initDf) = read("/timeusage/atussum.csv")
  //   val (primaryNeedsColumns, workColumns, otherColumns) = classifiedColumns(columns)
  //   val summaryDf = timeUsageSummary(primaryNeedsColumns, workColumns, otherColumns, initDf)
  //   val summaryDfTyped = timeUsageSummaryTyped(summaryDf)
  // }
}
