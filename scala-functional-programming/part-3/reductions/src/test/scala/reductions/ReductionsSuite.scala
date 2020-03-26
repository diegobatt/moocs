package reductions

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

@RunWith(classOf[JUnitRunner])
class ReductionsSuite
  extends LineOfSightSuite
    with ParallelCountChangeSuite
    with ParallelParenthesesBalancingSuite

