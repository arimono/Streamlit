from connection import *

allowed_tables = ["sensor", "demo"]  
allowed_columns = {
        "sensor": ["temp", "humidity"],
        "demo": ["message"]
    }
def checkTables(table_name):
    if table_name not in allowed_tables:
        raise ValueError(f"Invalid table name: {table_name}")
    
def checkCol(table_name,columns):
    if table_name in allowed_columns:
        for col in columns:
            if col not in allowed_columns[table_name]:
                raise ValueError(f"Invalid column: {col} for table {table_name}")
    else:
        raise ValueError(f"No column definition for table: {table_name}")

def update(table_name, columns, values):

    dbCre = mysqlConnect()
    checkTables(table_name)
    checkCol(table_name, columns)
    sqlCursor = dbCre.cursor()
    columns_str = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(values))
    sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
    sqlCursor.execute(sql, values)
    dbCre.commit()
    sqlCursor.close()
    dbCre.close()
    print(sqlCursor.rowcount, "record inserted.")

def select100(table_name):
    dbCre = mysqlConnect()
    checkTables(table_name)  
    sqlCursor = dbCre.cursor(dictionary=True)
    sqlCursor.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 100;")
    result = sqlCursor.fetchall()
    column_names = list(result[0].keys()) if result else []
    sqlCursor.close()
    dbCre.close()
    return result, column_names