package recfun

object Main {
  def main(args: Array[String]) {
    println("Pascal's Triangle")
    for (row <- 0 to 10) {
      for (col <- 0 to row)
        print(pascal(col, row) + " ")
      println()
    }
  }

  /**
   * Exercise 1
   */
    def pascal(c: Int, r: Int): Int = {
      if (c > r || c < 0 || r < 0) 
        throw new IllegalArgumentException("Can't find the pascal value for this position")
      else if (c == r || c == 0 || r == 0)
        1
      else
        pascal(c-1, r-1) + pascal(c, r-1)
    }
  
  /**
   * Exercise 2
   */
    def balance(chars: List[Char]): Boolean = {
      def countOpenCloseDiff(chars: List[Char], opens: Int, closes: Int): Int = {
        if (chars.isEmpty) 
          opens - closes
        else if (closes > opens)
          -2 // throw new IllegalArgumentException("What are you closing?")
        else
          countOpenCloseDiff(
            chars.tail,
            if (chars.head == '(') opens + 1 else opens,
            if (chars.head == ')') closes + 1 else closes)
      }
      countOpenCloseDiff(chars, 0, 0) == 0
    }
  
  /**
   * Exercise 3
   */
    def countChange(money: Int, coins: List[Int]): Int = {
      if (money < 0 || coins.isEmpty) 0
      else if (money == 0) 1
      else countChange(money, coins.tail) + countChange(money - coins.head, coins)
    }
  }
