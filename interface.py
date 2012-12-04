from helpers import FormHelpers
from helpers import NumberHelpers
from helpers import GeneralHelpers
from notes_backend import Notes

def do_index():
    n = Notes()
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

def do_select(note_id):
    n = Notes()
    #returns note/None
    note = n.select_note(note_id)
    if note:
        return "{"+GeneralHelpers.createJSONEntry("noteID",note_id)+", "+GeneralHelpers.createJSONEntry("note",note)+"}"
    return "<no_note>"

def do_update(note_id, text):
    n = Notes()
    #returns boolean
    if n.update_note(note_id,text):
        return "<success>"
    else:
        return "<error>"

def do_update_name(note_id,name):
    n = Notes();
    #returns boolean
    if n.update_note_name(note_id,name):
        return "<success>"
    else:
        return "<error>"

def do_delete(note_id):
    n = Notes()
    #returns boolean
    if n.remove_note(note_id):
        #return the note id
        return "{"+GeneralHelpers.createJSONEntry("noteID",note_id)+"}"
    else:
        return "<error>"

def do_add_note(data,name):
    n = Notes()
    note_id = n.add_note(data,name)
    return "{"+GeneralHelpers.createJSONEntry("noteID",note_id)+", "+GeneralHelpers.createJSONEntry("noteName",name)+"}"

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
    elif action =="view":
        note_id = FormHelpers.get_input(d,'id')
        if NumberHelpers.is_positive_integer(note_id):
            response_body = do_select(note_id)

        
    elif action == "add":
        data = FormHelpers.get_input(d,'data')
        name = FormHelpers.get_input(d,'name')
        if data and len(data) > 0 and name and len(name) >0:
            response_body = do_add_note(data,name)

    elif action == "delete":
        note_id = FormHelpers.get_input(d,'id')
        if NumberHelpers.is_positive_integer(note_id):
            response_body = do_delete(note_id)
        
    elif action == "update":
        note_id = FormHelpers.get_input(d,'id')
        data = FormHelpers.get_input(d,'data')

        if NumberHelpers.is_positive_integer(note_id) and data and len(data) > 0:
            response_body = do_update(note_id,data)       
    
    elif action=="update_name":
        note_id = FormHelpers.get_input(d,'id')
        name = FormHelpers.get_input(d,'name')

        if NumberHelpers.is_positive_integer(note_id) and name and len(name) > 0:
            response_body = do_update_name(note_id,name);

    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'),('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body]