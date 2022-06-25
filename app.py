import shelve, uuid, os
from pathlib import Path
from flask import Flask, render_template,request,redirect, url_for
import uuid 
from flask_ckeditor import CKEditor
from datetime import date
import socket


app = Flask(__name__)
app.config['CKEDITOR_HEIGHT'] = 500
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)



def start():
  folder = os.path.join(Path.home(), '.dais')
  file = os.path.join(folder,'daisdb')
  os.chdir(Path.home())
  if os.path.exists(folder):
    if os.path.exists(file):
      var = 1
    else:
      os.chdir(folder)
      noteObject = shelve.open('daisdb')
      note = []
      noteObject['notes'] = note
      noteObject.close()
  else:
    os.mkdir('.dais')
    os.chdir(folder)
    noteObject = shelve.open('daisdb')
    note = []
    noteObject['notes'] = note
    noteObject.close()
    
@app.route('/')
def index():
  start()
  folder = os.path.join(Path.home(), '.dais')
  os.chdir(folder)
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))

  ipaddress = s.getsockname()[0]
  noteObject = shelve.open('daisdb', 'r', writeback = True)
  notes = noteObject['notes']
  
  pnotes = []
  print(notes)
  
  for i in notes:
    if i['ipaddress'] == ipaddress:
      pnotes.append(i)
      
  return render_template('index.html',notes=pnotes)
  
  
@app.route('/new',methods = ['GET','POST'])
def new():
  folder = os.path.join(Path.home(), '.dais')
  os.chdir(folder)
  
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))

  ipaddress = s.getsockname()[0]
 
  if request.method == 'POST':
    ids = uuid.uuid4()
    title = request.form['title']
    data = request.form.get('ckeditor')
    current_date = date.today()
    
    obj = {
      'ipaddress' : ipaddress,
      'ids':ids,
      'title':title,
      'content': data,
      'date': current_date
    }
  
    noteObject = shelve.open('daisdb', writeback = True)
    noteObject['notes'].append(obj)
    
    noteObject.sync()
    
    noteObject.close()
    return redirect('/')
  else:
    return render_template('new.html')
  
@app.route('/edit/<ids>',methods = ['GET','POST'])
def edit(ids):
  folder = os.path.join(Path.home(), '.dais')
  os.chdir(folder)
  if request.method == 'POST':
    title = request.form['title']
    data = request.form.get('ckeditor')
    
    var = ids
    noteObject = shelve.open('daisdb','w', writeback = True)
    noteArrays = noteObject['notes']
    noteArray = []
  
    for i in noteArrays:
      if str(i['ids']) == str(var):
        noteArray.append(i)
        break
    num = noteArrays.index(noteArray[0])
    noteArrays[num]['title'] = title
    noteArrays[num]['content'] = data
    noteArrays[num]['date'] = date.today()
    
    noteObject['notes'] = noteArrays
    noteObject.sync()
    
    noteObject.close()
    return redirect('/view/' + str(noteArrays[num]['ids']))
  else:
    var = ids
    noteObject = shelve.open('daisdb','r', writeback = True)
    noteArrays = noteObject['notes']
    noteArray = []
  
    for i in noteArrays:
      if str(i['ids']) == str(var):
        noteArray.append(i)
        break
    
    return render_template('edit.html',noteArray=noteArray[0])


@app.route('/view/<ids>')
def view(ids):
  folder = os.path.join(Path.home(), '.dais')
  os.chdir(folder)
  noteObject = shelve.open('daisdb','r', writeback = True)
  noteArrays = noteObject['notes']
  noteArray = []

  for i in noteArrays:
    if str(i['ids']) == str(ids):
      print(i['ids'])
      noteArray.append(i)
      break
  
  return render_template('view.html',noteArray=noteArray[0])

@app.route('/delete/<ids>')
def delete(ids):
  folder = os.path.join(Path.home(), '.dais')
  os.chdir(folder)
  var = ids
  noteObject = shelve.open('daisdb','w', writeback = True)
  noteArrays = noteObject['notes']
  noteArray = []

  for i in noteArrays:
    if str(i['ids']) == str(var):
      noteArray.append(i)
      break
  num = noteArrays.index(noteArray[0])
  noteArrays.pop(num)
  noteObject['notes'] = noteArrays
  return redirect('/')


@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

if __name__ == '__main__':
  app.run(debug=True, port=35607)
