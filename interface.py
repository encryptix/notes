from helpers import FormHelpers
from helpers import NumberHelpers
from notes_backend import Notes

def do_index():
    n = Notes()
    return n.index()

def do_select(note_id):
    n = Notes()
    return n.select_note(note_id)

def do_update(note_id, text):
    n = Notes()
    return n.update_note(note_id,text)

def do_delete(note_id):
    n = Notes()
    return n.remove_note(note_id)

def do_add_note(data):
    n = Notes()
    #returns the note id
    return n.add_note(data)

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

    #index,view,add,delete,update
    if not action:
        response_body = "<error_interface>"

    elif action == "index":
        response_body = do_index()
    elif action =="view":
        note_id = FormHelpers.get_input(d,'id')
        if NumberHelpers.is_positive_integer(note_id):
            response_body =  do_select(note_id)
        else:
            response_body = "<error_interface>"

        
    elif action == "add":
        data = FormHelpers.get_input(d,'data')
        if data:
            response_body = do_add_note(data)
        else:
            response_body = "<error_interface>"

    elif action == "delete":
        note_id = FormHelpers.get_input(d,'id')
        if NumberHelpers.is_positive_integer(note_id):
            response_body = do_delete(note_id)
        else:
            response_body = "<error_interface>"
        
    elif action == "update":
        note_id = FormHelpers.get_input(d,'id')
        data = FormHelpers.get_input(d,'data')

        if NumberHelpers.is_positive_integer(note_id) and data:
            response_body = do_update(note_id,data)
        else:
            response_body = "<error_interface>"        
    else:
        response_body = "<error_interface>"

    response_body = "<pre>"+response_body+"</pre>"    
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'),('Content-Length', str(len(response_body)))]
    start_response(status, response_headers)

    return [response_body]