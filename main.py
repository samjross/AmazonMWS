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
    returns a list of lists of listings
    each sublist contains 4 values:
    sku, asin, price, quantity
    [
    [01100, 2067166263, 4.49, 5],
    [01325, 1906261776, 4.49, 22]
    ]

    alternatively, _GET_MERCHANT_LISTINGS_DATA_ returns a much bigger list of properties
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
    csv_reader = csv.reader(temp_file, dialect=AmazonCSVDialect)
    #csv_reader.next()
    listings = [line for line in csv_reader]
    temp_file.close()
    return listings


listings = request_wait_get_and_parse_flat_file()
for listing in listings:
    print listing
