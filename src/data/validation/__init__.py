from data.validation.offerings import OfferingsRule

__all__ = ["OfferingsRule"]

def run_all_rules():
    OfferingsRule().validate()

if __name__ == "__main__":
    run_all_rules()