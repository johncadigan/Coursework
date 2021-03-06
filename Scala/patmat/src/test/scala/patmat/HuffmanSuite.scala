package patmat

import org.scalatest.FunSuite

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

import patmat.Huffman._

@RunWith(classOf[JUnitRunner])
class HuffmanSuite extends FunSuite {
  trait TestTrees {
    val s1 = "cccbba"
    val s3 = "a"*28 + "b" * 14 + "c" * 6 + "d" * 4 + "e" * 2 + "f"
    val t1 = Fork(Leaf('a',2), Leaf('b',3), List('a','b'), 5)
    val t2 = Fork(Fork(Leaf('a',2), Leaf('b',3), List('a','b'), 5), Leaf('d',4), List('a','b','d'), 9)
    println("s3 to tree \n", createCodeTree(s3.toList))

  }
  
  test("weight of a larger tree") {
    new TestTrees {
      assert(weight(t1) === 5)
    }
  }

  test("chars of a larger tree") {
    new TestTrees {
      assert(chars(t2) === List('a','b','d'))
    }
  }

  test("string2chars(\"hello, world\")") {
    assert(string2Chars("hello, world") === List('h', 'e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r', 'l', 'd'))
  }
  test("times s1 = (c,3), (b,2), (a,1)"){
    new TestTrees{
    assert(times(s1.toList)===List(('c',3), ('b',2), ('a',1)))
    }
  }
  test("times Nil"){
    new TestTrees{
    assert(times(List())===List())
    }
  }
  test("makeOrderedLeafList for some frequency table") {
    assert(makeOrderedLeafList(List(('t', 2), ('e', 1), ('x', 3))) === List(Leaf('e',1), Leaf('t',2), Leaf('x',3)))
  }
  test("makeOrderedLeafList of Nil") {
    assert(makeOrderedLeafList(List()) === List())
  }

  test("combine of some leaf list") {
    val leaflist = List(Leaf('e', 1), Leaf('t', 2), Leaf('x', 4))
    println("combine of some leaf list \n %s \n =? \n %s".format(combine(leaflist), List(Fork(Leaf('e',1),Leaf('t',2),List('e', 't'),3), Leaf('x',4))))
    assert(combine(leaflist) === List(Fork(Leaf('e',1),Leaf('t',2),List('e', 't'),3), Leaf('x',4)))
  }
  test("decode simple ab tree"){
    new TestTrees{
      assert(decode(t1, List(1))===List('b'))
    }
  }
  test("decode simple abd tree"){
    new TestTrees{
      assert(decode(t2, List(1,0,0,0,1))===List('d', 'a', 'b'))
    }
  }
  test("encode simple ab tree"){
    new TestTrees{
      //println("encode");println( encode(t1)(List('b')))
      assert(encode(t1)(List('b'))===List(1))
    }
  }
  test("encode simple abd tree"){
    new TestTrees{
      assert(encode(t2)(List('d', 'a', 'b'))===List(1,0,0,0,1))
    }
  }
  test("decode and encode a very short text should be identity") {
    new TestTrees {
      assert(decode(t1, encode(t1)("ab".toList)) === "ab".toList)
    }
  }
  test("convert to simple ab tree to table"){
    new TestTrees{
      assert(convert(t1)===List(('a',List(0)), ('b', List(1))))
    }
  }
  test("convert to simple abd tree to table"){
    new TestTrees{
      assert(convert(t2)===List(('a',List(0,0)), ('b', List(0,1)), ('d', List(1))))
    }
  }
  test("optimal encoding"){
		  val msg = "The Huffman encoding of this message should be three hundred and fifty-two bits long".toList
		  println("Creating code tree")
		  val codetree = createCodeTree(msg)
		  println("Quick encoding")
		  val result = quickEncode(codetree)(msg)
		  assert(result.size==352)
}
  
  test("decode and quickEncode abd") {
    new TestTrees {
      assert(decode(t2, quickEncode(t2)("bad".toList)) === "bad".toList)
    }
  }
}
