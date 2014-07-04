from mws import mws
from jSonCredentials import Credentials
import csv
import time


class AmazonCSVDialect(csv.Dialect):
    delimiter = '\t'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\n'
    quoting = csv.QUOTE_MINIMAL


credentials = Credentials()

api = mws.Reports(access_key=credentials.AccessKey, secret_key=credentials.SecretKey,
                  account_id=credentials.AccountID, region='UK')


def request_wait_get_and_parse_flat_file():
    """
    _GET_FLAT_FILE_OPEN_LISTINGS_DATA_
    returns a list of dictionaries of listins
    each dictionary is made of the following keys:

    'sku', 'asin', 'price', 'quantity'
    -----------------------------------------------------------------------------------

    alternatively, _GET_MERCHANT_LISTINGS_DATA_ returns a much bigger list of properties
    here are the keys:

    'zshop-boldface', 'pending-quantity', 'seller-sku', 'zshop-browse-path',
    'item-condition', 'product-id', 'asin2', 'asin3', 'asin1', 'image-url',
    'item-description', 'product-id-type', 'open-date', 'will-ship-internationally',
    'listing-id', 'price', 'add-delete', 'zshop-storefront-feature', 'item-note',
    'item-name', 'zshop-category1', 'expedited-shipping', 'zshop-shipping-fee',
    'bid-for-featured-placement', 'item-is-marketplace', 'fulfillment-channel', 'quantity'

    The important ones:
    'seller-sku', 'quantity', 'price', 'asin1',
    'item-name', 'item-condition', 'fulfillment-channel'
    """
    request = api.request_report(report_type='_GET_MERCHANT_LISTINGS_DATA_',
                                 marketplaceids=(credentials.MarketplaceID,))
    ready = False
    while not ready:
        time.sleep(60)
        ready = check_if_ready(request.parsed.ReportRequestInfo.ReportRequestId)
    return get_and_parse_report(ready[1])


def get_request_list(request_ids=None):
    if request_ids is None:
        request_list = api.get_report_request_list()
    else:
        request_list = api.get_report_request_list(request_ids)
    report = request_list.parsed.ReportRequestInfo
    return report


def check_if_ready(request_id):
    report = get_request_list((request_id,))
    if 'DONE' in report.ReportProcessingStatus:
        return True, report.GeneratedReportId
    else:
        return False


def get_and_parse_report(generated_report_id):
    report = api.get_report(generated_report_id)
    temp_file = open('report.txt', 'w')
    temp_file.write(report.original.replace('\r\n', '\n'))
    temp_file.close()
    temp_file = open('report.txt', 'r')
    listings = read_amazon_csv(temp_file)
    temp_file.close()
    return listings


def read_amazon_csv(csv_file):
    csv_reader = csv.reader(csv_file, dialect=AmazonCSVDialect)
    keys = csv_reader.next()
    listings = []
    for line in csv_reader:
        listing_dict = {}
        for index in range(len(line)):
            listing_dict[keys[index]] = line[index]
        listings.append(listing_dict)
    return listings


if __name__ == "__main__":
    listins = request_wait_get_and_parse_flat_file()
    for listing in listins:
        print listing
