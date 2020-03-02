package quickcheck

import common._

import org.scalacheck._
import Arbitrary._
import Gen._
import Prop._

abstract class QuickCheckHeap extends Properties("Heap") with IntHeap {

  lazy val genHeap: Gen[H] = oneOf(
    const(empty),
    for {
      m <- arbitrary[Int]
      h <- oneOf(const(empty), genHeap)
    } yield insert(m, h)
  )
  implicit lazy val arbHeap: Arbitrary[H] = Arbitrary(genHeap)

  def minList(h: H): Boolean = {
    if (isEmpty(h)) true
    else {
      val a = findMin(h)
      val nextH = deleteMin(h)
      if (isEmpty(nextH)) true
      else {
        val b = findMin(nextH)
        if (b < a) false else minList(nextH)
      }
    }
  }

  property("gen1") = forAll { (h: H) =>
    val m = if (isEmpty(h)) 0 else findMin(h)
    findMin(insert(m, h)) == m
  }

  property("min1") = forAll { a: Int =>
    val h = insert(a, empty)
    findMin(h) == a
  }

  property("delete1") = forAll { a: Int =>
    val h = insert(a, empty)
    isEmpty(deleteMin(h))
  }

  property("min2") = forAll { (a: Int, b:Int) =>
    val h = insert(b, insert(a, empty))
    if (a < b) findMin(h) == a
    else findMin(h) == b
  }

  property("min after delete") = forAll { (a: Int, b:Int) =>
    val h = deleteMin(insert(b, insert(a, empty)))
    if (a < b) findMin(h) == b
    else findMin(h) == a
  }

  property("consistent min") = forAll { (h: H) =>
    minList(h)
  }

  property("meldming1") = forAll { (h1: H, h2: H) =>
    val h = meld(h1, h2)
    val m = if (isEmpty(h)) 0 else findMin(h)
    if (isEmpty(h1) && isEmpty(h2)) m == 0
    else if (isEmpty(h1)) m == findMin(h2)
    else if (isEmpty(h2)) m == findMin(h1)
    else {
      val a = findMin(h1)
      val b = findMin(h2)
      if (a < b) m == a
      else m == b
    }
  }

  // property("min after delete 2") = forAll { (a: Int, b:Int) =>
  //   val h = deleteMin(insert(b, insert(a, empty)))
  //   if (a < b) findMin(insert(a, h)) == a
  //   else findMin(insert(b, h)) == b
  // }

  property("min after dleete and insert") = forAll { (a: Int) =>
    val h = {
      if (a > 0) insert(a - 2, insert(a - 1, insert(a, empty)))
      else insert(a + 2, insert(a + 1, insert(a, empty)))
    }
    val b = findMin(deleteMin(h))
    if (a > 0) b != a - 2 else b != a
  }

  // property("min after dleete and insert") = forAll { (h: H) =>
  //   if (isEmpty(h)) true
  //   else {
  //     val a = findMin(h)
  //     val newMin = a - 1
  //     val b = findMin(insert(newMin, deleteMin(h)))
  //     newMin == b
  //   }
  // }
}
