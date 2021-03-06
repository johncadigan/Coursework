package objsets

import org.scalatest.FunSuite

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

@RunWith(classOf[JUnitRunner])
class TweetSetSuite extends FunSuite {
  trait TestSets {
    //Tweet(val user: String, val text: String, val retweets: Int)
    val a = new Tweet("a", "body " + "a"*3, 30)
    val b = new Tweet("a", "body " + "a"*4, 40)
    val c = new Tweet("c", "c body", 7)
    val d = new Tweet("d", "d body", 9)
    val set1 = new Empty
    val set2 = set1.incl(new Tweet("a", "a body", 20))
    val set3 = set2.incl(new Tweet("b", "b body", 20))
    val set4c = set3.incl(c)
    val set4d = set3.incl(d)
    val set5 = set4c.incl(d)
    val setmine = set1.incl(a).incl(b)
    val setofc = set1.incl(c)
    val set6 = set5.incl(a)
    val set7 = set6.incl(b)
    val google = List("android", "Android", "galaxy", "Galaxy", "nexus", "Nexus")
    val apple = List("ios", "iOS", "iphone", "iPhone", "ipad", "iPad")
    lazy val googleTweets: TweetSet = TweetReader.allTweets.filter((t:Tweet)=>google.exists(t.text.contains(_)))
    lazy val appleTweets: TweetSet = TweetReader.allTweets.filter((t:Tweet)=>apple.exists(t.text.contains(_)))
  }
  
  def asSet(tweets: TweetSet): Set[Tweet] = {
    var res = Set[Tweet]()
    tweets.foreach(res += _)
    res
  }

  def size(set: TweetSet): Int = asSet(set).size

  test("filter: on empty set") {
    new TestSets {
      assert(size(set1.filter(tw => tw.user == "a")) === 0)
    }
  }

  test("filter: a on set5") {
    println("filter: a set on 5")
    new TestSets {
      assert(size(set5.filter(tw => tw.user == "a")) === 1)
    }
  }

  test("filter: 20 on set7") {
    println("filter: 20 on set 7")
    new TestSets {
      assert(size(set7.filter(tw => tw.retweets == 20)) === 2)
    }
  }
  test(" set5 filter: <10 == setofc"){
    new TestSets{
      println("set of c")
      assert(size(set7.filter(tw => tw.retweets < 9.0))===1)
    }
    
  }

  test("union: set4c and set4d") {
    new TestSets {
      println("union sets 4c and 4d")
      assert(size(set4c.union(set4d)) === 4)
    
    }
  }

  test("union: with empty set (1)") {
    new TestSets {
      println("union with empty set")
      assert(size(set5.union(set1)) === 4)
    }
  }

  test("union: with empty set (2)") {
    new TestSets {
      assert(size(set1.union(set5)) === 4)
    }
  }
  
    
  
  test("most retweeted: set5 ==20")
  {
    new TestSets{
      assert(set5.mostRetweeted.user=="a"||set5.mostRetweeted.user=="b")
    }
  }
  test("most retweeted: set6 = 30"){
    new TestSets{
      println("union 1")
      assert(setmine.union(set5).mostRetweeted.retweets===40)
      println("union 2")
      assert(set5.union(setmine).mostRetweeted.retweets===40)
    }
  }
  test("descending: set5") {
    new TestSets {
      println("descending")
      val trends = set5.descendingByRetweet
      assert(!trends.isEmpty)
      assert(trends.head.user == "a" || trends.head.user == "b")
    }
  }
  test("descending: all google and apple tweets"){
    new TestSets{
      val trending: TweetList = googleTweets.union(appleTweets).descendingByRetweet
      assert(trending.head.retweets===321)
    }
  }
}
