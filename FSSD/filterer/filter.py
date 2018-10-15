'''
Created on 2 dec. 2016

@author: Adnene
'''
#Same as filter but :
# input can be :          Outputs
#      * dataset ----->  sub dataset
#      * datasetArray -----> sub array
#      * object  ---------> Object or None
#      * simple Array -----> sub array
#      * value -------------> value or None
'''
Created on 24 nov. 2016

@author: Adnene
'''
'''
@note : stage of filtering is a dictionnary :
{
    'dimension' : 'dimensionName',
    'equal | notEqual | inSet | outSet | inInterval | outInterval | lowerThan | greaterThan' : 
    value or values according to the conditions
    
    note that if the attribute is numeric the values introduced can be wrote as values or as :
    avg for average of the whole dataset in the parameter and
    std for standarddeviation
    
    
}
'''
from copy import deepcopy
import math
import os
import re

from util.csvProcessing import writeCSVwithHeader, readCSVwithHeader


def average(dataset,dimensionName):
    #onepass todo
    avg_ret=sum([float(x[dimensionName]) for x in dataset])/float(len(dataset))
    return avg_ret
    
def standardDeviation(dataset,dimensionName):
    #onepass todo
    avg_ret=sum([float(x[dimensionName]) for x in dataset])/float(len(dataset))
    std_ret = math.sqrt(sum([(float(x[dimensionName])-avg_ret)**2 for x in dataset])/float(len(dataset)))
    return std_ret
    

def bitwise(dataset,dimensionName,valueInCondition):
    
    if valueInCondition is not None :
        filteredDataSet=[dataset[i] for i in range(len(dataset)) if i<len(valueInCondition) and valueInCondition[i]]
        return filteredDataSet
    else :
        return dataset

def bitwise_obj(obj,dimensionName,valueInCondition):
    if (valueInCondition is None or valueInCondition):
        return obj
    else :
        return None
    
def equal(dataset,dimensionName,valueInCondition):
    filteredDataSet=[]
    for obj in dataset :
        if (obj[dimensionName]==valueInCondition):
            filteredDataSet.append(obj)
    return filteredDataSet

def equal_obj(obj,dimensionName,valueInCondition):
    if (obj[dimensionName]==valueInCondition):
        return obj
    else :
        return None

def strlike(dataset,dimensionName,valueInCondition):
    filteredDataSet=[]
    regularExp=str(valueInCondition)
    regularExp=regularExp.replace('.','\.')
    regularExp=regularExp.replace('%','.*')
    regularExp=regularExp.replace('_','.')
    regularExp='^'+regularExp+'$'
    regexp = re.compile(regularExp)
    
    for obj in dataset :
        if regexp.search(obj[dimensionName]) is not None :
            filteredDataSet.append(obj)
    return filteredDataSet

def strlike_obj(obj,dimensionName,valueInCondition):
    
    regularExp=str(valueInCondition)
    regularExp=regularExp.replace('.','\.')
    regularExp=regularExp.replace('%','.*')
    regularExp=regularExp.replace('_','.')
    regularExp='^'+regularExp+'$'
    regexp = re.compile(regularExp)
    
    
    if regexp.search(obj[dimensionName]) is not None :
        return obj
    else :
        return None

def strNotlike(dataset,dimensionName,valueInCondition):
    filteredDataSet=[]
    regularExp=str(valueInCondition)
    regularExp=regularExp.replace('.','\.')
    regularExp=regularExp.replace('%','.*')
    regularExp=regularExp.replace('_','.')
    regularExp='^'+regularExp+'$'
    regexp = re.compile(regularExp)
    
    for obj in dataset :
        if regexp.search(obj[dimensionName]) is None :
            filteredDataSet.append(obj)
    return filteredDataSet 

def strNotlike_obj(obj,dimensionName,valueInCondition):
    
    regularExp=str(valueInCondition)
    regularExp=regularExp.replace('.','\.')
    regularExp=regularExp.replace('%','.*')
    regularExp=regularExp.replace('_','.')
    regularExp='^'+regularExp+'$'
    regexp = re.compile(regularExp)
    
    
    if regexp.search(obj[dimensionName]) is None :
        return obj
    else :
        return None    

