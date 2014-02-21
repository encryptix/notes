var site="site=http://dev.raynoonanwindows.ie/";
var first_time = true;
var new_note_content = "NewNote";
var new_note_name = "NoteName";
//Parser
function create_JSON_object(dataJSON){
    log("Recieved: "+dataJSON);
    var message_area = document.getElementById("message_area");
    var message_text = document.getElementById("message_text");

    if(dataJSON == "<error>"){
        message_area.setAttribute('class','error');
        message_text.innerText = "An error has occured, please refresh";
    }else if(dataJSON == "<error_interface>"){
        message_area.setAttribute('class','error');
        message_text.innerText = "Invalid Input(s)";
    }else if (dataJSON == "<no_note>"){
        message_area.setAttribute('class','error');
        message_text.innerText = "A note could not be found, please refresh";
    }else if(dataJSON == "<success>"){
        message_area.setAttribute('class','ok');
        message_text.innerText = "Sucessfully Completed";
        return true;
    }else{
        jsonObj = JSON.parse(dataJSON);

        var lock = document.getElementById("lock");
        lock.checked = false;
        message_text.innerText = "";

        //Check that the note wasnt locked
        if (jsonObj.hasOwnProperty("isLocked")){
            var note_id = jsonObj.noteID;
            var is_locked = jsonObj.isLocked;

            var hidden_field_id = document.getElementById("current_note_id");
            hidden_field_id.value = jsonObj.noteID;
            
            if(is_locked == true || is_locked=="true"){
                var note_text = document.getElementById("note_text");
                div_to_textarea();
                //note_text.value="" was not setting the value quickly enough
                note_text.value = "";
                document.getElementById("note_text").value="";

                message_text.innerText = "Note is locked please unlock to continue";
                set_editable(false,note_id);
                lock.checked = true;
                textarea_to_div();
                return null;
            }
        }
        return jsonObj;
    }
    return null;
}
//Interaction with HTML
function add_note_index(noteID,noteName){
    var index_area = document.getElementById("index_area");
    //Check if it already exists
    var current_div = document.getElementById("note_"+noteID);
    if(current_div!=null){
        return;
    }

    var html = '<input type="hidden" id="note_id" value="'+noteID+'"/>';
    html += '<div class="selectable" onClick="get_note('+noteID+')" >';
    html +=     '<input type="text" class="note_name" value="'+noteName+'" onKeyUp="update_note_name('+noteID+')" />'
    html += '</div>';
    html += '<input type="button" class="remove_button" onClick="delete_note('+noteID+')" value="Delete Note" />';
                
    var newdiv = document.createElement('div');
    newdiv.setAttribute('id',"note_"+noteID);
    newdiv.setAttribute('class',"noteID");
    newdiv.innerHTML = html;
    index_area.appendChild(newdiv);
}

function show_note(noteID,content){
    //convert to text area to update
    div_to_textarea();
    var hidden_field_id = document.getElementById("current_note_id");
    var note_text = document.getElementById("note_text");
    hidden_field_id.value = noteID;
    note_text.value = content;
    //set to div
    textarea_to_div();
}

function set_editable(bool,noteID){
    log("set_editable: "+bool)
    var note_text = document.getElementById("note_text");
    note_text.disabled = !bool;
    var id;
    if (!noteID){
        var hidden_field_id = document.getElementById("current_note_id");
        id = hidden_field_id.value;
    }else{
        id = noteID;
    }

    var note_name = document.getElementById("note_"+id);
    if (note_name != null){
        note_name.getElementsByTagName("input")[1].disabled = !bool;
    }
}

//Receive Functions
function receive_note_indexes(dataJSON){
    log("Receive Index");

    var indexes = create_JSON_object(dataJSON);
    if(indexes != null){
        var length = indexes.notes.length;
        //Generate side bar
        if(length > 0){
            for(i=0;i<length;i++){
                var index = indexes.notes[i].noteID;
                var note_name = atob(indexes.notes[i].noteName);

                add_note_index(index,note_name);
            }
            var id = indexes.notes[0].noteID;
            get_note(id);
        }else{
            set_editable(false);
        }
    }
}

