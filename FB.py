from facebookads.adobjects.adaccount import AdAccount
from facebookads.api import FacebookAdsApi
import Parser
from decimal import *
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

access_token = 'YOUR TOKEN HERE'
ad_account_id = 'YOUR ID HERE'
app_secret = 'YOUR SECRET HERE'
FacebookAdsApi.init(access_token=access_token)

desired_start_date = raw_input('Enter Start date (YYYYY-MM-DD)')
desired_end_date = raw_input('Enter End date (YYYY-MM-DD)')

month = "Cost"

if '-08-' in desired_start_date:
    month = "August"
elif '-09-' in desired_start_date:
    month = "September"

print(month)

fields = [
    'spend', 'campaign_name'
]
params = {
    'level': 'campaign',
    'filtering': [],
    'breakdowns': [],
}

try:
    params['time range']['since'] = desired_start_date
except KeyError:
    params['time range'] = {'since': desired_start_date}
try:
    params['time range']['until'] = desired_end_date
except KeyError:
    params['time range'] = {'until': desired_end_date}

print type(params)


json_key = json.load(open('creds.json'))
scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

file1 = gspread.authorize(credentials)
sheet = file1.open("test_budgets_export").sheet1

cell_list = sheet.range('A1:A20')
cell_list2 = sheet.range('B2:B20')

print cell_list
modified_list = unicode(cell_list)
print type(modified_list)


def getvalues():
    tmp_string = str(AdAccount(ad_account_id).get_insights(
        fields=fields,
        params=params,
    )).split('<AdsInsights>')
    tmp_string = str(tmp_string)[7:][:-3]

    i = 2
    list_of_jsons = str(tmp_string).split(', \'')
    for jsonchik in list_of_jsons:
        jsonchik = jsonchik.replace('\\n    ', '')
        jsonchik = jsonchik.replace('\\n', '')
        try:
            j = json.loads(jsonchik)
            cn = j['campaign_name']
            sp = j['spend']
            print cn
            print type(cn)
            cost = Decimal(sp) * Parser.q
            print cost
            sheet.update_acell('B1', month)
            if modified_list.find(cn) != -1:
                print ("String in the string!")
            else:
                sheet.update_acell('A' + str(i), cn)

            sheet.update_acell('B' + str(i), cost)

            i += 1
        except ValueError:
            'stupid error, everything works'


getvalues()


if cell_list2:
    print ("Not empty column")
