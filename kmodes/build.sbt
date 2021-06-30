import Dependencies._

ThisBuild / scalaVersion     := "2.13.6"
ThisBuild / version          := "0.1.0-SNAPSHOT"
ThisBuild / organization     := "com.lee"
ThisBuild / organizationName := "lee"

lazy val root = (project in file("."))
  .settings(
    name := "kModes",
    libraryDependencies += scalaTest % Test
  )

libraryDependencies += "org.scalactic" %% "scalactic" % "3.2.9"
libraryDependencies += "org.scalatest" %% "scalatest" % "3.2.9" % "test"
libraryDependencies += "org.scalatestplus" %% "mockito-3-4" % "3.2.9.0" % "test"
libraryDependencies += "org.mockito" %% "mockito-scala" % "1.16.37" % "test"
libraryDependencies ++= Seq(
  "com.github.seratch" %% "awscala-dynamodb" % "0.9.+",
  "com.github.seratch" %% "awscala-s3" % "0.9.+",
)
libraryDependencies ++= Seq(
  "com.amazonaws" % "aws-lambda-java-core" % "1.2.1",
  "com.amazonaws" % "aws-lambda-java-events" % "3.9.0",
  scalaTest % Test
)

//addSbtPlugin("com.eed3si9n" % "sbt-assembly" % "1.17.0")
