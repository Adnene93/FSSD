'''
Created on 5 janv. 2017

@author: Adnene
'''

def cover(arr_1,arr_2): #arr_1 and arr_2 are boolean array representing the elements of a set
    
    if arr_1 is None or arr_2 is None :
        return 0
    else :
        
        arr_1_inter_arr_2 = [x and y for x,y in zip(arr_1,arr_2)]
        arr2_count=arr_2.count(True)
        if arr2_count==0:
            return 0
        else :
            return float(arr_1_inter_arr_2.count(True)) / arr2_count
        
        
        
def workflowStage_coverabilityWithVisited(
        inputs={},
        configuration={},
        outputs={},
        workflow_stats={}
    ):
    
    '''
    {
    
        'id':'stage_id',
        'type':'misc_cover',
        'inputs': {
            'bitwise':[],
            'pattern':[],
            'bitwises_array':[],
            'patterns_array':[]
        },
        'configuration': {
            
        },
        'outputs':{
            'cover':0
        }
    }
    '''
    
    
    bitwise=inputs['bitwise']
    bitwises_array=inputs['bitwises_array']
    pattern=inputs.get('pattern',None)
    patterns_array=inputs.get('patterns_array',None)
    coverToRet=0
    
    if pattern is not None :
       
        for x,p in zip(bitwises_array,patterns_array):
            if (x.count()>0 and p[2]==pattern[2]):
                print p[2],pattern[2]
                coverToRet=max(coverToRet,(bitwise & x).count()/float(x.count())) 
                if coverToRet==1:
                    break
    else :
        for x in bitwises_array:
            if (x.count()>0):
                
                coverToRet=max(coverToRet,(bitwise & x).count()/float(x.count())) 
                if coverToRet==1:
                    break
    outputs['cover']=coverToRet
    return outputs


def workflowStage_coverabilityMultiple(
        inputs={},
        configuration={},
        outputs={},
        workflow_stats={}
    ):
    
    '''
    {
    
        'id':'stage_id',
        'type':'misc_covermultiple',
        'inputs': {
            'bitwises':[],
            'bitwises_arrays':[],
            'pattern':[],
            'patterns_array':[]
        },
        'configuration': {
            
        },
        'outputs':{
            'cover':0
        }
    }
    '''
    
    
    bitwise=inputs['bitwises']
    bitwises_array=inputs['bitwises_arrays']
    pattern=inputs.get('pattern',None)
    
    patterns_array=inputs.get('patterns_array',None)
    coverToRet=0
    
    range_nb_attributes=range(len(bitwises_array))
    range_nb_visited=range(len(bitwises_array[0]))
    
    valToRemember=[]
    patternToRemember=[]
    
    for k in range_nb_visited:
            
        x=[]
        cover_arr=[]
        for t in range_nb_attributes:
            x.extend([bitwises_array[t][k]])
        tmp=1
        for t in range_nb_attributes:
            if (x[t].count()>0):
                cover_arr.append(((bitwise[t] & x[t]).count()/float(x[t].count())))
            else :
                cover_arr.append(0.)
            
            
        tmp= reduce(lambda x, y: x*y, cover_arr)    
        if tmp>coverToRet:
            coverToRet = tmp
            valToRemember = cover_arr
            patternToRemember= patterns_array[k]
        
        if coverToRet==1:
            #print 'found : ', patterns_array[k]
            break
    
    print  coverToRet,valToRemember,patternToRemember
    outputs['cover']=coverToRet
    return outputs