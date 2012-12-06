from helpers import FormHelpers
from helpers import NumberHelpers
from helpers import GeneralHelpers
from notes_backend import Notes

def do_index():
    n = Notes(None)
    #will returns a list of row_id's/None
    rows =  n.index()
    return_str = "{\"notes\": ["
    for row in rows:
        return_str += "{"+GeneralHelpers.createJSONEntry("noteID",str(row[0]))+","
        return_str += GeneralHelpers.createJSONEntry("noteName",str(row[1]))+"},"

    #if there was content parse off the last ,
    if rows:
         return_str = return_str[:-1]
    return return_str+"]}"

def do_select(n):
    #returns note/None
    note = n.select_note()
    if note:
        return "{"+GeneralHelpers.createJSONEntry("noteID",n.note_id)+", "+GeneralHelpers.createJSONEntry("note",note)+"}"
    return "<no_note>"

def do_update(n, text):
    #returns boolean
    if n.update_note(text):
        return "<success>"
    else:
        return "<error>"

def do_update_name(n,name):
    #returns boolean
    if n.update_note_name(name):
        return "<success>"
    else:
        return "<error>"

def do_delete(n):
    #returns boolean
    if n.remove_note():
        #return the note id
        return "{"+GeneralHelpers.createJSONEntry("noteID",n.note_id)+"}"
    else:
        return "<error>"

def do_add_note(data,name):
    n = Notes()
    note_id = n.add_note(data,name)
    return "{"+GeneralHelpers.createJSONEntry("noteID",n.note_id)+", "+GeneralHelpers.createJSONEntry("noteName",name)+"}"

def do_lock(n,new_pass):
    return n.set_password(new_pass)

def do_unlock(n, current_pass):
    if n.check_password(current_pass):
        return n.set_password(current_pass,"")
    else:
        return "<locked>"


def application(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    # When the method is POST the query string will be sent
    # in the HTTP request body which is passed by the WSGI server
    # in the file like wsgi.input environment variable.
    request_body = environ['wsgi.input'].read(request_body_size)
    d = FormHelpers.get_form(request_body)

    action = FormHelpers.get_input(d,'action')

    response_body = "<error_interface>"
    #index,view,add,delete,update
    if action == "index":
        response_body = do_index()
    
    elif action == "add":
        data = FormHelpers.get_input(d,'data')
        name = FormHelpers.get_input(d,'name')
        if data and len(data) > 0 and name and len(name) >0:
            response_body = do_add_note(data,name)
    #The rest of these require the notes to be unlocked
    note_id = FormHelpers.get_input(d,'id')   
    if NumberHelpers.is_positive_integer(note_id):
        note = Note(note_id)
        if note.is_locked:
            if action == "unlock":
                if password and len(password) > 0:
                    response_body = do_unlock(note,password)
            else:
                response_body = "<locked>"

        elif action =="view":
            response_body = do_select(note)

        elif action == "delete":
            response_body = do_delete(note)
            
        elif action == "update":
            data = FormHelpers.get_input(d,'data')
            if data and len(data) > 0:
                response_body = do_update(note,data)       
        
        elif action=="update_name":
            name = FormHelpers.get_input(d,'name')
            if name and len(name) > 0:
                response_body = do_update_name(note,name)

        elif action=="lock":
            password = FormHelpers.get_input(d,'password')
            if password and len(password) > 0:
                response_body = do_lock(note,password)

    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'),('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body]