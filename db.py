import sqlite3

class DB:
    def __init__(self, db_name, id_col):
        self.db_name = str(db_name)
        self.db_file = str(db_name.lower()+".db")
        self.id_column = str(id_col)
        self.conn = None
        self.cursor = None
        
    def init_cursor(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()

    def release_conn(self):
        if self.conn:
            self.conn.close()
        self.conn = None
        self.cursor = None

    def select_one(self, row, columns):
        columns_string = ""
        for column in columns:
            columns_string += column+", "
        #remove last ,
        columns_string = columns_string[:-2]

        statement = "SELECT "+columns_string+" FROM "+self.db_name+" WHERE "+self.id_column+" = "+str(row)
        self.init_cursor()
        self.cursor.execute(statement)
        row = self.cursor.fetchone()
        self.release_conn()

        return row

    def insert(self,columns,data):
        print "todo"
        self.init_cursor()
        statement = "insert into "+self.db_name+" ( "+self.id_column+" , "+columns[0]+") values ( ? , ? )"
        self.cursor.execute(statement, [None, str(data[0])])

        row_id = self.cursor.execute('SELECT last_insert_rowid()')
        self.conn.commit()
        self.release_conn()
        return row_id

    def update(self, row_id, columns, data):
        #columns and data are lists which map to each other
        self.init_cursor()
        statement = "update "+self.db_name+" set "+columns[0]+" = ? WHERE "+self.id_column+" = ?"
        print statement
        print str(row_id) + " : "+str(data[0])
        self.cursor.execute(statement, [str(data[0]), str(row_id)])
        self.conn.commit()
        self.release_conn()
        return True  
        #return column id      
    
    def remove(self, row_id):
        query = "DELETE FROM "+self.db_name+" WHERE "+self.id_column+" = ?"
        self.init_cursor()
        self.cursor.execute(query,str(row_id))
        self.conn.commit()
        self.release_conn()
        return True