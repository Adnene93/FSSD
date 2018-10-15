'''
Created on 24 nov. 2016

@author: Adnene
'''
import json


def writeJSON(jsonObject,destination) : ##+'\\'+'overallStatistiques.json'
    with open(destination, 'wb') as outfile:
        json.dump(jsonObject, outfile)
        
        
def readJSON(source):
    data={}
    with open(source,'rb') as data_file:    
        data = json.load(data_file)
    return data


def stringifyUnicodeValues(data):
    if type(data) is dict :
        for key,value in data.iteritems():
            if type(value) is unicode :
                data[key]=str(data[key])
            elif hasattr(data[key], '__iter__'):
                stringifyUnicodeValues(data[key])
    if type(data) is list or type(data) is tuple :
        for key,value in enumerate(data):
            if type(value) is unicode :
                data[key]=str(data[key])
            elif hasattr(data[key], '__iter__'):
                stringifyUnicodeValues(data[key])


def readJSON_stringifyUnicodes(source):
    data={}
    with open(source,'rb') as data_file:    
        data = json.load(data_file)
    stringifyUnicodeValues(data)
    
    
    
    return data

def workflowStage_jsonReader( #iterator  for a repository
    inputs={},
    configuration={},
    outputs={},
    workflow_stats={}
    ) :
    
    '''
    {
    
        'id':'stage_id',
        'type':'jsonReader',
        'inputs': {
            'sourceFile':'file_path'
        },
        'configuration': {
        },
        'outputs':{
            'dataset':[]
        }
    }
    '''
    
    
    outputs['dataset']=readJSON(inputs['sourceFile'])
    
    return outputs


def workflowStage_jsonWriter( #iterator  for a repository
    inputs={},
    configuration={},
    outputs={},
    workflow_stats={}
    ) :
    
    '''
    {
    
        'id':'stage_id',
        'type':'jsonWriter',
        'inputs': {
            'dataset':[],
            'destinationFile':'file_path'
        },
        'configuration': {
        },
        'outputs':{

        }
    }
    '''
    
    
    writeJSON(inputs['dataset'],inputs['destinationFile'])
    return outputs
    
