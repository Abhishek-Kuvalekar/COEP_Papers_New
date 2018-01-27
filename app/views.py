from flask import render_template
from app import app
import os

@app.route('/')
def homepage():
    'Renders home.html.'
    contentDict = dict()
    return render_template('home.html', contentDict = contentDict)

@app.route('/branch/<branchName>')
def showContent(branchName = None):
    'Creates a dictionary of contents of each branch directory.'
    
    if(branchName == None):
        return render_template('home.html')
    
    path = 'app/static/papers/' + branchName
    contentDict = dict()
    
    for year in os.listdir(path):
        if(not os.path.isdir(path + '/' + year)):
            continue
        contentDict[year] = dict()
        for sub in os.listdir(path + '/' + year):
            if(not os.path.isdir(path + '/' + year + '/' + sub)):
                continue
                
            contentDict[year][sub] = os.listdir(path + '/' + year + '/' + sub)
        
    contentDict['branchName'] = branchName
    return render_template('content.html', contentDict = contentDict, header_title = branchName)