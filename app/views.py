from flask import render_template, flash, redirect
from app import app, mail
from .forms import SearchForm, RequestForm, UploadForm
from app import searchBar
import os, os.path, time, subprocess, datetime
from flask_mail import Message
from config import ADMINS

def createDict(contentList):
    'Creates a dictionary of the list obtained from search result.'
    contentDict = dict()
    for item in contentList:
        if(item.decode() == ''):
            continue
        itemList = item.decode().split('/')
        if(contentDict.get(itemList[3], None) == None):
            contentDict[itemList[3]] = dict()
        if(contentDict[itemList[3]].get(itemList[4], None) == None):
            contentDict[itemList[3]][itemList[4]] = dict()
        if(contentDict[itemList[3]][itemList[4]].get(itemList[5], None) == None):
            contentDict[itemList[3]][itemList[4]][itemList[5]] = list()
        contentDict[itemList[3]][itemList[4]][itemList[5]].append(itemList[6])
        
    return contentDict
    
def clearMess(difference):
    'Deletes all the tar.gz files created "difference" minutes before.'
    path = 'app/static'
    output = os.listdir(path)
    currentTime = int(str(datetime.datetime.now()).split(' ')[1].split(':')[0]) * 60 + int(str(datetime.datetime.now()).split(' ')[1].split(':')[1])
    for item in output:
        if(item == ''):
            break
        if('gz' not in item):
            continue
        tmp = time.ctime(os.path.getctime(path + "/" + item))
        tmp1 = tmp.split(' ')[3]
        tmp2 = tmp1.split(':')
        creationTime = 60 * int(tmp2[0]) + int(tmp2[1])
        if(difference <= (currentTime - creationTime)):
            os.remove(path + "/" + item)
    return

def requestPaper(form):
    msg = Message('New paper request', sender = ADMINS[0], recipients = ADMINS)
    msg.body = 'text body'
    msg.html = 'Branch: ' + form.branch_request.data + '<br />' + 'Year: ' + form.year_request.data + '<br />' + 'Subject: ' + form.sub_request.data
    with app.app_context():
        mail.send(msg)
    return "hello"

def uploadPaper(form):
    msg = Message('New upload request', sender = ADMINS[0], recipients = ADMINS)
    msg.body = 'text body'
    msg.html = 'Branch: ' + form.branch.data + '<br />' + 'Year: ' + form.year.data + '<br />' + 'Subject: ' + form.sub.data
    msg.attach(form.paper.name, 'application/octect-stream', form.paper.read())
    with app.app_context():
        mail.send(msg)
    return "world"
    
@app.route('/', methods = ['GET', 'POST'])
def homepage():
    'Renders home.html.'
    contentDict = dict()
    form = SearchForm()
    requestForm = RequestForm()
    uploadForm = UploadForm()
    if(requestForm.validate_on_submit()):
        return requestPaper(requestForm)
    if(uploadForm.validate_on_submit()):
        return uploadPaper(uploadForm)
    if(form.validate_on_submit()):
        searchDict = createDict(searchBar.grep(form.searchKey.data))
        return render_template('searchResult.html', searchDict = searchDict, form = SearchForm(), contentDict = contentDict)    
    
    return render_template('home.html', contentDict = contentDict, form = form, requestForm = requestForm, uploadForm = uploadForm)

@app.route('/branch/<branchName>', methods = ['GET', 'POST'])
def showContent(branchName = None):
    'Creates a dictionary of contents of each branch directory.'
    if(branchName == None):
        return render_template('home.html')
    
    path = 'app/static/papers/' + branchName
    contentDict = dict()
    form = SearchForm()
    requestForm = RequestForm()
    uploadForm = UploadForm()
    if(requestForm.validate_on_submit()):
        return requestPaper(requestForm)
    if(uploadForm.validate_on_submit()):
        return uploadPaper(uploadForm)
    if(form.validate_on_submit()):
        searchDict = createDict(searchBar.grep(form.searchKey.data))
        return render_template('searchResult.html', searchDict = searchDict, form = SearchForm(), contentDict = contentDict)   
    
    for year in os.listdir(path):
        if(not os.path.isdir(path + '/' + year)):
            continue
        contentDict[year] = dict()
        for sub in os.listdir(path + '/' + year):
            if(not os.path.isdir(path + '/' + year + '/' + sub)):
                continue
                
            contentDict[year][sub] = os.listdir(path + '/' + year + '/' + sub)
    
    contentDict['branchName'] = branchName
    return render_template('content.html', contentDict = contentDict, header_title = branchName, form = form, requestForm = requestForm, uploadForm = uploadForm)

@app.route('/compressed/<branchName>/<year>')
@app.route('/compressed/<branchName>/<year>/<subject>')
def giveCompressedFolder(branchName = None, year = None, subject = None):
    'Give compressed file of specified subject or year.'
    if(branchName == None):
        return;
    if(year == None):
        return;
    clearMess(5)
    path = "app/static/papers/" + branchName + "/" + year
    filename = branchName + "_" + year
    if(subject != None):
        path += "/" + subject
        filename += "_" + subject
    filename += ".tar.gz"
    os.system('tar -czf ' + "app/static/" + filename + " " + path)
    return redirect("/static/" + filename)