from db import DB

class Notes:
    #Database names
    database = "NOTES"
    note_id = "id"
    data = "data"
    name= "name"
    password = "password"
    #Actual Note ID
    noteID = None

    def __init__(self,noteID):
        self.DB = DB(self.database, self.note_id)
        self.noteID = noteID
    def note_id():
        return noteID
    
    def index(self):
        return self.DB.select_all([self.note_id,self.name])

    def select_note(self):
        row = self.DB.select_one(noteID, [self.data])
        if row:
            return str(row[0])
        return None
    
    def update_note(self, text):
        return self.DB.update(noteID,[self.data],[text])
    
    def update_note_name(self,name):
        return self.DB.update(noteID,[self.name],[name])

    def add_note(self,text,name):
        return self.DB.insert([self.data,self.name],[text,name])

    def remove_note(self):
        return self.DB.remove(noteID)

    def check_password(self, password):
        actual_password = self.DB.select_one(noteID,[self.password])
        print actual_password
        if password == actual_password:
            return True
        return False

    def set_password(self,new_pass):
        return self.DB.update(noteID,[self.password],[new_pass])

    def is_locked(self):
        password = self.DB.select_one(noteID,[self.password])
        if password==None or len(password) ==0:
            return False
        else:
            return True
