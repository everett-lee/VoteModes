import json
import logging
import os
import sys
from typing import Any, Dict, Union

import requests

from ..boto3_helpers.client_wrapper import get_table

"""
In the current set up MPs are both downloaded and put to the datastore manually using the script below.
"""
logging.basicConfig(level=logging.INFO)

URL_GET_MPS_BASE = (
    "http://data.parliament.uk/membersdataplatform/services/mnis/members/"
)
URL_GET_MPS_QUERY = "query/House=Commons%7CIsEligible=true%7Ccommonsmemberbetween={start_date}and{end_date}/"
START_DATE = "2019-12-15"
END_DATE = "2021-05-03"
MP_ELECTION_YEAR = os.getenv("ELECTION_YEAR", "2019")


def get_fields_of_interest(mp: Dict[str, Any]) -> Dict[str, Union[int, str]]:
    return {
        "MemberId": int(mp["@Member_Id"]),
        "Name": mp["DisplayAs"],
        "Party": mp["Party"]["#text"],
    }


def download_active_mp_list_to_file(
    start_date: str = START_DATE, end_date: str = END_DATE
) -> None:
    """
    Downloads MPs to file.
    The resulting file is added to the database manually, as this data is
    treated as static until the next election.
    """

    full_url = URL_GET_MPS_BASE + URL_GET_MPS_QUERY.format(
        start_date=start_date, end_date=end_date
    )
    headers = {"content-type": "application/json"}
    response = requests.get(full_url, headers=headers)

    response_text = response.content.decode("utf-8-sig")
    parsed = json.loads(response_text)

    with open("raw/rawMPList", "w") as f:
        all_members = parsed["Members"]["Member"]
        members_with_id_and_name = [get_fields_of_interest(mp) for mp in all_members]

        f.write('{"Data": ')
        f.write(json.dumps(members_with_id_and_name))
        f.write("}")


def write_to_db(table_name: str):
    table = get_table(table_name)
    with open("raw/rawMPList", "r") as f:
        mp_data = json.loads(f.read())
        data = mp_data["Data"]
        logging.info(f"Writing {len(data)} MPs")
        for row in data:
            row["MPElectionYear"] = int(MP_ELECTION_YEAR)
            row["Votes"] = []
            table.put_item(Item=row)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "refresh":
        logging.info("Performing fresh download")
        download_active_mp_list_to_file()

    write_to_db("MPs")
