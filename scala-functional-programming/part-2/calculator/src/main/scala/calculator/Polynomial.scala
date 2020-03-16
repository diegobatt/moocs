package calculator

object Polynomial {
  def computeDelta(a: Signal[Double], b: Signal[Double],
      c: Signal[Double]): Signal[Double] = {
    def delta = b() * b() - 4 * a() * c()
    Signal(delta)
  }

  def computeSolutions(a: Signal[Double], b: Signal[Double],
      c: Signal[Double], delta: Signal[Double]): Signal[Set[Double]] = {
    def positive = (-b() + math.sqrt(delta())) / (2 * a())
    def negative = (-b() - math.sqrt(delta())) / (2 * a())
    def logic = if (delta() < 0) Set[Double]() else Set(positive, negative)
    Signal(logic)
  }
}
