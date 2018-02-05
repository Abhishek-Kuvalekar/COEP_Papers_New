from flask import render_template, flash, redirect
from app import app
from .forms import SearchForm
from app import searchBar
import os

@app.route('/', methods = ['GET', 'POST'])
def homepage():
    'Renders home.html.'
    
    contentDict = dict()
    form = SearchForm()
    if(form.validate_on_submit()):
        """Add code for keyword search."""
        contentList = searchBar.grep(form.searchKey.data)
        return render_template('searchResult.html', contentList = [item.decode() for item in contentList], form = SearchForm(), contentDict = contentDict)    
    
    return render_template('home.html', contentDict = contentDict, form = form)

@app.route('/branch/<branchName>', methods = ['GET', 'POST'])
def showContent(branchName = None):
    'Creates a dictionary of contents of each branch directory.'
    
    if(branchName == None):
        return render_template('home.html')
    
    path = 'app/static/papers/' + branchName
    contentDict = dict()
    form = SearchForm()
    
    for year in os.listdir(path):
        if(not os.path.isdir(path + '/' + year)):
            continue
        contentDict[year] = dict()
        for sub in os.listdir(path + '/' + year):
            if(not os.path.isdir(path + '/' + year + '/' + sub)):
                continue
                
            contentDict[year][sub] = os.listdir(path + '/' + year + '/' + sub)
        
    contentDict['branchName'] = branchName
    return render_template('content.html', contentDict = contentDict, header_title = branchName, form = form)

@app.route('/compressed/<branchName>/<year>')
@app.route('/compressed/<branchName>/<year>/<subject>')
def giveCompressedFolder(branchName = None, year = None, subject = None):
    if(branchName == None):
        return;
    if(year == None):
        return;
    path = "app/static/papers/" + branchName + "/" + year
    filename = branchName + "_" + year
    if(subject != None):
        path += "/" + subject
        filename += "_" + subject
    filename += ".tar.gz"
    os.system('tar -czf ' + "app/static/" + filename + " " + path)
    return redirect("/static/" + filename)