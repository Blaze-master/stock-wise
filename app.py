from mysql.connector import connect

DB = "store_inventory_db"
TABLES = ("sales", "purchases", "products", "customers", "suppliers")

connection = connect(
        host="localhost",
        user="root",
        password="root",
        database=DB
    )
cur = connection.cursor()

# Functions that directly execute SQL statements
# Gets the columns of a table
def getTableColumns(cursor, tb_name):
    cursor.execute(f"""
        SHOW COLUMNS FROM {tb_name}
    """)
    return cursor.fetchall()

# Adds a record to a table
def addTableRecord(cursor, tb_name, columns, fields):
    cursor.execute(f"""
        INSERT INTO {tb_name} ({",".join(columns)}) VALUES {tuple(fields)}
""")
    connection.commit()

# Searches for a record in a table
def searchTable(cursor, tb_name, field, value):
    cursor.execute(f"""
        SELECT * FROM {tb_name} WHERE LOWER({field}) LIKE '%{value.lower()}%'
""")
    return cursor.fetchall()

# Deletes a record from a table
def deleteTableRecord(cursor, tb_name, id):
    cursor.execute(f"""
        DELETE FROM {tb_name} WHERE {tb_name[:-1]+"_id"} = {id}
""")
    connection.commit()

# Updates a record in a table
def updateTableRecord(cursor, tb_name, id, field, value):
    cursor.execute(f"""
        UPDATE {tb_name} SET {field} = '{value}' WHERE {tb_name[:-1]+"_id"} = {id}
""")
    connection.commit()


# Functions that provide CRUD functionality interface
# Adds a record
def addRecord(cursor, tb_name, columns):
    fields = []
    colnames = []
    for col in columns[1:]:
        print("Enter", col[0])
        colnames.append(col[0])
        fields.append(input())
    addTableRecord(cursor, tb_name, tuple(colnames), fields)

# Views a record by id
def viewRecord(cursor, tb_name):
    print(f"Enter the {tb_name[:-1]} id")
    id = input()
    record = searchTable(cursor, tb_name, tb_name[:-1]+"_id", id)
    if len(record) == 0:
        print("Record not found")
    else:
        print(record[0])

# Searches for a record by a non pk field
def searchRecords(cursor, tb_name, columns):
    print("Enter the search field")
    for i,col in enumerate(columns[1:]):
        print(str(i+1)+".", col[0])
    field = int(input())
    print("Enter the search value")
    value = input()
    results = searchTable(cursor, tb_name, columns[field][0], value)
    print(len(results), "result(s) found")
    for res in results:
        print(res)

# Deletes a record
def deleteRecord(cursor, tb_name):
    print(f"Enter the {tb_name[:-1]} id")
    id = input()
    record = searchTable(cursor, tb_name, tb_name[:-1]+"_id", id)
    if len(record) == 0:
        print("Record not found")
        return 0
    else:
        print(record[0])
    print("Are you sure you want to delete this record?")
    print("1. Yes")
    print("2. No")
    choice = int(input())
    if choice == 1:
        deleteTableRecord(cursor, tb_name, id)

# Updates a record
def updateRecord(cursor, tb_name, columns):
    print(f"Enter the {tb_name[:-1]} id")
    id = input()
    record = searchTable(cursor, tb_name, tb_name[:-1]+"_id", id)
    if len(record) == 0:
        print("Record not found")
        return 0
    else:
        print(record[0])
    print("Enter the field to be updated")
    for i,col in enumerate(columns[1:]):
        print(str(i+1)+".", col[0])
    field = int(input())
    print("Enter the new value")
    value = input()
    updateTableRecord(cursor, tb_name, id, columns[field][0], value)


# Selects a CRUD option
def selectOption(opt, cursor, tb_name, columns):
    if opt==1:
        addRecord(cursor, tb_name, columns)
    if opt==2:
        viewRecord(cursor, tb_name)
    if opt==3:
        searchRecords(cursor, tb_name, columns)
    if opt==4:
        deleteRecord(cursor, tb_name)
    if opt==5:
        updateRecord(cursor, tb_name, columns)

# Interface for tables with only CRD functionality
def crdTable(menu, cursor):
    tb_name = TABLES[menu]
    columns = getTableColumns(cursor, tb_name)
    print((tb_name.upper()+" TABLE").center(50, "-"))
    print(f"1. Add a {tb_name[:-1]}")
    print(f"2. View a {tb_name[:-1]} record (by id)")
    print(f"3. Search for a {tb_name[:-1]} record")
    print(f"4. Delete a {tb_name[:-1]} record")
    print("Any other number to go back")
    opt = int(input())
    if opt < 1 or opt > 4:
        return 0
    selectOption(opt, cursor, tb_name, columns)
    crdTable(menu, cursor)

# Interface for tables with CRUD functionality
def crudTable(menu, cursor):
    tb_name = TABLES[menu]
    columns = getTableColumns(cursor, tb_name)
    print((tb_name.upper()+" TABLE").center(50, "-"))
    print(f"1. Add a {tb_name[:-1]}")
    print(f"2. View a {tb_name[:-1]} record (by id)")
    print(f"3. Search for a {tb_name[:-1]} record")
    print(f"4. Delete a {tb_name[:-1]} record")
    print(f"5. Edit a {tb_name[:-1]} record")
    print("Any other number to go back")
    opt = int(input())
    if opt < 1 or opt > 5:
        return 0
    selectOption(opt, cursor, tb_name, columns)
    crudTable(menu, cursor)


# Main menu
def main(cursor):
    print("STORE INVENTORY".center(50, "-"))
    for i,tb in enumerate(TABLES):
        print(str(i+1)+".", tb[:-1].capitalize(), "Records")
    print("Any other number to exit")
    menu_opt = int(input())-1
    if menu_opt >= 0 and menu_opt <= 1:
        crdTable(menu_opt, cursor)
        main(cursor)
    if menu_opt > 1 and menu_opt <= 4:
        crudTable(menu_opt, cursor)
        main(cursor)

main(cur)

connection.commit()
connection.close()