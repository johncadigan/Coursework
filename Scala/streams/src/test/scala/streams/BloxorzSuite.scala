package streams

import org.scalatest.FunSuite

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

import Bloxorz._

@RunWith(classOf[JUnitRunner])
class BloxorzSuite extends FunSuite {

  trait SolutionChecker extends GameDef with Solver with StringParserTerrain {
    /**
     * This method applies a list of moves `ls` to the block at position
     * `startPos`. This can be used to verify if a certain list of moves
     * is a valid solution, i.e. leads to the goal.
     */
    def solve(ls: List[Move]): Block =
      ls.foldLeft(startBlock) { case (block, move) => move match {
        case Left => block.left
        case Right => block.right
        case Up => block.up
        case Down => block.down
      }
    }
  }

  trait Level1 extends SolutionChecker {
      /* terrain for level 1*/

    val level =
    """ooo-------
      |oSoooo----
      |ooooooooo-
      |-ooooooooo
      |-----ooToo
      |------ooo-""".stripMargin

    val optsolution = List(Right, Right, Down, Right, Right, Right, Down)
  }
  trait Level2 extends SolutionChecker {
      /* terrain for level 2*/

    val level =
    """ST
      |oo
      |oo""".stripMargin

    val optsolution = List(Down, Right, Up)
  }
  
  trait Level3 extends SolutionChecker {
      /* terrain for level 2*/

    val level =
    """ST
      |o-
      |oo""".stripMargin

    val optsolution = List()
  }

  test("terrain function level 1") {
    new Level1 {
      assert(terrain(Pos(0,0)), "0,0")
      assert(!terrain(Pos(0,4)), "0,4")
      assert(terrain(Pos(5,8)), "5,8")
    }
  }
  test("terrain function level 2") {
    new Level2 {
      assert(terrain(Pos(0,0)), "0,0")
      assert(terrain(Pos(2,0)), "2,0")
      assert(!terrain(Pos(0,2)), "0,2")
    }
  }

  test("findChar level 1") {
    new Level1 {
      assert(startPos == Pos(1,1))
      assert(goal==Pos(4,7))
    }
  }
  
  test("All possible moves") {
    new Level1 {
      assert(Block(Pos(3,3), Pos(3,3)).neighbors == List((Block(Pos(3,1), Pos(3,2)), Left),(Block(Pos(3,4), Pos(3,5)), Right),(Block(Pos(1,3), Pos(2,3)), Up), (Block(Pos(4,3), Pos(5,3)), Down)))
      assert(Block(Pos(3,2), Pos(3,3)).neighbors == List((Block(Pos(3,1), Pos(3,1)), Left), (Block(Pos(3,4), Pos(3,4)), Right), (Block(Pos(2,2), Pos(2,3)), Up), (Block(Pos(4,2), Pos(4,3)), Down)))
      assert(Block(Pos(2,3), Pos(3,3)).neighbors == List((Block(Pos(2,2), Pos(3,2)), Left), (Block(Pos(2,4), Pos(3,4)), Right), (Block(Pos(1,3), Pos(1,3)), Up), (Block(Pos(4,3), Pos(4,3)), Down)))
    }
  }
  test("All possible legal moves") {
    new Level1 {
      assert(Block(Pos(3,3), Pos(3,3)).legalNeighbors == List((Block(Pos(3,1), Pos(3,2)), Left),(Block(Pos(3,4), Pos(3,5)), Right),(Block(Pos(1,3), Pos(2,3)), Up)))
      assert(Block(Pos(3,2), Pos(3,3)).legalNeighbors == List((Block(Pos(3,1), Pos(3,1)), Left), (Block(Pos(3,4), Pos(3,4)), Right), (Block(Pos(2,2), Pos(2,3)), Up)))
      assert(Block(Pos(2,3), Pos(3,3)).legalNeighbors == List((Block(Pos(2,2), Pos(3,2)), Left), (Block(Pos(2,4), Pos(3,4)), Right), (Block(Pos(1,3), Pos(1,3)), Up)))
    }
  }
  test("Stream of possible moves") {
    new Level1 {
      val expect = Set(
        (Block(Pos(1, 2), Pos(1, 3)), List(Right, Left, Up)),
        (Block(Pos(2, 1), Pos(3, 1)), List(Down, Left, Up)))

      assert(neighborsWithHistory(Block(Pos(1, 1), Pos(1, 1)), List(Left, Up)).toSet === expect)

    }  
    
  }

  test("New neighbors only"){
    new Level1 {
    val expect = Set((Block(Pos(2,1),Pos(3,1)), List(Down,Left,Up))).toStream
    assert(newNeighborsOnly(Set(
    		  				(Block(Pos(1,2),Pos(1,3)), List(Right,Left,Up)),
    		  				(Block(Pos(2,1),Pos(3,1)), List(Down,Left,Up))).toStream,
    		  			Set(Block(Pos(1,2),Pos(1,3)), Block(Pos(1,1),Pos(1,1)))
    )==expect)
    
    }
  }
//  test("solution for level 0"){
//    new Level1 {
//      println(solve(solution))
//      assert(1==0)
//    }
//  }
  test("optimal solution for level 1") {
    new Level1 {
      assert(solve(solution) == Block(goal, goal))
    }
  }
  test("empty solutions for level 3"){
    new Level3 {
      println(solution)
      assert(solution==List())
    }
  }

  test("optimal solution length for level 1") {
    new Level1 {
      assert(solution.length == optsolution.length)
    }
  }
}
