'''
Created on 1 mars 2017

@author: Adnene
'''
from operator import is_not,or_
from functools import partial,reduce


def get_domain_from_dataset_nominal(distinct_values):
    return sorted(distinct_values),{}

def get_starting_pattern_nominal(domain):
    starting_pattern=domain[:]
    starting_refinement=0
    default_widthmax=0
    return starting_pattern,starting_refinement,default_widthmax

def value_to_yield_nominal(domain,pattern,refinement_index,widthmax):
    returned=list(filter(partial(is_not, None), pattern))

    return returned if len(returned) else None


def children_nominal_bottom_up(domain,pattern,refinement_index,widthmax=0):
    for i in range(refinement_index,len(domain)):
        possible_child=pattern+[domain[i]]
        yield possible_child,i+1


def enumerator_nominal_bottom_up(domain,pattern,refinement_index,widthmax=0):

    yield pattern
    for child,refin_child in children_nominal_bottom_up(domain,pattern,refinement_index,widthmax):
        for child_pattern in enumerator_nominal_bottom_up(domain,child,refin_child,widthmax):
            yield child_pattern
            
def enumerator_nominal_bottom_up_bfs(domain,pattern_arr=[[]],refinement_index_arr=[0],configuration_arr=[{'flag':True}],widthmax=0):
        
    arr_next=[];arr_next_append=arr_next.append
    arr_refin_next=[];arr_refin_next_append=arr_refin_next.append
    arr_config_next=[];arr_config_next_append=arr_config_next.append
    for pattern,refinement_index,config in zip(pattern_arr,refinement_index_arr,configuration_arr):
        config_new=config.copy()
        yield pattern,config_new
        if config_new['flag']:
            for child,refin_child in children_nominal_bottom_up(domain,pattern,refinement_index,widthmax):
                arr_next_append(child)
                arr_refin_next_append(refin_child)
                arr_config_next_append(config_new)
        
    if len(arr_next)>0:
        for child_pattern,child_config in enumerator_nominal_bottom_up_bfs(domain,arr_next,arr_refin_next,arr_config_next,widthmax):
            yield child_pattern,child_config      
            
def children_nominal(domain,pattern,refinement_index,widthmax=0,others=None):
    
    for i in range(refinement_index,len(domain)):
        if pattern[i] is None:
            continue
        possible_child=pattern[:]
        possible_child[i]=None
        yield possible_child,i+1

def children_withSupport_nominal(attr,wholeDataset,p_indices,p_indices_bitset,closed=True):
    
    pattern=attr['pattern']
    domain=attr['domain']#tree
    index_attr=attr['index_attr']
    index_attr_bitset=attr['index_attr_bitset']
    refinement_index=attr['refinement_index']
    widthmax=attr['widthmax']

    len_p=len(pattern)
    
    for i in range(refinement_index,len(domain)):
        if pattern[i] is None:
            continue
        possible_child=pattern[:]
        possible_child[i]=None
        indices_new,indices_bitset_new=compute_full_support_nominal_with_bitset(p_indices,p_indices_bitset,attr,closed=closed)
        support_new=[wholeDataset[ind] for ind in indices_new]

        yield possible_child,i+1,support_new,indices_new,indices_bitset_new

        
        
        
def enumerator_nominal(domain,pattern,refinement_index,widthmax=0):
    yielded_pattern=value_to_yield_nominal(domain,pattern,refinement_index,widthmax)
    if yielded_pattern is not None:
        yield yielded_pattern
    for child,refin_child in children_nominal(domain,pattern,refinement_index,widthmax):
        for child_pattern in enumerator_nominal(domain,child,refin_child,widthmax):
            yield child_pattern
            
def pattern_cover_object_nominal(domain,pattern,refinement_index,record,attribute):
    return record[attribute] in pattern

def pattern_cover_object_nominal_index(pattern,record,attribute):
    return record[attribute] in pattern

def object_value_for_index_nominal(domain,record,attribute):
    return record[attribute]   