function receive_note(dataJSON){
    log("Receive Note");

    var note = create_JSON_object(dataJSON);
    if(note != null){
        log(note);
        
        var id = note.noteID;
        var textb64 = note.note;

        var text = atob(textb64);
        show_note(id,text);
        set_editable(true);
    }
}

function receive_add_note(dataJSON){
    log("Receive Add Note");

    var noteObj = create_JSON_object(dataJSON);
    if(noteObj != null){
        var note_id = noteObj.noteID;

        add_note_index(note_id,new_note_name);
        show_note(note_id,new_note_content);
        if(first_time){
            set_editable(true);
            //TODO::just set this correctly 
            first_time=false;
        }
    }
}

function receive_delete_note(dataJSON){
    log("Receive Delete Note");

    var noteObj = create_JSON_object(dataJSON);
    if(noteObj!=null){
        var note_id = noteObj.noteID;
        var index_area = document.getElementById("index_area");
        var div = document.getElementById("note_"+note_id);
        index_area.removeChild(div);

        var hidden_field_id = document.getElementById("current_note_id");
        if(hidden_field_id.value == note_id){
            hidden_field_id.value = "-1";
            //Lazy way of dealing with note content
            first_time=true;
            get_notes();
        }
    }
}

function receive_unlock(dataJSON){
    log("Receive unlock");

    var lockInfo = create_JSON_object(dataJSON);

    if(lockInfo != null){
        var note_id = lockInfo.noteID;
        var is_locked = lockInfo.isLocked;

        if (is_locked == false || is_locked == "false"){
            var note_text = document.getElementById("note_text");
            note_text.disabled = false;


            get_note(note_id);
        }
    }

}

//Send Functions
function get_notes(){
    log("Get Index");
    
    ajax(receive_note_indexes,"action=index");
}

function get_note(noteID){
    log("Get Note");
    
    ajax(receive_note,"action=view&id="+noteID);
}

function add_note(){
    log("Add Note");
    data_b64 = btoa(new_note_content);
    name_b64 = btoa(new_note_name);

    ajax(receive_add_note,"action=add&data="+data_b64+"&name="+name_b64);
}

function delete_note(index){
    log("Delete Note");
    var lock = document.getElementById("lock");
    if (lock.checked){
        log("note is locked");
    }else{
        var id = index;
        if(index =='current_note'){
            id = document.getElementById("current_note_id").value;
        }
        ajax(receive_delete_note,"action=delete&id="+id);
    }
}

function update_note(){
    log("Update Note");

    var lock = document.getElementById("lock");
    if (lock.checked){
        log("note is locked");
    }else{
        var id = document.getElementById("current_note_id").value;
        var data = document.getElementById("note_text").value;

        log("id: "+id+", data: "+data);

        data_b64 = btoa(data);

        //Check that the data is valid b64 before sending
        //Same check should be done server side before accepting/saving
        try{
            atob(data_b64);
        }catch(e){
            alert("Please copy the text and refresh..b64 issue");
            return;
        }
        
        //Just error check for updating a note
        ajax(create_JSON_object,"action=update&id="+id+"&data="+data_b64);
    }
}

function update_note_name(id){
    log("Update Note Name");

    var lock = document.getElementById("lock");
    if (lock.checked){
        log("note is locked");
    }else{
        var name = document.getElementById("note_"+id).getElementsByTagName("input")[1].value;
        log("id: "+id+", name: "+name);

        name_b64 = btoa(name);
        try{
            atob(name_b64);
        }catch(e){
            alert("Please copy the name and refresh..b64 issue");
            return;
        }
        ajax(create_JSON_object,"action=update_name&id="+id+"&name="+name_b64);
    }
}

function lock_clicked(){
    log("Lock Clicked")
    var lock = document.getElementById("lock");
    var id = document.getElementById("current_note_id").value;
    var password = prompt("Enter Password","");    

    if(password == null || password == ""){
        alert("didnt enter pass; todo");
        lock.checked = !lock.checked;
    }else if(lock.checked){
        lock_note(id,password);
    }else{
        unlock_note(id,password);
    }
}

function lock_note(id,password){
    log("Lock Note: "+id)
    //UPDATE what if it doesnt lock?!
    ajax(create_JSON_object,"action=lock&id="+id+"&password="+password);
}

