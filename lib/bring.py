"""
Made with <3 by Mustafa Gezen (mustafagezen)
The MIT License (MIT)

Copyright (c) 2014 Mustafa Gezen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import requests, json
from struct import Struct

class Bring(object):
  BRING_TRACKING_API =    "http://sporing.bring.no/sporing.json?q=%s"
  BRING_LOCATION_API =    "http://fraktguide.bring.no/fraktguide/api/postalCode.json?country=%s&pnr=%s"
  BRING_POSTAL_API =   "http://fraktguide.bring.no/fraktguide/api/pickuppoint/postalcode/%s.json"
  BRING_POSTAL_GEO_API =   "http://fraktguide.bring.no/fraktguide/api/pickuppoint/location/%s/%s.json"

  def tracking(self, tr_nr):
    """Returns tracking data
    DATA(WEIGHT_KG, STATUS, CITY, DESCRIPTION, COUNTRY, COUNTRY_CODE, UNIT_TYPE, POSTAL_CODE, SIGNATURE) and RAW

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
    'SIGNATURE': EVENT_SET["recipientSignature"]["name"],
    'RAW': json.loads(REQUEST.text),
    'RAW_string': str(json.loads(REQUEST.text))
    }

    for (i, val) in enumerate(DATA):
      if not DATA[val]:
        DATA[val] = None

    return Struct(DATA)

  def postal(self, country, postal):
    """Returns postal information
    DATA(RESULT, POSTAL_TYPE) and RAW

    @param :country Country Code
    @param :postal Postal code
    """
    FINAL_URI = self.BRING_LOCATION_API % (country, postal)
    REQUEST = requests.get(FINAL_URI)

    JSON = json.loads(REQUEST.text)

    DATA = {
    'RESULT': None,
    'POSTAL_TYPE': None,
    'RAW': None,
    'RAW_string': None
    }

    if JSON["valid"] == False:
      pass
    else:
      DATA["RESULT"] = JSON["result"]
      DATA["POSTAL_TYPE"] = JSON["postalCodeType"]
      DATA["RAW"] = json.loads(REQUEST.text)
      DATA["RAW_string"] = str(json.loads(REQUEST.text))

    return Struct(DATA)

  def pickup(self, postal=None, geo=None):
    """Returns the nearest pickup point
    DATA(NAME, ADDRESS, POSTAL, CITY, COUNTRY_CODE, COUNTY, VISITING_ADDRESS, VISITING_POSTAL, LOCATION_DESCRIPTION, OPENING_HOURS_NO, OPENING_HOURS_EN, RAW)

    @param(optional) :postal Postal code
    @param(optional) :geo Geographic location in array, ex. [59.7263078,10.2250463]

    @required :postal or :geo
    """
    DATA = {
      'NAME': None,
      'ADDRESS': None,
      'POSTAL': None,
      'CITY': None,
      'COUNTRY_CODE': None,
      'COUNTY': None,
      'VISITING_ADDRESS': None,
      'VISITING_POSTAL': None,
      'LOCATION_DESCRIPTION': None,
      'OPENING_HOURS_NO': None,
      'OPENING_HOURS_EN': None,
      'RAW': None,
      'RAW_string': None
    }

    if postal != None and geo != None:
      raise Exception("You cannot provide both postal code and geographic locations!")
    elif postal != None:
      FINAL_URI = self.BRING_POSTAL_API % postal
    elif geo != None:
      FINAL_URI = self.BRING_POSTAL_GEO_API % (geo[0], geo[1])
    else:
      raise Exception("Unexpected error")

    REQUEST = requests.get(FINAL_URI)
    JSON = json.loads(REQUEST.text)["pickupPoint"][0]

    DATA["NAME"] = JSON["name"]
    DATA["ADDRESS"] = JSON["address"]
    DATA["POSTAL"] = JSON["postalCode"]
    DATA["CITY"] = JSON["city"]
    DATA["COUNTRY_CODE"] = JSON["countryCode"]
    DATA["COUNTY"] = JSON["county"]
    DATA["VISITING_ADDRESS"] = JSON["visitingAddress"]
    DATA["VISITING_POSTAL"] = JSON["visitingPostalCode"]
    DATA["LOCATION_DESCRIPTION"] = JSON["locationDescription"]
    DATA["OPENING_HOURS_NO"] = JSON["openingHoursNorwegian"]
    DATA["OPENING_HOURS_EN"] = JSON["openingHoursEnglish"]
    DATA["RAW"] = JSON
    DATA["RAW_string"] = str(JSON)

    return Struct(DATA)