def encode_sup(arr_pos,len_map_keys):
    to_shift_in_last=len_map_keys-arr_pos[-1]
    for i in range(len(arr_pos)-1,0,-1):#range(1,len(arr_pos))[::-1]:
        arr_pos[i]-=arr_pos[i-1]
    ret=1
    for i in arr_pos:
        ret=(ret<<i)|1
    ret=ret<<to_shift_in_last
    if arr_pos[0]==0:
        ret=bin(ret)[:1:-1]
    else:
        ret=bin(ret)[:2:-1]+'0'
    return int(ret,2)

def index_correspondant_to_nominal(attr,indexall):
    attr_name=attr['name']
    index_attr={key:set() for key in attr['domain']}
    for i in range(len(indexall)):
        index_attr[indexall[i][attr_name]]|={i}
    len_indexall=len(indexall)
    index_attr_bitset={}
    for t in index_attr:
        index_attr_bitset[t]=encode_sup(sorted(index_attr[t]),len_indexall)
    attr['index_attr_bitset']=index_attr_bitset

    attr['index_attr']=index_attr 
    
def compute_full_support_nominal(set_indices_prec,attr,closed=True):
    #print attr['pattern'],'aha'
    attr_pattern=attr['pattern']
    return set_indices_prec&set.union(*(attr['index_attr'][x] for x in list(filter(partial(is_not, None), attr_pattern))) )        

def compute_full_support_nominal_with_bitset(set_indices_prec,datasetIndices_bitset,attr,closed=True):
    #print attr['pattern'],'aha'
    attr_pattern=attr['pattern']
    index_attr_bitset=attr['index_attr_bitset']
    diff=set(filter(partial(is_not, None), attr['parent']))-set(filter(partial(is_not, None), attr_pattern))
    #print (attr['parent'],attr['pattern'],diff,attr['refinement_index'])
    #input('...')
    if closed:
        #print('xXx')
        if len(diff)>0:
            return set_indices_prec-set.union(*(attr['index_attr'][x] for x in diff))  , datasetIndices_bitset&~reduce(or_,[index_attr_bitset[x] for x in diff])
        else:
            return set_indices_prec,datasetIndices_bitset

    return set_indices_prec&set.union(*(attr['index_attr'][x] for x in list(filter(partial(is_not, None), attr_pattern))))  , datasetIndices_bitset&reduce(or_,[index_attr_bitset[x] for x in list(filter(partial(is_not, None), attr_pattern))])




def infimum_nominal(domain,p1,p2):
    return sorted(set(p1)|set(p2))

def closed_nominal(domain,list_patterns):
    list_set_patterns = [{item} for item in list_patterns]
    clos=reduce(set.union,list_set_patterns)
    res=domain[:]
    for k in range(len(res)):
        if res[k] not in clos:
            res[k]=None
    return res

def closed_nominal_index(domain,datasetIndices,list_patterns,attr):
    attr_name=attr['name']
    list_patterns=[x[attr_name] for x in list_patterns]
    list_set_patterns = [{item} for item in list_patterns]
    clos=reduce(set.union,list_set_patterns)
    res=domain[:]
    for k in range(len(res)):
        if res[k] not in clos:
            res[k]=None
    return res

def respect_order_nominal(p1,p2,refinement_index):
    return False if any(p1[i]!=p2[i] for i in range(0,refinement_index)) else True


def respect_order_nominal_not_after_closure(p1,p2,refinement_index_1,refinement_index_2):
    return False if any(p1[i]!=p2[i] for i in range(0,refinement_index_1)) else True

def closure_continueFrom_nominal(domain,pattern,closed,refinement_index): #what is the pattern which represent the one that we need to continue from after closing (it's none if the lexicographic order is not respected)
    return closed

def equality_nominal(p1,p2):
    return p1==p2

def p1_subsume_p2_nominal(p1,p2):
    return set(p2)<=set(p1)  