def strlikeInSet(dataset,dimensionName,valueInCondition):
    filteredDataSet=[]
    finalRegularExp=''
    iterator_valueInCondition=iter(valueInCondition)
    finalRegularExp+=str(next(iterator_valueInCondition))
    for regularExpression in iterator_valueInCondition:
        finalRegularExp+='|'+str(regularExpression)
        
    filteredDataSet=strlike(dataset, dimensionName, finalRegularExp)
    return filteredDataSet 

def strlikeInSet_obj(obj,dimensionName,valueInCondition):
    finalRegularExp=''
    iterator_valueInCondition=iter(valueInCondition)
    finalRegularExp+=str(next(iterator_valueInCondition))
    for regularExpression in iterator_valueInCondition:
        finalRegularExp+='|'+str(regularExpression)
        
    objRet=strlike_obj(obj, dimensionName, finalRegularExp)
    return objRet 

def strlikeOutSet(dataset,dimensionName,valueInCondition):
    filteredDataSet=[]
    finalRegularExp=''
    iterator_valueInCondition=iter(valueInCondition)
    finalRegularExp+=str(next(iterator_valueInCondition))
    for regularExpression in iterator_valueInCondition:
        finalRegularExp+='|'+str(regularExpression)
        
    filteredDataSet=strNotlike(dataset, dimensionName, finalRegularExp)
    return filteredDataSet 

def strlikeOutSet_obj(obj,dimensionName,valueInCondition):
    finalRegularExp=''
    iterator_valueInCondition=iter(valueInCondition)
    finalRegularExp+=str(next(iterator_valueInCondition))
    for regularExpression in iterator_valueInCondition:
        finalRegularExp+='|'+str(regularExpression)
        
    objRet=strNotlike_obj(obj, dimensionName, finalRegularExp)
    
    return objRet 

def strlikeContainSet(dataset,dimensionName,valueInCondition): #the dimension value is an array - \forall b in set_b \exist a in set_a verify(a,b) 
    filteredDataSet=[]
    iterator_valueInCondition=iter(valueInCondition)
    iteratorRegExp=[]
    for regularExpression in iterator_valueInCondition:
        regularExp = str(regularExpression)
        regularExp=regularExp.replace('.','\.')
        regularExp=regularExp.replace('%','.*')
        regularExp=regularExp.replace('_','.')
        regularExp='^'+regularExp+'$'
        iteratorRegExp.append(re.compile(regularExp))
    for obj in dataset :
        verifyRegExps=[False for i in range(len(iteratorRegExp))]
        
        for index_regexp in range(len(iteratorRegExp)):
            for val in obj[dimensionName]:
                if iteratorRegExp[index_regexp].search(val) is not None:
                    verifyRegExps[index_regexp]=True
                    break

        verify = not (False in verifyRegExps) or (len(verifyRegExps)==0)
        if verify:
            filteredDataSet.append(obj)   
    return filteredDataSet



def strlikeContainSet_obj(obj,dimensionName,valueInCondition): #the dimension value is an array - \forall b in set_b \exist a in set_a verify(a,b) 
 
    iterator_valueInCondition=iter(valueInCondition)
    iteratorRegExp=[]
    for regularExpression in iterator_valueInCondition:
        regularExp = str(regularExpression)
        regularExp=regularExp.replace('.','\.')
        regularExp=regularExp.replace('%','.*')
        regularExp=regularExp.replace('_','.')
        regularExp='^'+regularExp+'$'
        iteratorRegExp.append(re.compile(regularExp))
 
    numberOfRegExp=len(iteratorRegExp)
    verifyRegExps=[False for i in range(numberOfRegExp)]
     
     
    for index_regexp in range(numberOfRegExp):
        for val in obj[dimensionName]:
            if iteratorRegExp[index_regexp].search(val) is not None:
                verifyRegExps[index_regexp]=True
                break
 
        verify = not (False in verifyRegExps) or (len(verifyRegExps)==0)
        if verify:
            return obj  
    return None
