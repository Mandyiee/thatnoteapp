import shelve, uuid, os
from pathlib import Path
from flask import Flask, render_template,request,redirect, url_for
import uuid 
from flask_ckeditor import CKEditor
from datetime import date
import datetime
import flask
import requests,json,ast
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
    
@app.route('/',methods = ['GET','POST'])
def index():
  
  if request.method == 'POST':
    
    folder = os.path.join(Path.home(), '.dais')
    os.chdir(folder)
  
    resp = requests.get('https://api.ipify.org/')
    ipaddress1 = resp.text
    noteObject = shelve.open('daisdb', 'r', writeback = True)
    note = noteObject['notes']
  
    ipaddress3 = flask.request.remote_addr
    hostname = socket. gethostname()
    ipaddress2 = socket. gethostbyname(hostname)
    ipaddress4 = request.environ.get('HTTP_X_REAL_IP', request.remote_addr) 

    print(ipaddress1,ipaddress2,ipaddress3,ipaddress4)
    
    resp = request.get_data('data')
    
    
    
    resp = json.loads(resp.decode("utf-8").replace("'",'"'))

    
    
    ipaddress = resp['data']['ip'] 
    gnotes = []
    
    for i in note:
      if i['ipaddress'] == ipaddress:
        print(ipaddress == i['ipaddress'])
        print(i)
        gnotes.append(i)
    
    print(gnotes)  
    return redirect('/ne')
  else:
    start()
    pnotes = []
    print(' return render_template(index.html,notes=pnotes)')
    return render_template('index.html',notes=pnotes)
    
  
@app.route('/<ip>')
def index_two(ip):
    ipaddress = ip
    folder = os.path.join(Path.home(), '.dais')
    os.chdir(folder)
    
    noteObject = shelve.open('daisdb', 'r', writeback = True)
    note = noteObject['notes']
    
    gnotes = []
    
    for i in note:
      if i['ipaddress'] == ipaddress:
        print(ipaddress == i['ipaddress'])
        print(i)
        gnotes.append(i)
    return render_template('main_index.html',notes=gnotes)
    
@app.route('/new',methods = ['GET','POST'])
def new():
  folder = os.path.join(Path.home(), '.dais')
  os.chdir(folder)
  

  if request.method == 'POST':
    ids = uuid.uuid4()
    title = request.form['title']
    data = request.form.get('ckeditor')
    current_date = date.today()
    ipaddress = request.form['ipaddress']
    
    
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