function unlock_note(id,password){
    log("Unlock Note: "+id)
    ajax(receive_unlock,"action=unlock&id="+id+"&password="+password);
}

//Standard js functions
function log(fn){
    console.log(fn);
}

function ajax(callback_func,params){
    var xmlHttp;
    var action = site+"&"+params;
    if(window.XMLHttpRequest){
        xmlHttp = new XMLHttpRequest();
    }else{
        //Its IE
        xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlHttp.onreadystatechange=function(){
        if(xmlHttp.readyState == 4){
            if(xmlHttp.status==200){
                callback_func(xmlHttp.responseText);
            }else{
                log("ERROR: "+xmlHttp.status+" RS: "+xmlHttp.readyState);
            }
        }
    }
    xmlHttp.open("POST","interface.wsgi",true);
    xmlHttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    xmlHttp.send(action);
}

//Could create an object and have a .toDiv .toTextArea
function textarea_to_div(){
    var note_text = document.getElementById("note_text");
    if(note_text.nodeName=="DIV"){
        console.log("Already a div");
        return;
    }
    var parent = note_text.parentNode;
    var data = note_text.value;
    data = data.replace(/\n/g," <br/>");

    //console.log("data is "+data);

    var div = document.createElement('div');

    div.innerHTML = data;
    div.setAttribute('id',"note_text");
    div.setAttribute('onDblClick',"toggle_text_area()");

    //condense into one later
    div.innerHTML = convert_to_links(div.innerHTML);
    parent.replaceChild(div, note_text);

    var mode_button = document.getElementById("mode_button");
    //set class to mode_button_read
    mode_button.setAttribute('class',"mode_button_read");
}

function div_to_textarea(){
    var note_text = document.getElementById("note_text");
    if(note_text.nodeName=="TEXTAREA"){
        console.log("Already a textarea");
        return;
    }
    var parent = note_text.parentNode;
    remove_links();
    var data = note_text.innerHTML;


    data = data.replace(/<br\/>/g,"\n");
    data = data.replace(/<br>/g,"\n");
    data = data.replace(/ <br\/>/g,"\n");
    data = data.replace(/ <br>/g,"\n");

    //console.log("data is "+data);

    var textarea = document.createElement('textarea');
    textarea.setAttribute('id',"note_text");
    textarea.setAttribute('rows',"20");
    textarea.setAttribute('cols',"50");
    textarea.setAttribute('onKeyUp',"update_note()");
    textarea.setAttribute('onDblClick',"toggle_text_area()");
    textarea.setAttribute('onBlur',"textarea_to_div()");


    textarea.value = data;
    parent.replaceChild(textarea, note_text);

    var mode_button = document.getElementById("mode_button");
    //set class to mode_button_edit
    mode_button.setAttribute('class',"mode_button_edit");
}

function toggle_text_area(){
    var note_text = document.getElementById("note_text");
    if(note_text.nodeName=="TEXTAREA"){
        textarea_to_div();
    }else{
        div_to_textarea();
    }
}

//was used for cancelling single click events
function stop_event(){
    window.event.stopPropagation();
}

function convert_to_links(text) {
    var replaceText, replacePattern1;

    //URLs starting with http://, https://
    replacePattern1 = /(\b(https?):\/\/[-A-Z0-9+&amp;@#\/%?=~_|!:,.;]*[-A-Z0-9+&amp;@#\/%=~_|])/ig;
    replacedText = text.replace(replacePattern1, '<a href="$1" onclick="stop_event()" target="_blank">$1</a>');

    //URLs starting with "www."
    replacePattern2 = /(^|[^\/])(www\.[\S]+(\b|$))/gim;
    //space gets eaten converting back so add one
    replacedText = replacedText.replace(replacePattern2, ' <a href="http://$2" onclick="stop_event()" target="_blank">$2</a>');

    //returns the text result

    return replacedText;
}

function remove_links(){
    var e = document.getElementById("note_text");
    var links = e.getElementsByTagName("a");
    //console.log(links);

    var i=0;
    while(links.length>0){
      //console.log(links[0].innerHTML);
      links[0].outerHTML = links[0].innerHTML;
      i++;

      if(i>1000){
        console.log("infinite loop in remove links due to quirkyness I couldnt loop");
        return;
      }
    }
}