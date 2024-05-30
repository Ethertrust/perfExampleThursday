import gs2
import mdb
import pandas
from datetime import datetime as dt
from googleapiclient.discovery import build
from google.oauth2 import service_account


def getxlsnames():
    fiolist = gs2.read('13UIj4U0ry16Ib5W6dWMrtCpNyv-5TW5hUMzIJlkIFb4', 'b Performance')
    return [val for val in fiolist]


def getdata():
    return mdb.selectperfdata()

def resulPerfForm(names):
    performance=[]
    for name in names:
        stPerf = {'FIO': name,
                    'Нулевое': '',
                    'Первое': '',
                    'Второе': '',
                    'Третье': '',
                    'Четвёртое': '',
                    'Упражнение 1': '',
                    'Упражнение 2': '',
                    'Упражнение 3': '',
                    'Упражнение 4': '',
                    'О себе.py': '',
                    'Ошибки': [],
                    'Последняя активность': '',
                    'AllDone': '',
                    'Успех': '',
                    '% Успех': '',
                    'Зачет': ''}
        performance.append(stPerf)
    return performance

def lastActivity(st, row):
    if st['Последняя активность'] == '':
        st['Последняя активность'] = row[9]
    #"2024-03-05 22:47:23"
    if dt.strptime(st['Последняя активность'], "%Y-%m-%d %H:%M:%S") < dt.strptime(row[9], "%Y-%m-%d %H:%M:%S"):
        st['Последняя активность'] = row[9]
        st['att'] = row[13]
        st['quid'] = [row[14], row[4]]

def checkTests(st, row, tries, testnames):
    # №Теста.№Вопроса -> '0.1'  -> Нулевое.1
    key = str(testnames[row[0]][1]) + '.' + str(row[4])
    if not key in tries:
        tries[key] = [row[7], row[13], row[14],  row[4], row[9], row[6]]
    if tries[key][0] != 'complete':
        tries[key] = [row[7], row[13], row[14],  row[4], row[9], row[6]]

def checkErrors(st, tries, testnames):
    #strTry №Теста.№Вопроса -> '0.1'  -> Нулевое.1
    for stTry in tries:
        #Ошибки №Теста.№Вопроса.№Шага
        if tries[stTry][0] != 'complete':
            st['Ошибки'].append(stTry+'.'+tries[stTry][5])
    st['Ошибки'] = ', '.join(st['Ошибки'])

def sumUP(st, tries, testnames):
    for test in testnames:
        complete = False
        key = ''
        for q in range(1, testnames[test][2]+1): #'Нулевое' 1 : 4-> q 1, 2, 3
            key = str(testnames[test][1])+'.'+str(q)
            if key in tries and tries[key][0]=='complete':
                complete = True
                #  # П.В.Ш https://moodle.surgu.ru/mod/quiz/review.php?attempt=1355811#question-1529449-2
                st[testnames[test][0]]= "=HYPERLINK(\"https://moodle.surgu.ru/mod/quiz/review.php?attempt={}#question-{}-{}\"; \"{}\")".format(
                    tries[key][1], tries[key][2], tries[key][3],
                    str(testnames[test][1]) + '.' + str(q) + '.' + tries[key][-1])
        if key in tries and complete:
            st[testnames[test][0]] = "=HYPERLINK(\"https://moodle.surgu.ru/mod/quiz/review.php?attempt={}#question-{}-{}\"; \"{}\")".format(
                tries[key][1], tries[key][2], tries[key][3], '+')


def stPerformance(st, data):
    testnames = {'Нулевое практическое занятие по Python': ['Нулевое', 0, 3],
                'Первое практическое занятие по Python': ['Первое', 1, 5],
                'Второе практическое занятие по Python': ['Второе', 2, 5],
                'Третье практическое занятие по Python': ['Третье', 3, 4],
                'Четвёртое практическое занятие по Python': ['Четвёртое', 4, 7],
                'Упражнение 1': ['Упражнение 1', 5, 4],
                'Упражнение 2': ['Упражнение 2', 6, 4],
                'Упражнение 3': ['Упражнение 3', 7, 4],
                'Упражнение 4': ['Упражнение 4', 8, 5]}
    # №Теста.№Вопроса -> '0.1'  -> Нулевое.1
    tries = {}
# 0 - Тест, 1 - ФИО, 2 - № попытки, 4 - № вопроса, 6 - шаг, 7 - состояние, 9 - дата, 12 - О себе.py, 13 - attempt id, 14 - question usage id
    for row in data:
        if (not row[6]=='0') and row[1] == st['FIO']:
            lastActivity(st, row)
            checkTests(st, row, tries, testnames)
    checkErrors(st, tries, testnames)
    sumUP(st, tries, testnames)
    lastHlink(st)

def lastHlink(student):
    if 'att' in student:
        student['Последняя активность'] = "=HYPERLINK(\"https://moodle.surgu.ru/mod/quiz/review.php?attempt={}#question-{}-{}\"; \"{}\")".format(
                    student['att'], student['quid'][0], student['quid'][1], student['Последняя активность'])

def performance(data, names):
    performance = resulPerfForm(names)
    for st in performance:
        stPerformance(st, data)
    newperformance = []
    newperformance += [list(row.values())[0:-3] for row in performance]
    return newperformance



if __name__ == '__main__':
    data = getdata()
    #credentials = service_account.Credentials.from_service_account_file(filename=sa_file)
    #service = build('sheets', 'v4', credentials=credentials)
    names = getxlsnames()
    # print(names)
    newdata = performance(data, names)
    #gs.write(newdata, '13UIj4U0ry16Ib5W6dWMrtCpNyv-5TW5hUMzIJlkIFb4', 'b Performance')
    print(newdata)