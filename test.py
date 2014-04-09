from lib.bring import Bring

def main():
    bring = Bring()
    tracking = bring.tracking("TESTPACKAGE-AT-PICKUPPOINT")
    print tracking.CITY

    postal = bring.postal("NO", 5055)
    print postal.RESULT

if __name__ == "__main__":
    main()
