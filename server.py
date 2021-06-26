from flask import Flask, request ,make_response
from flask_restful import Resource, Api
from sqlalchemy import create_engine
import json
from typing import final
from bs4 import BeautifulSoup 
import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom
#from flask.ext.jsonpify import jsonify

db_connect = create_engine('sqlite:///test.db')
app = Flask(__name__)
api = Api(app)

@app.route('/result')
def Result():
        conn = db_connect.connect() # connect to database
        result ={}
        query = conn.execute("select * from DATA") # This line performs query and returns json result
        data = query.fetchall()
        for i in data:
            result[i[0]] = i[1]
        #return hello
 
        return(result)
@app.route('/input/<string:xml_name>')
def Input(xml_name):
        
        try:
            doc= xml.dom.minidom.parse('../LM_backend_challenge/'+xml_name+'.xml')
        except :
            return json.dumps({'errors':"error"})
        hello = doc.getElementsByTagName('formatting')
        arr=[]
        for elem in hello:
            arr.append(elem.firstChild.data)
        tryy(arr)
        return json.dumps({'result': 'Data Uploaded','status': 200})

def tryy(arrr):
    finalArray = []
    liveArray = []
    for ell in arrr:
        if(ell.__contains__("Plaintiff,")):
            finalArray.append(ell)
        if(ell.__contains__("Defendants.")):
            finalArray.append(ell)
    
    hello = finalArray[len(finalArray)-1]
    bye = finalArray[len(finalArray)-2]
    total = arrr[arrr.index(hello)-3]+arrr[arrr.index(hello)-2]+arrr[arrr.index(hello)-1]

    
    if(len(total)<10):
        total = arrr[arrr.index(hello)-6]+arrr[arrr.index(hello)-5]
    totals = arrr[arrr.index(bye)-2]+arrr[arrr.index(bye)-1]
    liveArray.append(totals)
    liveArray.append(total)

    conn = db_connect.connect()  
    addData = f"""INSERT INTO DATA VALUES('{liveArray[0]}', '{liveArray[1]}')"""
    conn.execute(addData)
        


if __name__ == '__main__':
     app.run(port='5002')