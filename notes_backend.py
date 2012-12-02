from db import DB

class Notes:
    database = "NOTES"
    note_id = "id"
    data = "data"

    def __init__(self):
        self.DB = DB(self.database, self.note_id)

    def index(self):
        return self.DB.select_all([self.note_id])

    def select_note(self, note_id):
        row = self.DB.select_one(note_id, [self.data])
        if row:
            return str(row[0])
        return None
    
    def update_note(self, note_id, text):
        return self.DB.update(note_id,[self.data],[text])

    def add_note(self,text):
        return self.DB.insert([self.data],[text])

    def remove_note(self, note_id):
        return self.DB.remove(note_id)