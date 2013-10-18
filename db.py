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

    def select_all(self,columns,constraints,constraint_data,limit):
        columns_string = ""
        for column in columns:
            columns_string += column+", "
        #remove last ,
        columns_string = columns_string[:-2]

        where_string = ""
        if(constraints):
            where_string=" WHERE "
            for constraint in constraints:
                where_string+= constraint+" ? "

        limit_string = ""
        if(limit):
            limit_string = " LIMIT "+str(limit)

        values = []
        for value in constraint_data or []:
            values.append(str(value))

        statement = "SELECT "+columns_string+" FROM "+self.db_name+where_string+limit_string
        print "select statement: "+statement
        self.init_cursor()
        self.cursor.execute(statement,values)
        rows = self.cursor.fetchall()
        self.release_conn()

        return rows

    def insert(self,columns,data):
        #columns and data are lists which map to each other
        columns_string = " ( "+self.id_column+" , "
        value_string = " ( ? ,"

        for column in columns:
            columns_string += column+", "
            value_string += " ? ,"
        #remove last ,
        value_string = value_string[:-2]+" ) "
        columns_string = columns_string[:-2]+" ) "
    
        statement = "insert into "+self.db_name+columns_string +" values "+value_string

        values = []
        values.append(None)

        for value in data:
            values.append(value)

        self.init_cursor()
        self.cursor.execute(statement, values)
        row_id = self.cursor.execute('SELECT last_insert_rowid()').fetchone()
        self.conn.commit()
        self.release_conn()
        
        return str(row_id[0])

    def update(self, row_id, columns, data):
        #columns and data are lists which map to each other
        update_str = "update "+self.db_name+" set "
        for column in columns:
            update_str+=column + " = ? , "
        update_str=update_str[:-2]+" where "+self.id_column+" = ?"

        values = []
        for value in data:
            values.append(str(value))
        values.append(str(row_id))
        
        self.init_cursor()
        self.cursor.execute(update_str, values)
        self.conn.commit()
        self.release_conn()
        return True  
        #return column id      
    
    def remove(self, row_id):
        print "todo"
        query = "DELETE FROM "+self.db_name+" WHERE "+self.id_column+" = ?"
        self.init_cursor()
        #error here when number > 9
        print "DEBUG"
        print query
        print str(row_id)
        print "DEBUG"
        self.cursor.execute(query,[str(row_id)])
        self.conn.commit()
        self.release_conn()
        return True
