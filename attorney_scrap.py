import sys
import time
import json
from random import randint
import requests

# from case.models import Case

AUTH_TOKEN = "8a66336e94023116a37e07a2bbacb432da93aa18"
# USERNAME = "sidharth.shah"
# PASSWORD = "Glum348Mend84"

# Utility Functions


def fetch_api(url):
    token = f"Token {AUTH_TOKEN}"
    headers = {"Authorization": token}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            parsed_response = json.loads(response.content)
            print("Parsed Response: ", parsed_response)
            return parsed_response
    except Exception as error:
        print(f"An Error Occurred: {error}")
        sys.exit()


MAX_CASES = 2


def fetch_parties(court_id, docket_number):
    """
    This will hit end point like: https://www.courtlistener.com/api/rest/v4/search/?q=25-cv-03069&court=flmd&type=d&order_by=dateFiled%20desc
    """
    results = []
    url = f"https://www.courtlistener.com/api/rest/v4/search/?q={docket_number}&court={court_id}&type=d&order_by=dateFiled%20desc"
    try:
        parsed_response = fetch_api(url)
    except Exception as error:
        print(f"An Error Occurred: {error}")

    # Function to get "Party ID"
    for current in parsed_response["results"]:
        if "party_id" in current:
            print("Party Id: ", current["party_id"])
            return current["party_id"]
    return results


doc_num = "25-cv-03069"
cid = "flmd"

fetch_parties(doc_num, cid)


def fetch_parties_and_attorneys(party_ids):
    """
    This will hit end point like: https://www.courtlistener.com/api/rest/v4/parties/16653042/
    """
    results = []
    for current in party_ids:
        url = f"https://www.courtlistener.com/api/rest/v4/parties/{current}/"
        try:
            parsed_response = fetch_api(url)
        except Exception as error:
            print(f"An Error Occurred: {error}")

        party_type = "Plaintiff"
        if "party_types" in parsed_response:
            party_type = parsed_response["party_types"][0]["name"]
        name = parsed_response["name"]

        attorney_ids = []
        if "attorneys" in parsed_response:
            for current_attorney in parsed_response["attorneys"]:
                attorney_ids.append(current_attorney["attorney_id"])

        row = {"name": name, "party_type": party_type, "attorney_ids": attorney_ids}
        results.append(row)
    return results


def fetch_attorney_info(attorney_ids):
    for current in attorney_ids:
        url = f"https://www.courtlistener.com/api/rest/v4/attorneys/{current}/"
        try:
            parsed_response = fetch_api(url)
        except Exception as error:
            print(f"An Error Occurred: {error}")
        print(parsed_response)


def fetch_cases_and_metadata(MAX_CASES):
    """
    this function is used to get docket numbers from API call
    """
    initial_url = "https://www.courtlistener.com/api/rest/v4/search/?q=&type=d&order_by=dateFiled%20desc&nature_of_suit=patent"
    try:
        parsed_response = fetch_api(initial_url)
    except Exception as error:
        print(f"An Error Occurred: {error}")

    docket_info = {}
    cases = []
    parties = []
    documents = []

    while (
        not isinstance(parsed_response["next"], type(None)) and len(cases) < MAX_CASES
    ):
        for case in parsed_response["results"]:
            if len(cases) >= MAX_CASES:
                break
            if case["docket_id"] not in docket_info:
                docket_info[case["docket_id"]] = case["docketNumber"]
                case_info = {}
                case_info["Case Name"] = case["caseName"]
                case_info["Case ID"] = case["docketNumber"]
                case_info["District Court"] = case["court"]
                case_info["Assigned To"] = case["assignedTo"]
                case_info["Referred To"] = case["referredTo"]
                case_info["Court Abbr"] = case["court_id"]
                case_info["Date Filed"] = case["dateFiled"]
                case_info["CL Docket ID"] = case["docket_id"]
                case_info["Date Terminated"] = case["dateTerminated"]
                case_info["Cause"] = case["cause"]
                case_info["Nature of Suit"] = case["suitNature"]
                case_info["Jury Demand"] = case["juryDemand"]
                case_info["Date of Last Known Filing"] = case["dateFiled"]
                case_info["Attorney ID"] = case["attorney_id"]
                cases.append(case_info)
                print(f"\n\n2:Number of cases:{len(cases)} and MAX_CASES:{MAX_CASES}")

                if case["attorney"] is not None:
                    for i in range(len(case["attorney"])):
                        attorney = {}
                        attorney["Attorney Name"] = case["attorney"][i]
                        attorney["Attorney ID"] = case["attorney_id"][i]
                        attorney["Case Name"] = case["attorney"][i]
                        attorney["Case ID"] = case["docketNumber"]
                        attorney["Address"] = ""
                        attorney["Party Type"] = ""
                        parties.append(attorney)
                print(f"fetching docket {case['caseName']}")
                time.sleep(randint(3, 10))
                print("Waking up again...")

        if len(cases) >= MAX_CASES:
            break

        try:
            parsed_response = fetch_api(initial_url)
        except Exception as error:
            print(f"An Error Occurred: {error}")

    print(f"Cases Downloaded:{len(cases)}\n")

    return cases, parties, documents


cases, _, _ = fetch_cases_and_metadata(MAX_CASES)

# for item in cases:
#     print(item["Court Abbr"], item["Case ID"], item["Attorney ID"])
#     fetch_attorney_info(item["Attorney ID"])


# for item in Case.objects.exclude(court_abbrevation__name=None).order_by("-id")[:100]:
#     court_id, docket_number = item.court_abbrevation, item.case_id
#     docket_number = docket_number.split(":")[1]
#     parties = fetch_parties(court_id, docket_number)
#     parties_and_attorneys = fetch_parties_and_attorneys(parties)
#     print(parties_and_attorneys)
