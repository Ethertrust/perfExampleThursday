import gspread

gc = gspread.service_account(filename="C:\\Users\\HYPER\\PycharmProjects\\Classes B\\Thursday\\8\\creds_newexample.json")

def read(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME):
    sh = gc.open_by_key(SAMPLE_SPREADSHEET_ID)
    get_values = sh.values_get(range=SAMPLE_RANGE_NAME + '!A:A')['values']
    return [val[0] for val in get_values[2:]]

def write(data, SAMPLE_SPREADSHEET_ID, sheetname):
    sh = gc.open_by_key(SAMPLE_SPREADSHEET_ID)
    # worksheet = sh.worksheet(sheetname)
    sh.values_update(sheetname+'!A3', #b Performance!A3
                        params={'valueInputOption': 'USER_ENTERED'},
                        body={
                            'values': data
                        })

if __name__ == '__main__':
    # for val in read('13UIj4U0ry16Ib5W6dWMrtCpNyv-5TW5hUMzIJlkIFb4', 'b Performance'):
    #     print(val[0])
    data = [['Стрельцов Андрей Александрович', '', "'+", "'+", '', "'+", "'+", "'+", "'+", "'+", '', '', '=HYPERLINK("https://moodle.surgu.ru/mod/quiz/review.php?attempt=1562311#question-1745693-5"; "2024-03-05 23:34:08")', '', '', '', ''],
            ['Стрельцов Андрей Александрович', '', "'+", "'+", '', "'+", "'+", "'+", "'+", "'+", '', '', '2024-03-05 23:34:08', '', '', '', '']]
    write(data, '13UIj4U0ry16Ib5W6dWMrtCpNyv-5TW5hUMzIJlkIFb4', 'b Performance')