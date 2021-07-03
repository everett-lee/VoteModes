import Dependencies._

ThisBuild / scalaVersion     := "2.12.9"
ThisBuild / version          := "0.1.0-SNAPSHOT"
ThisBuild / organization     := "com.lee"
ThisBuild / organizationName := "lee"

lazy val root = (project in file("."))
  .settings(
    name := "VoteModes",
    libraryDependencies += scalaTest % Test,
    assembly / mainClass := Some("com.lee.Main"),
  )
enablePlugins(AssemblyPlugin)

libraryDependencies += "org.scalactic" %% "scalactic" % "3.2.9"
libraryDependencies += "org.scalatest" %% "scalatest" % "3.2.9" % "test"
libraryDependencies += "org.scalatestplus" %% "mockito-3-4" % "3.2.9.0" % "test"
libraryDependencies += "org.mockito" %% "mockito-scala" % "1.16.37" % "test"
libraryDependencies += "com.typesafe.scala-logging" %% "scala-logging" % "3.9.3"
libraryDependencies += "ch.qos.logback" % "logback-classic" % "1.2.3"

libraryDependencies ++= Seq(
  "org.json4s" %% "json4s-native" % "4.0.1",
  "org.json4s" %% "json4s-jackson" % "4.0.1",
)

libraryDependencies ++= Seq(
  "com.github.seratch" %% "awscala-dynamodb" % "0.8.5",
  "com.github.seratch" %% "awscala-s3" % "0.8.5",
)
libraryDependencies ++= Seq(
  "com.amazonaws" % "aws-lambda-java-core" % "1.2.1",
  "com.amazonaws" % "aws-lambda-java-events" % "3.9.0",
  scalaTest % Test
)
