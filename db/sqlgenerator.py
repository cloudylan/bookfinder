
import io

file = io.open("db_design.txt", "r")

tableName = ""

sql_create_table = "CREATE TABLE %s (%s)"


def get_data_type(doc_type):

    if doc_type == 'INT':
        dbtype = 'INTEGER'
    elif doc_type == 'DOUBLE':
        dbtype = 'REAL'
    elif doc_type == 'BLOB':
        dbtype = 'BLOB'
    else:
        dbtype = doc_type
    return dbtype


table_start = False
table_end = False
column_string = ''
sql_list = []


for line in file.readlines():
    content = line.strip()
    if content.endswith(':'):
        tableName = content[:content.index(':')]
        print(tableName)
        table_start = True
    elif content == '':
        continue
    elif not content.endswith('.'):
        if not table_start:
            column_string += ', '
        count = content.count(':')
        if count > 0:
            index = content.index(':')
            column_string += content[:index] + ' ' + get_data_type(content[index+1:])
        else:
            column_string += content + ' ' + 'TEXT'
        table_start = False

    elif content.endswith('.'):

        sql_list.append(sql_create_table % (tableName, column_string))
        column_string = ''
        tableName = ''
        table_end = True

    else:
        continue

print('==============================================================')
for sql in sql_list:
    print(sql)
