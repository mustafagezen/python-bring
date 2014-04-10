import requests, json
from struct import Struct

class Bring(object):
    BRING_TRACKING_API =    "http://sporing.bring.no/sporing.json?q=%s"
    BRING_LOCATION_API =    "http://fraktguide.bring.no/fraktguide/api/postalCode.json?country=%s&pnr=%s"

    def tracking(self, tr_nr):
        """Returns tracking data
            DATA: (WEIGHT_KG, STATUS, CITY, DESCRIPTION, COUNTRY, COUNTRY_CODE, UNIT_TYPE, POSTAL_CODE, SIGNATURE)

            @param :tr_nr Tracking number
        """
        FINAL_URI = self.BRING_TRACKING_API % tr_nr
        REQUEST = requests.get(FINAL_URI)

        JSON = json.loads(REQUEST.text)["consignmentSet"][0]
        PACKAGE_SET = JSON["packageSet"][0]
        EVENT_SET = PACKAGE_SET["eventSet"][0]

        DATA = {
            'WEIGHT_KG': JSON["totalWeightInKgs"],
            'STATUS': EVENT_SET["status"],
            'CITY': EVENT_SET["city"],
            'DESCRIPTION': EVENT_SET["description"],
            'COUNTRY': EVENT_SET["country"],
            'COUNTRY_CODE': EVENT_SET["countryCode"],
            'UNIT_TYPE': EVENT_SET["unitType"],
            'POSTAL_CODE': EVENT_SET["postalCode"],
            'SIGNATURE': EVENT_SET["recipientSignature"]["name"]
        }

        for (i, val) in enumerate(DATA):
            if not DATA[val]:
                DATA[val] = None

        return Struct(DATA)

    def postal(self, country, postal):
        """Returns postal information
            DATA: (RESULT, POSTAL_TYPE)

            @param :country Country Code
            @param :postal Postal code
        """
        FINAL_URI = self.BRING_LOCATION_API % (country, postal)
        REQUEST = requests.get(FINAL_URI)

        JSON = json.loads(REQUEST.text)

        DATA = {
            'RESULT': None,
            'POSTAL_TYPE': None
        }

        if JSON["valid"] == False:
            pass
        else:
            DATA["RESULT"] = JSON["result"]
            DATA["POSTAL_TYPE"] = JSON["postalCodeType"]

        return Struct(DATA)
