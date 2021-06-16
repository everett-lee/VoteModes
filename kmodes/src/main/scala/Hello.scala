
import awscala._
import dynamodbv2._



object Hello {
  def main(args: Array[String]) {
    println("Hello World!")
    testIT()
  }

  def testIT(): Unit = {

    
    implicit val dynamoDB = DynamoDB.at(Region.Ireland)

    val table: Table = dynamoDB.table("MPs").get

    val mps: Seq[Item] = table.scan(Seq("MPElectionYear" -> cond.eq(2019)))

    val attributes = mps(0).attributes
    attributes.foreach(el => println(el))

//    for (
//      (attribute <- attributes)
//      yield attribute.name match
//    )

  }

}