#     
#     setOfAllPossibleParents=[]
#     setOfAllPossibleParents_extend=setOfAllPossibleParents.extend
#     for val in obj[dimensionName]:
#         v=(val.split(' ')[0]).split('.')
#         parents=['.'.join(v[0:x+1]) for x in range(len(v))]
#         setOfAllPossibleParents_extend(parents)
#     
#     s1=set([x[:-1] for x in valueInCondition if len(x)>1])
#     s2=set(setOfAllPossibleParents)
# 
#     if s1 <= s2:
#         return obj
#     else :
#         return None

# strlikeContainSet_obj.LAST_VALUE_IN_CONDITION=None
# strlikeContainSet_obj.LAST_REGEXPS=None

def strlikeNotContainSet(dataset,dimensionName,valueInCondition): #the dimension value is an array - \forall b in set_b \exist a in set_a verify(a,b) 
    filteredDataSet=[]
    iterator_valueInCondition=iter(valueInCondition)
    iteratorRegExp=[]
    for regularExpression in iterator_valueInCondition:
        regularExp = str(regularExpression)
        regularExp=regularExp.replace('.','\.')
        regularExp=regularExp.replace('%','.*')
        regularExp=regularExp.replace('_','.')
        regularExp='^'+regularExp+'$'
        iteratorRegExp.append(re.compile(regularExp))
    for obj in dataset :
        verifyRegExps=[False for i in range(len(iteratorRegExp))]
        
        for index_regexp in range(len(iteratorRegExp)):
            for val in obj[dimensionName]:
                if iteratorRegExp[index_regexp].search(val) is not None:
                    verifyRegExps[index_regexp]=True
                    break

        verify = (verifyRegExps.count(False))==len(verifyRegExps)
        if verify:
            filteredDataSet.append(obj)   
    return filteredDataSet 

def strlikeNotContainSet_obj(obj,dimensionName,valueInCondition): #the dimension value is an array - \forall b in set_b \exist a in set_a verify(a,b) 
    iterator_valueInCondition=iter(valueInCondition)
    iteratorRegExp=[]
    for regularExpression in iterator_valueInCondition:
        regularExp = str(regularExpression)
        regularExp=regularExp.replace('.','\.')
        regularExp=regularExp.replace('%','.*')
        regularExp=regularExp.replace('_','.')
        regularExp='^'+regularExp+'$'
        iteratorRegExp.append(re.compile(regularExp))
    
    verifyRegExps=[False for i in range(len(iteratorRegExp))]
    
    for index_regexp in range(len(iteratorRegExp)):
        for val in obj[dimensionName]:
            if iteratorRegExp[index_regexp].search(val) is not None:
                verifyRegExps[index_regexp]=True
                break

        verify = (verifyRegExps.count(False))==len(verifyRegExps)
        if verify:
            return obj  
    return None 


def contain_themes_obj_old(obj,dimensionName,valueInCondition): #the dimension value is an array - \forall b in set_b \exist a in set_a verify(a,b)      
    s1=set([x for x in valueInCondition if len(x)>0])
    
    s2_arr=[]
    s2_arr_extend=s2_arr.extend
    #s2=set()
    for val in obj[dimensionName]: 
        v=val[:val.index(' ')].split('.')
        s2_arr_extend(['.'.join(v[0:x+1]) for x in range(len(v))])
    s2=set(s2_arr)
     
    return obj if s1 <= s2 else None

def contain_themes_obj(obj,dimensionName,valueInCondition): #the dimension value is an array - \forall b in set_b \exist a in set_a verify(a,b)      
    s1=set([x for x in valueInCondition if len(x)>0])
    
