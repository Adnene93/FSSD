from operator import is_not,or_
from functools import partial
#from intbitset import intbitset

def get_domain_from_dataset_simple(distinct_values):
    return sorted(distinct_values),{}

def get_starting_pattern_simple(domain):
    starting_pattern=domain[:]
    starting_refinement=0
    default_widthmax=0
    return starting_pattern,starting_refinement,default_widthmax


def value_to_yield_simple(domain,pattern,refinement_index,widthmax):
#     returned=filter(partial(is_not, None), pattern)    
#     return returned if len(returned) else None
    #if len(pattern)>1: return None
    return pattern[:]

# def children_simple(domain,pattern,refinement_index,widthmax=0):
#     if (len(pattern)-pattern.count(None))>1:
#         for i in range(refinement_index,len(domain)):
#             if pattern[i] is None:
#                 continue
#             possible_child=[None]*i+[pattern[i]]+[None]*(len(domain)-(i+1))
#             yield possible_child,len(domain)
            
def children_simple(domain,pattern,refinement_index,widthmax=0,others=None):
    if len(pattern)>1:
        for i in range(refinement_index,len(pattern)):
            possible_child=[pattern[i]]
            yield possible_child,len(domain)
        

def children_withSupport_simple(attr,wholeDataset,p_indices,p_indices_bitset,closed=True):
    
    pattern=attr['pattern']
    domain=attr['domain']#tree
    index_attr=attr['index_attr']
    index_attr_bitset=attr['index_attr_bitset']
    refinement_index=attr['refinement_index']
    widthmax=attr['widthmax']
    len_p=len(pattern)

    if len(pattern)>1:
        for i in range(refinement_index,len(pattern)):
            possible_child=[pattern[i]]
            indices_new,indices_bitset_new=compute_full_support_simple_with_bitset(p_indices,p_indices_bitset,attr,closed=closed)
            support_new=[wholeDataset[ind] for ind in indices_new]
            yield possible_child,len(domain),support_new,indices_new,indices_bitset_new



def enumerator_simple(domain,pattern,refinement_index,widthmax=0):
    yielded_pattern=value_to_yield_simple(domain,pattern,refinement_index,widthmax)
    if yielded_pattern is not None:
        yield yielded_pattern
    for child,refin_child in children_simple(domain,pattern,refinement_index,widthmax):
        for child_pattern in enumerator_simple(domain,child,refin_child,widthmax):
            yield child_pattern
            

def pattern_cover_object_simple(domain,pattern,refinement_index,record,attribute):
    return record[attribute] in pattern

def pattern_cover_object_simple_index(pattern,record,attribute):
    return record[attribute] in pattern

def object_value_for_index_simple(domain,record,attribute):
    return record[attribute]  

def infimum_simple(domain,p1,p2):
    return sorted(set(p1)|set(p2))


def closed_simple(domain,list_patterns):
    list_set_patterns = [{item} for item in list_patterns]
    clos=reduce(set.union,list_set_patterns)
    res=domain[:]
    for k in range(len(res)):
        if res[k] not in clos:
            res[k]=None
    return res


def closed_simple_index(domain,datasetIndices,list_patterns,attr):
    attr_name=attr['name']
    list_patterns=[x[attr_name] for x in list_patterns]
    list_set_patterns = set(list_patterns)
    
    return sorted(list_set_patterns)


def respect_order_simple(p1,p2,refinement_index):
    #return False if any(p1[i]!=p2[i] for i in range(0,refinement_index)) else True
    return True

def respect_order_simple_not_after_closure(p1,p2,refinement_index_1,refinement_index_2):
    if len(p1)>1:
        return True
    elif len(p1)==1 and len(p2)==1:
        return p1[0]<=p2[0]
    return False
    # if len(p1)>1 or len(p2)>1:
    #     return (set(p2)<=set(p1))


    

def closure_continueFrom_simple(domain,pattern,closed,refinement_index): #what is the pattern which represent the one that we need to continue from after closing (it's none if the lexicographic order is not respected)
    return closed[:]

# def equality_simple(p1,p2):
#     if (len(p1)>1 and len(p2)>1) or (len(p1)==1 and len(p2)==1):
#         return True
#     return False

def equality_simple(p1,p2):
    if (len(p1)>1 and len(p2)>1):
        return True
        #return set(p2)<=set(p1)
    else:
        return p1==p2
    

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

def index_correspondant_to_simple(attr,indexall):
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
    
    
def compute_full_support_simple(set_indices_prec,attr,closed=True):
    #print attr['pattern'],'aha'
    attr_pattern=attr['pattern']
    if len(attr_pattern)>1:
        return set_indices_prec
    else:
        return set_indices_prec&attr['index_attr'][attr_pattern[0]]
    #return set_indices_prec&reduce(set.union,[attr['index_attr'][p] for p in attr['pattern']]) 

def compute_full_support_simple_with_bitset(set_indices_prec,datasetIndices_bitset,attr,closed=True):
    #print attr['pattern'],'aha'
    attr_pattern=attr['pattern']
    #if closed:
    if len(attr_pattern)>1:
        return set_indices_prec,datasetIndices_bitset
    else:
        # print(attr['index_attr'].keys())
        # print (attr_pattern)
        # print (attr_pattern[0])
        return set_indices_prec&attr['index_attr'][attr_pattern[0]],datasetIndices_bitset&attr['index_attr_bitset'][attr_pattern[0]]
    # else:
    #     return set_indices_prec&reduce(set.union,[attr['index_attr'][p] for p in attr['pattern']])  , datasetIndices_bitset&reduce(or_,[attr['index_attr_bitset'][p] for p in attr['pattern']])

    #return set_indices_prec&reduce(set.union,[attr['index_attr'][p] for p in attr['pattern']]) 


def p1_subsume_p2_simple(p1,p2):
    if len(p1)>1:
        return True
    else:
        return p1==p2
    #return set(p2)<=set(p1)

