package quickcheck

import org.scalacheck.Prop
import org.scalacheck.Properties
import org.scalacheck.Test.{Failed, PropException, Result, check}
import org.scalatest.FunSuite
import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

object QuickCheckBinomialHeap extends QuickCheckHeap with BinomialHeap

@RunWith(classOf[JUnitRunner])
class QuickCheckSuite extends FunSuite {
  def checkBogus(p: Properties) {
    def fail = throw new AssertionError(s"A bogus heap should NOT satisfy all properties. Try to find the bug!")
    check(asProp(p))(identity) match {
      case r: Result => r.status match {
        case _: Failed         => () // OK: scalacheck found a counter example!
        case p: PropException  => p.e match {
          case e: NoSuchElementException => () // OK: the implementation throws NSEE
          case _ => fail
        }
        case _ => fail
      }
    }
  }

  /** Turns a `Properties` instance into a single `Prop` by combining all the properties */
  def asProp(properties: Properties): Prop = Prop.all(properties.properties.map(_._2):_*)

    test("Binomial heap satisfies properties.") {
    check(asProp(new QuickCheckHeap with quickcheck.test.BinomialHeap))(identity)
  }

  test("Bogus (1) binomial heap does not satisfy properties.") {
    checkBogus(new QuickCheckHeap with quickcheck.test.Bogus1BinomialHeap)
  }

  test("Bogus (2) binomial heap does not satisfy properties.") {
    checkBogus(new QuickCheckHeap with quickcheck.test.Bogus2BinomialHeap)
  }

  test("Bogus (3) binomial heap does not satisfy properties.") {
    checkBogus(new QuickCheckHeap with quickcheck.test.Bogus3BinomialHeap)
  }

  test("Bogus (4) binomial heap does not satisfy properties.") {
    checkBogus(new QuickCheckHeap with quickcheck.test.Bogus4BinomialHeap)
  }

  test("Bogus (5) binomial heap does not satisfy properties.") {
    checkBogus(new QuickCheckHeap with quickcheck.test.Bogus5BinomialHeap)
  }
}
