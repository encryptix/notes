from db import DB

def application(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return ["Hell0 World! "]

class Notes:
    database = "NOTES"
    note_id = "id"
    data = "data"

    def __init__(self):
        self.DB = DB(self.database, self.note_id)

    def select(self, row_id):
        row = self.DB.select_one(row_id, [self.data])
        if row:
            return row
        else:
            return "<No_Note>"
    
    def update(self, row_id, text):
        if self.DB.update(row_id,[self.data],[text]):
            return "<Success>"
        else:
            return "<Error>"

    def add_row(self,text):
        self.DB.insert([self.data],[text])

    def remove_row(self, row_id):
        if self.DB.remove(row_id):
            return "<Success>"
        else:
            return "<Error>"

notes = Notes()
print notes.select(2)

#notes.add_row("test message")
print notes.update(2, ["hello w0rld"])
