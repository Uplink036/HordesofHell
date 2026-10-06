from .offerings import OfferingsRule

__all__ = ["OfferingsRule"]

def run_all_rules():
    OfferingsRule().validate()