#     s2_arr=[]
#     s2_arr_extend=s2_arr.extend
#     #s2=set()
#     for val in obj[dimensionName]: 
#         v=val[:val.index(' ')].split('.')
#         s2_arr_extend(['.'.join(v[0:x+1]) for x in range(len(v))])
#     s2=set(s2_arr)
    
    s2=obj[dimensionName]
    
    s2_arr=[]
    s2_arr_extend=s2_arr.extend
    #s2=set()
    for val in obj[dimensionName]: 
        v=val[:val.index(' ')].split('.')
        s2_arr_extend(['.'.join(v[0:x+1]) for x in range(len(v))])
    s2=set(s2_arr)

    #print s1,s2
    
    return obj if s1 <= s2 else None



def notEqual(dataset,dimensionName,valueInCondition):
    filteredDataSet=[]
    for obj in dataset :
        if not (obj[dimensionName]==valueInCondition):
            filteredDataSet.append(obj)
    return filteredDataSet

def notEqual_obj(obj,dimensionName,valueInCondition):
    if not (obj[dimensionName]==valueInCondition):
        return obj
    return None

def inSet(dataset,dimensionName,valueInCondition):
    filteredDataSet=[]
    for obj in dataset :
        if (obj[dimensionName] in valueInCondition):
            filteredDataSet.append(obj)
    return filteredDataSet     

def inSet_obj(obj,dimensionName,valueInCondition):
    if (obj[dimensionName] in valueInCondition):
        return obj
    return None 

def outSet(dataset,dimensionName,valueInCondition):
    filteredDataSet=[]
    for obj in dataset :
        if not (obj[dimensionName] in valueInCondition):
            filteredDataSet.append(obj)
    return filteredDataSet        


def outSet_obj(obj,dimensionName,valueInCondition):
    if (obj[dimensionName] not in valueInCondition):
        return obj
    return None 

def inInterval(dataset,dimensionName,valueInCondition):
   
    filteredDataSet=[]
    avg=0
    std=0
    newValueInCondition = [str(valueInCondition[0]),str(valueInCondition[1])]
    if 'avg' in newValueInCondition[0] : 
        avg=average(dataset,dimensionName)
        newValueInCondition[0]=newValueInCondition[0].replace('avg',str(avg))
    if 'avg' in newValueInCondition[1] : 
        avg=average(dataset,dimensionName)
        newValueInCondition[1]=newValueInCondition[1].replace('avg',str(avg))
    if 'std' in newValueInCondition[0] : 
        std=standardDeviation(dataset,dimensionName)
        newValueInCondition[0]=newValueInCondition[0].replace('std',str(std))
    if 'std' in newValueInCondition[1] : 
        std=standardDeviation(dataset,dimensionName)
        newValueInCondition[1]=newValueInCondition[1].replace('std',str(std))
    
    newValueInCondition = [float(eval(newValueInCondition[0])),float(eval(newValueInCondition[1]))]
    for obj in dataset :
        if (newValueInCondition[0] <= float(obj[dimensionName]) <= newValueInCondition[1]):
            filteredDataSet.append(obj)
    return filteredDataSet     


def inInterval_obj(obj,dimensionName,valueInCondition):
   
    newValueInCondition = [valueInCondition[0],valueInCondition[1]]
    if (newValueInCondition[0] <= float(obj[dimensionName]) <= newValueInCondition[1]):
        return obj
    return None 


def outInterval(dataset,dimensionName,valueInCondition):
    filteredDataSet=[]
    avg=0
    std=0
    newValueInCondition = [str(valueInCondition[0]),str(valueInCondition[1])]
    if 'avg' in newValueInCondition[0] : 
        avg=average(dataset,dimensionName)
        newValueInCondition[0]=newValueInCondition[0].replace('avg',str(avg))
    if 'avg' in newValueInCondition[1] : 
        avg=average(dataset,dimensionName)
        newValueInCondition[1]=newValueInCondition[1].replace('avg',str(avg))
    if 'std' in newValueInCondition[0] : 
        std=standardDeviation(dataset,dimensionName)
        newValueInCondition[0]=newValueInCondition[0].replace('std',str(std))
    if 'std' in newValueInCondition[1] : 
        std=standardDeviation(dataset,dimensionName)
        newValueInCondition[1]=newValueInCondition[1].replace('std',str(std))
        
    newValueInCondition = [float(eval(newValueInCondition[0])),float(eval(newValueInCondition[1]))]
    
    for obj in dataset :
        if not (newValueInCondition[0] <= float(obj[dimensionName]) <= newValueInCondition[1]):
            filteredDataSet.append(obj)
    return filteredDataSet   

