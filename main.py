from mws import mws
from jSonCredentials import Credentials
import csv


class AmazonCSVDialect(csv.Dialect):
    delimiter = '\t'
    quotechar = '"'
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL


credentials = Credentials()

api = mws.Reports(access_key=credentials.AccessKey, secret_key=credentials.SecretKey,
                  account_id=credentials.AccountID, region='UK')


def request_flat_file():
    request = api.request_report(report_type='_GET_FLAT_FILE_OPEN_LISTINGS_DATA_',
                                 marketplaceids=(credentials.MarketplaceID,))


def get_request_list():
    request_list = api.get_report_request_list()
    # what I'm going to need to do is, when I make a request I need to store the report ID.
    # Then, I check every now and then if that report ID is 'done'
    # if it is, use api.get_report(generatedreportId) to get the report
    # will see what happens after that...
    for report in request_list.parsed.ReportRequestInfo:
        print "RequestID: %-11s| GeneratedID: %-12s| Type: %-45s| Status: %-8s| " \
              "DateSubmitted: %s" % (
                  report.ReportRequestId, report.GeneratedReportId, report.ReportType,
                  report.ReportProcessingStatus, report.SubmittedDate
              )


def parse_report(generated_report_id):
    report = api.get_report(generated_report_id)
    temp_file = open('report.txt', 'w')
    temp_file.write(report.original.replace('\r\n', '\n'))
    temp_file.close()
    temp_file = open('report.txt', 'r')
    csv_reader = csv.reader(temp_file, dialect=AmazonCSVDialect)
    csv_reader.next()
    listings = [line for line in csv_reader]
    temp_file.close()
    return listings


listings = parse_report('38270919104')
pass
