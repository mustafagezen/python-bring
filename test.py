from lib.bring import Bring

def main():
  # Bring object
  bring = Bring()

  # Tracking test
  tracking = bring.tracking("TESTPACKAGE-AT-PICKUPPOINT")

  # Returns DATA(WEIGHT_KG, STATUS, CITY, DESCRIPTION, COUNTRY, COUNTRY_CODE, UNIT_TYPE, POSTAL_CODE, SIGNATURE, RAW)
  print str(tracking.RAW.consignmentSet[0]["totalWeightInKgs"])

  # Postal test
  postal = bring.postal("NO", 5055)

  # Returns DATA(RESULT, POSTAL_TYPE, RAW)
  print postal.RESULT

  # Nearest pickup point - POSTAL
  pickup = bring.pickup(3041)

  # Returns DATA(NAME, ADDRESS, POSTAL, CITY, COUNTRY_CODE, COUNTY, VISITING_ADDRESS, VISITING_POSTAL, LOCATION_DESCRIPTION, OPENING_HOURS_NO, OPENING_HOURS_EN, RAW)
  print pickup.NAME

  # Nearest pickup point - GEO
  pickup = bring.pickup(None, [59.7263078,10.2250463])
  print pickup.NAME



if __name__ == "__main__":
  main()