def outInterval_obj(obj,dimensionName,valueInCondition):
   
    newValueInCondition = [valueInCondition[0],valueInCondition[1]]
    if not (newValueInCondition[0] <= float(obj[dimensionName]) <= newValueInCondition[1]):
        return obj
    return None 


def lowerThan(dataset,dimensionName,valueInCondition):
    filteredDataSet=[]
    avg=0
    std=0
    newValueInCondition = str(valueInCondition)
    if 'avg' in newValueInCondition : 
        avg=average(dataset,dimensionName)
        newValueInCondition=newValueInCondition.replace('avg',str(avg))
    if 'std' in newValueInCondition : 
        std=standardDeviation(dataset,dimensionName)
        newValueInCondition=newValueInCondition.replace('std',str(std))
    newValueInCondition = float(eval(newValueInCondition))
    
    for obj in dataset :
        if (float(obj[dimensionName]) <= newValueInCondition):
            filteredDataSet.append(obj)
    return filteredDataSet 

def lowerThan_obj(obj,dimensionName,valueInCondition):
   
    if (float(obj[dimensionName]) < valueInCondition):
        return obj
    return None  

def lowerThanOrEqual_obj(obj,dimensionName,valueInCondition):
   
    if (float(obj[dimensionName]) <= valueInCondition):
        return obj
    return None  

def greaterThan(dataset,dimensionName,valueInCondition):
    filteredDataSet=[]
    
    avg=0
    std=0
    newValueInCondition = str(valueInCondition)
    if 'avg' in newValueInCondition : 
        avg=average(dataset,dimensionName)
        newValueInCondition=newValueInCondition.replace('avg',str(avg))
    if 'std' in newValueInCondition : 
        std=standardDeviation(dataset,dimensionName)
        newValueInCondition=newValueInCondition.replace('std',str(std))
    newValueInCondition = float(eval(newValueInCondition))
    for obj in dataset :
        
        if (float(obj[dimensionName]) >= newValueInCondition):
            filteredDataSet.append(obj)
    return filteredDataSet 


def greaterThanOrEqual_obj(obj,dimensionName,valueInCondition):
   
    if (float(obj[dimensionName]) >= valueInCondition):
        return obj
    return None

def greaterThan_obj(obj,dimensionName,valueInCondition):
   
    if (float(obj[dimensionName]) > valueInCondition):
        return obj
    return None

MAP_FILTER_TYPE={
    'bitwise':bitwise,
    #########################################"
    'equal':equal,
    'notEqual':notEqual,
    'inSet':inSet,
    'outSet':outSet,
    'inInterval':inInterval,
    'outInterval':outInterval,
    'lowerThan':lowerThan,
    'greaterThan':greaterThan,
    'like':strlike,
    'likeInSet':strlikeInSet,
    'likeOutSet':strlikeOutSet,
    
    #####ARRAY OPERATORS##################
    'likeContainSet':strlikeContainSet,
    'likeNotContainSet':strlikeNotContainSet
}

MAP_FILTER_TYPE_obj={
    'bitwise':bitwise_obj,
    ############SIMPLE###########
    'equal':equal_obj,
    'notEqual':notEqual_obj,
    'inSet':inSet_obj,
    'outSet':outSet_obj,
    'inInterval':inInterval_obj,
    'outInterval':outInterval_obj,
    'lowerThan':lowerThan_obj,
    'greaterThan':greaterThan_obj,
    'lowerThanOrEqual':lowerThanOrEqual_obj,
    'greaterThanOrEqual':greaterThanOrEqual_obj,
    'like':strlike_obj,
    'likeInSet':strlikeInSet_obj,
    'likeOutSet':strlikeOutSet_obj,
    
    #####ARRAY OPERATORS##################
    'likeContainSet':strlikeContainSet_obj,
    'likeNotContainSet':strlikeNotContainSet_obj,
    
    #####THEMES############################
    'contain_themes':contain_themes_obj
}

