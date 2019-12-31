package recfun

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

@RunWith(classOf[JUnitRunner])
class RecFunSuite
  extends BalanceSuite
    with PascalSuite
    with CountChangeSuite

