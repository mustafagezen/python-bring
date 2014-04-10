from lib.bring import Bring

def main():
    # Bring object
    bring = Bring()

    # Tracking test
    tracking = bring.tracking("TESTPACKAGE-AT-PICKUPPOINT")

    # You can get this information: (WEIGHT_KG, STATUS, CITY, DESCRIPTION, COUNTRY, COUNTRY_CODE, UNIT_TYPE, POSTAL_CODE, SIGNATURE)
    print tracking.CITY

    # Postal test
    postal = bring.postal("NO", 5055)

    #You can get this information: (RESULT, POSTAL_TYPE)
    print postal.RESULT

if __name__ == "__main__":
    main()