SET_MAP_FILTER_TYPE_obj=set(MAP_FILTER_TYPE_obj.keys())


def filter_stage(dataset,stage): #the data set must be an array of dictionnaries
    '''
    {
        'dimensionName':'COUNTRY',
        'equal':'Greece'
    }
    '''
    filteredDataSet=[]
    typeOfCondition=(set(stage.keys()) & set(MAP_FILTER_TYPE.keys())).pop()
    valueOfCondition=stage[typeOfCondition]
    dimensionName=stage['dimensionName']
    filteredDataSet=MAP_FILTER_TYPE[typeOfCondition](dataset,dimensionName,valueOfCondition)
    return filteredDataSet


def filter_stage_obj(obj,stage): #the data set must be an array of dictionnaries
    '''
    {
        'dimensionName':'COUNTRY',
        'equal':'Greece'
    }
    '''
    typeOfCondition=(set(stage.keys()) & SET_MAP_FILTER_TYPE_obj).pop()
    valueOfCondition=stage[typeOfCondition]
    dimensionName=stage['dimensionName']
    objRet=MAP_FILTER_TYPE_obj[typeOfCondition](obj,dimensionName,valueOfCondition)
    return objRet

def filter_pipeline(dataset,pipeline):
    #here we do multiple pass can we if we have multiple stage do at maximum one pass
    filteredDataSet=[dict(d) for d in dataset]
#     filteredtoReturn=[]
#     
#     for d in filteredDataSet:
        
    
    for stage in pipeline:
        filteredDataSet=filter_stage(filteredDataSet,stage)
    return filteredDataSet


def filter_pipeline_obj_simple(dataset,pipeline):
    filteredtoReturn=[]
    size_dataset=len(dataset)
    filteredDataset_appender=filteredtoReturn.append
    
    pipelineOpt=[]
    
    for stage in pipeline:
        typeOfCondition=(set(stage.keys()) & SET_MAP_FILTER_TYPE_obj).pop()
        valueOfCondition=stage[typeOfCondition]
        dimensionName=stage['dimensionName']
        pipelineOpt.append([stage['dimensionName'],stage[typeOfCondition],MAP_FILTER_TYPE_obj[typeOfCondition]])
    
    for i,d in enumerate(dataset):
        for dimensionName,valueOfCondition,filterToCall in pipelineOpt:
            obj=filterToCall(d,dimensionName,valueOfCondition)
            if obj is None :
                break
        if obj is not None :
            filteredDataset_appender(obj)
    return filteredtoReturn,bitwise


def filter_pipeline_obj(dataset,pipeline,bitwiseAttr=None):
    filteredtoReturn=[]
    size_dataset=len(dataset)
    filteredDataset_appender=filteredtoReturn.append
    bitwise=[True]*size_dataset if bitwiseAttr is None else bitwiseAttr[:]
    
    pipelineOpt=[]
    pipelineOpt_append=pipelineOpt.append
    for stage in pipeline:
        typeOfCondition=(set(stage.keys()) & SET_MAP_FILTER_TYPE_obj).pop()
        valueOfCondition=stage[typeOfCondition]
        dimensionName=stage['dimensionName']
        
