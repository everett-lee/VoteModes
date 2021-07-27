## VoteModes

### TL;DR

This project contains serverless applications that download House of Commons (HoC) voting data
for use as input to a K-modes clustering algorithm.  

K-modes is implemented using Scala and deployed as an AWS Lambda.  

A Python application - also deployed as an AWS Lambda - performs the data download and processing tasks.   

The outputs of the K-modes algorithm are converted to JSON and added to an S3 bucket.
Each application accesses a shared DynamoDB database.  

The above might beg the question: couldn't these steps be handled by a single app? Answer: yes, but
that's no fun :)

### Infrastructure

![K-modes infrastructure diagram](./infrastructure_diagram.jpg "K-modes infrastructure")

### Downloader Lambda

The downloader Lambda fetches data from the HoC's APIs, then converts
the results to a format suited to the K-modes algorithm. This Lambda is executed once monthly 
using a cron expression.

`divisions_list_downloader.py` handles fetching vote (division in HoC terminology)  
data from the `/divisions` endpoint using helper functions in
`divisions/downloaders.py`. 

Unfortunately, this division data does not contain the votes cast for individual MPs, 
only the total for and against counts. As such,
`votes_per_division_downloader.py` and its helpers in `votes_per_divisions/downloaders.py`
contain code to extract the division ids returned from `/divisions`
for use as inputs for the HoC's `/division/{id}` endpoint.   

To reduce the Lambda's execution time, each division's voting data is downloaded in parallel.

The resulting data for each MP is then extracted and used to update a 
DynamoDB table containing data for each MP. This data is initialised manually using the (simplifying but wrong) 
assumption that the list of MPs will remain unchanged between election years.

The table contains a `Votes` value for each MP, representing their votes as a list of mappings
from `DivisionId` -> `Vote` (Aye/No/NoAttend). This, along with the `MemberId`, drives 
the K-modes algorithm.

### K-Modes lambda

The K-Modes algorithm is written in Scala and also executed as a Lambda. Instead of 
running on a schedule, the K-Modes lambda is triggered using a subscription to an SQS 
queue. Messages in this queue are produced by the downloader lambda.

K-Modes was selected for this data, in place of better-known K-means algorithm, as
the  input is categorical (categories of vote cast). This makes it difficult to 
represent the data numerically (should a 'No Attend' be closer to a 'No' 
than a 'Yes' is?) as input to the distance formula.

With K-Modes, each MP is instead checked to see how much he or she 'agrees' with current centroid
by comparing their votes cast for each division. If they voted the same way, their
agreement score is incremented, otherwise the next vote is checked. This alternative
implementation of the distance function is listed in `CentroidsHelperMain.scala`:

```scala
  @tailrec
  final override def calculateDistance(votes: List[VotePair], centroid: List[VotePair], acc: Int = 0): Int = {
    require(votes.size == centroid.size, "Vote sizes must match")

    votes match {
      case Nil => acc
      case x :: xs =>
        require(x.divisionId == centroid.head.divisionId, "Divisions Ids must match")
        val res = if (x.voteDecision != centroid.head.voteDecision) 1 else 0
        calculateDistance(xs, centroid.tail, acc + res)
    }
  }
```


select k, now = 5
Parse db data  
Select starting centroids   
Group by 'distance' -> Reculate using mode -> repeat until stable of max iters  
Convert to JSON -> push to S3  

### Example (truncated to six MPs per cluster) output
```json
{
    "Clusters": {
        "4747": {
            "PartyCounts": {
                "Social Democratic & Labour Party": 2,
                "Alba Party": 2,
                "Independent": 2,
                "Scottish National Party": 44,
                "Plaid Cymru": 3
            },
            "MPs": [
                {
                    "Name": "Hywel Williams",
                    "Party": "Plaid Cymru"
                },
                {
                    "Name": "Pete Wishart",
                    "Party": "Scottish National Party"
                },
                {
                    "Name": "Stewart Hosie",
                    "Party": "Scottish National Party"
                },
                {
                    "Name": "Angus Brendan MacNeil",
                    "Party": "Scottish National Party"
                },
                {
                    "Name": "Jonathan Edwards",
                    "Party": "Independent"
                },
                {
                    "Name": "Kirsty Blackman",
                    "Party": "Scottish National Party"
                }
            ]
        },
        "4645": {
            "PartyCounts": {
                "Conservative": 3,
                "Sinn Féin": 7,
                "Labour": 1,
                "Speaker": 1
            },
            "MPs": [
                {
                    "Name": "Dame Eleanor Laing",
                    "Party": "Conservative"
                },
                {
                    "Name": "Sir Christopher Chope",
                    "Party": "Conservative"
                },
                {
                    "Name": "Dame Rosie Winterton",
                    "Party": "Labour"
                },
                {
                    "Name": "Sir Lindsay Hoyle",
                    "Party": "Speaker"
                },
                {
                    "Name": "Mr Nigel Evans",
                    "Party": "Conservative"
                },
                {
                    "Name": "Michelle Gildernew",
                    "Party": "Sinn Féin"
                }
            ]
        },
        "4529": {
            "PartyCounts": {
                "Conservative": 97,
                "Democratic Unionist Party": 5
            },
            "MPs": [
                {
                    "Name": "Mrs Theresa May",
                    "Party": "Conservative"
                },
                {
                    "Name": "Sir Bernard Jenkin",
                    "Party": "Conservative"
                },
                {
                    "Name": "Sir Roger Gale",
                    "Party": "Conservative"
                },
                {
                    "Name": "Sir Paul Beresford",
                    "Party": "Conservative"
                },
                {
                    "Name": "Sajid Javid",
                    "Party": "Conservative"
                },
                {
                    "Name": "Boris Johnson",
                    "Party": "Conservative"
                }
            ]
        },
        "4522": {
            "PartyCounts": {
                "Conservative": 263,
                "Independent": 1,
                "Democratic Unionist Party": 3
            },
            "MPs": [
               {
                    "Name": "Rishi Sunak",
                    "Party": "Conservative"
                },
                {
                    "Name": "Will Quince",
                    "Party": "Conservative"
                },
                {
                    "Name": "Mr Mark Francois",
                    "Party": "Conservative"
                },
                {
                    "Name": "Priti Patel",
                    "Party": "Conservative"
                },
                {
                    "Name": "Penny Mordaunt",
                    "Party": "Conservative"
                },
                {
                    "Name": "Grant Shapps",
                    "Party": "Conservative"
                }
            ]
        },
        "483": {
            "PartyCounts": {
                "Green Party": 1,
                "Alliance": 1,
                "Labour": 172,
                "Labour (Co-op)": 25,
                "Independent": 2,
                "Liberal Democrat": 11
            },
            "MPs": [
              {
                    "Name": "Keir Starmer",
                    "Party": "Labour"
                },
                {
                    "Name": "Dr Alan Whitehead",
                    "Party": "Labour"
                },
                {
                    "Name": "Dame Margaret Hodge",
                    "Party": "Labour"
                },
                {
                    "Name": "Edward Miliband",
                    "Party": "Labour"
                },
                {
                    "Name": "Ms Harriet Harman",
                    "Party": "Labour"
                },
                {
                    "Name": "Ms Diane Abbott",
                    "Party": "Labour"
                }
            ]
        }
    }
}

```
