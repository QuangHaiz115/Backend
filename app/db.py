import pyodbc

def get_connection():
    conn_str = "Driver={SQL Server};Server=QUANGHAI;Database=NhaHangDb;Trusted_Connection=yes"
    return pyodbc.connect(conn_str)