#         if typeOfCondition=='likeContainSet':
#             iterator_valueInCondition=iter(valueOfCondition)
#             iteratorRegExp=[]
#             for regularExpression in iterator_valueInCondition:
#                 regularExp = str(regularExpression)
#                 regularExp=regularExp.replace('.','\.')
#                 regularExp=regularExp.replace('%','.*')
#                 regularExp=regularExp.replace('_','.')
#                 regularExp='^'+regularExp+'$'
#                 iteratorRegExp.append(re.compile(regularExp))
#             pipelineOpt.append([stage['dimensionName'],iteratorRegExp,MAP_FILTER_TYPE_obj[typeOfCondition]])
#         else:
        pipelineOpt_append([stage['dimensionName'],stage[typeOfCondition],MAP_FILTER_TYPE_obj[typeOfCondition]])
        
    to_ret_set=set(range(len(dataset)))
    if len(pipeline)>0:       
        for i,d in enumerate(dataset):
            obj=d
            if (bitwise[i]):
                for dimensionName,valueOfCondition,filterToCall in pipelineOpt:
                    obj=filterToCall(d,dimensionName,valueOfCondition)
                    if obj is None :
                        bitwise[i]=False
                        to_ret_set-={i}
                        break
                if obj is not None :
                    bitwise[i]=True
                    filteredDataset_appender(obj)
    else :
        filteredtoReturn= dataset[:]
    return filteredtoReturn,to_ret_set

#################################################################



def workflowStage_filter(
        inputs={},
        configuration={},
        outputs={},
        workflow_stats={}
    ):
    
    '''
    {
    
        'id':'stage_id',
        'type':'filter',
        'inputs': {
            'dataset':[]
            #can be value or record or array
        },
        'configuration': {
            'pipeline':[
                {
                    'dimensionName':'dim_name', # if it's a dataset or a record in entry
                    'equal': 'value_expression' #expression is in function of other stages and the dataset
                    #normal operators : equal | notEqual | inSet | outSet | inInterval | outInterval | lowerThan | greaterThan | like | likeInSet | likeOutSet
                    #set operators : likeContainSet | likeNotContainSet
                    # the expression can contain avg(attribute) or std(attribute) if numeric values are concerned
                }
            ],
            'bitwise':[] #filter according the bitwise first, if None do nothing
        },
        'outputs':{
            'dataset':[],
            #can be value or record or array,
            'bitwise':[] 
            #contain the bitwise array (True or False) of the filtered results 
        }
    }
    '''
    
    
    localConfiguration={}
    localConfiguration['pipeline']=configuration.get('pipeline',[])
    localConfiguration['bitwise']=configuration.get('bitwise',None)
    
    
    
    
    results=[]
    
    if inputs.has_key('dataset') :
        dataset=inputs['dataset']#bitwise(inputs['dataset'], '', localConfiguration['bitwise'])
        results=filter_pipeline_obj(dataset,localConfiguration['pipeline'],localConfiguration['bitwise'])
        
        outputs['dataset'] = results[0]
        outputs['bitwise'] = results[1]
        
    elif inputs.has_key('array') :   
        usedDataset=[{'value':item} for item in inputs['array']]
        #usedDataset=bitwise(usedDataset, '', localConfiguration['bitwise'])
        for filterStage in localConfiguration['pipeline'] : 
            filterStage['dimensionName']='value'
        
        filterResults=filter_pipeline_obj(usedDataset,localConfiguration['pipeline'],localConfiguration['bitwise'])
        
        results=[item['value'] for item in filterResults[0]]
        outputs['array'] = results
        outputs['bitwise'] = filterResults[1]
        
    elif inputs.has_key('record') : #is a dataset unique object   
        usedDataset=[inputs['record']]
        #usedDataset=bitwise(usedDataset, '', localConfiguration['bitwise'])
        filterResults=filter_pipeline_obj(usedDataset,localConfiguration['pipeline'],localConfiguration['bitwise'])
        results=filterResults[0]
        results = results[0] if len(results)>0 else None
        
        outputs['record'] = results
        outputs['bitwise'] = filterResults[1]                 
    
    elif inputs.has_key('value') :
        usedDataset=[{'value':inputs['value']}]
        #usedDataset=bitwise(usedDataset, '', localConfiguration['bitwise'])
        for filterStage in localConfiguration['pipeline'] : 
            filterStage['dimensionName']='value'
        
        filterResults=filter_pipeline_obj(usedDataset,localConfiguration['pipeline'],localConfiguration['bitwise'])
        
        results=[item['value'] for item in filterResults[0]]
        results = results[0] if len(results)>0 else None
        outputs['value'] = results
        outputs['bitwise'] = filterResults[1]
        
    return outputs
    
    