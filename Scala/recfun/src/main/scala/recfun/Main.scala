package recfun
import common._

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
  if(c==0){1}
  else if(c==r) {1}
  else{pascal(c-1, r-1) + pascal(c, r-1)}
  }
  /**
   * Exercise 2
   */
  def balance(chars: List[Char]): Boolean = {
    if(chars.isEmpty){true}
	else if(chars.head=='('){
	  if(chars.tail.size == 0){false}
	  def expandbuffer(buff: String, left: List[Char]): List[Char] ={
	    if(left.size > 0){
	    val buffer = buff + left.head.toString
	    val open = buffer.count(_=='(') - buffer.count(_ == ')')
	    if(open==0){left.tail}
		else{expandbuffer(buffer, left.tail)}
	    }
	    else{List(')')}
	  }
	   
	   val tail = expandbuffer(chars.head.toString, chars.tail)
	   balance(tail)
	}
	else if(chars.head==')'){false}
	else{
	  balance(chars.tail)
	}   
	}
  
  /**
   * Exercise 3
   */
  def countChange(money: Int, coins: List[Int]): Int = {
    if(money == 0){1}
    else if(coins.isEmpty ||money < 0){0}  
    else{countChange(money-coins.head, coins) + countChange(money, coins.tail)}
  }
}
