package example


object Lists {

    def sum(xs: List[Int]): Int = {
      if(xs.isEmpty) {
        0
      } else {
        xs.head + sum(xs.tail)
      }
    }
  
    def _max(xs: List[Int], result:Int): Int = {
      if(xs.isEmpty) {
        result
      } else {
        _max(xs.tail, if(xs.head > result) xs.head else result)
      }
    }

    def max(xs: List[Int]): Int = {
      if(xs.isEmpty) {
        throw new NoSuchElementException("No max in empty list")
      }
      _max(xs.tail, xs.head)
    }
  }
