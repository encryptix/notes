from db import DB

class Notes:
    database = "NOTES"
    note_id = "id"
    data = "data"

    def __init__(self):
        self.DB = DB(self.database, self.note_id)

    def index(self):
        rows = self.DB.select_all([self.note_id])
        return_str = "<notes>"
        for row in rows:
            return_str += "<note_id>"+str(row[0])+"</note_id>"
        return return_str+"</notes>"

    def select_note(self, note_id):
        row = self.DB.select_one(note_id, [self.data])
        if row:
            return str(row[0])
        else:
            return "<no_note>"
    
    def update_note(self, note_id, text):
        if self.DB.update(note_id,[self.data],[text]):
            return "<success>"
        else:
            return "<error>"

    def add_note(self,text):
        return self.DB.insert([self.data],[text])

    def remove_note(self, note_id):
        if self.DB.remove(note_id):
            return "<success>"
        else:
            return "<error>"