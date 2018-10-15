'''
Created on 2 mars 2017

@author: Adnene
'''

from operator import itemgetter,iand,or_
from functools import partial


#intersection_integers=partial(reduce,iand)
def flattenThemesTree(themes):
    arrNew=[]
    for x in themes :
        s= x.split('.')
        
        for i in range(len(s)) :
            sub=''
            for j in range(i+1):
                sub+=s[j]+'.'
            sub=sub[:-1]
            if sub not in arrNew :
                arrNew.append(sub)
    arrNew.append('')
    arrNew.sort()
    return arrNew

def parent_tag(t):
    if len(t)==0:
        return None
    parent='.'.join(t.split('.')[:-1])
    return parent


def all_parents_tag(t): #PARENTS + SELF
    v=t.split('.')
    all_parents=set(['']) | set(['.'.join(v[0:i+1]) for i in range(len(v))])
    return all_parents

def all_parents_tag_exclusive(t): #PARENTS without SELF
    if (t==''):
        return set()
    v=t.split('.')
    all_parents=set(['']) | set(['.'.join(v[0:i+1]) for i in range(len(v)-1)])
    return all_parents

def tree_hmt(themes):
    flat=flattenThemesTree(themes)
    ret_map={};
    for x in flat:
        parent_x=parent_tag(x)
        all_parents=all_parents_tag(x)
        ret_map[x]={'parent':parent_x,'children':[],'right_borthers':[],'all_parents':all_parents,'all_parents_exclusive':all_parents-{x}}
        if parent_x is not None:
            ret_map[parent_x]['children'].append(x)
        
    for x,y in ret_map.iteritems():
        if y['parent'] is not None:
            brothers=ret_map[y['parent']]['children']
            y['right_borthers']=brothers[brothers.index(x)+1:]
    return ret_map



def get_hmt_from_value(v):
    space_index=v.find(' ')
    if space_index>0:
        return v[:space_index]
    return v

def get_label_from_value(v):
    space_index=v.find(' ')
    if space_index>0:
        #return v[space_index+1:]
        return v
    return v

def get_domain_from_dataset_hmt(distinct_values):
    distinct_hmt_without_label=set()
    labelmap={}
    for v in distinct_values:
        theme_v=get_hmt_from_value(v)
        label_v=get_label_from_value(v)
        labelmap[theme_v]=label_v
        distinct_hmt_without_label |= {theme_v}
    tree_of_hmt=tree_hmt(distinct_hmt_without_label)
    for key in tree_of_hmt:
        labelmap[key]=labelmap.get(key,key+' -')
        
    
    #print labelmap
    return tree_of_hmt,labelmap

def get_starting_pattern_hmt(tree):
    starting_pattern=['']
    starting_refinement=0
    default_widthmax=float('inf')
    return starting_pattern,starting_refinement,default_widthmax


def value_to_yield_hmt(tree,pattern,refinement_index,widthmax=0):
    #return None if (refinement_index<len(pattern)-1) and pattern[refinement_index] in tree[pattern[refinement_index+1]]['all_parents']  else pattern
    return pattern



def children_hmt_flag(tree,pattern,refinement_index=None,widthmax=float('inf')):
    len_p=len(pattern)
    refin_index_is_not_last=refinement_index+1<len_p 
    p_refinindex_1=pattern[refinement_index+1] if refin_index_is_not_last else None
    if len_p<=widthmax:
        if refinement_index is None:
            refinement_index=len_p
        last_t=pattern[refinement_index]
        actual=tree[last_t]
        parent=actual['parent']
        for c in actual['children']:
            if refin_index_is_not_last and c>=p_refinindex_1:
                continue
            actual_child=pattern[:]
            actual_child.insert(refinement_index+1,c)
            yield actual_child,refinement_index+1
        if len_p<widthmax:
            brothers_and_uncles=[br for par in actual['all_parents'] for br in tree[par]['right_borthers'] if not (refin_index_is_not_last and br>=p_refinindex_1)]
            for b in brothers_and_uncles:
                actual_child=pattern[:]
                actual_child.insert(refinement_index+1,b)
                yield actual_child,refinement_index+1


def children_hmt(tree,p,refinement_index=None,widthmax=float('inf'),others=None):
    len_p=len(p)
    ##NEW - CANONICAL ORDER PRUNNING##
    if others is not None:
        sup_actu=others['support']
        index_attr=others['index_attr']
    ##NEW##
    for new_refin in range(refinement_index,len_p):
        for c,refin_child in children_hmt_flag(tree,p,new_refin,widthmax):
            ##NEW - CANONICAL ORDER PRUNNING##
            if others is not None :
                sup_new=sup_actu&index_attr[c[refin_child]]
                # if len(sup_new)==0 or canonical_order_went_down_hmt(tree,index_attr,c,refin_child,sup_new):
                #     continue
                if canonical_order_went_down_hmt(tree,index_attr,c,refin_child,sup_new):
                    continue
            ##NEW##
            yield c,refin_child 


def children_withSupport_hmt(attr,wholeDataset,p_indices,p_indices_bitset,closed=True):
    
    p=attr['pattern']
    domain=attr['domain']#tree
    index_attr=attr['index_attr']
    index_attr_bitset=attr['index_attr_bitset']
    refinement_index=attr['refinement_index']
    widthmax=attr['widthmax']

    len_p=len(p)
    
    for new_refin in range(refinement_index,len_p):
        for c,refin_child in children_hmt_flag(domain,p,new_refin,widthmax):
            indices_new=p_indices&index_attr[c[refin_child]]
            if closed and canonical_order_went_down_hmt(domain,index_attr,c,refin_child,indices_new):
                continue
            indices_bitset_new=p_indices_bitset&index_attr_bitset[c[refin_child]]
            support_new=[wholeDataset[ind] for ind in indices_new]
            yield c,refin_child,support_new,indices_new,indices_bitset_new
                

def enumerator_hmt(domain,pattern,refinement_index,widthmax):
    yielded_pattern=value_to_yield_hmt(domain,pattern,refinement_index,widthmax)
    if yielded_pattern is not None:
        yield yielded_pattern
    for child,refin_child in children_hmt(domain,closure_continueFrom_hmt(domain, pattern, pattern, refinement_index),refinement_index,widthmax):
        for child_pattern in enumerator_hmt(domain,child,refin_child,widthmax):
            yield child_pattern
def dfs_tree(tree,p,config={'flag':True}):
    
    yield p,config
    if config['flag']:
        for c in tree[p]['children']:
            for pc,pc_config in dfs_tree(tree,c,config.copy()):
                yield pc,pc_config

# def dfs_tree_interm(tree,p,config={'flag':True}):
    
#     yield p,config
#     if config['flag']:
#         for c in tree[p]['children']:
#             for pc,pc_config in dfs_tree_interm(tree,c,config.copy()):
#                 yield pc,pc_config
#     for c in [br for par in tree[p]['all_parents'] for br in tree[par]['right_borthers']]:
#         for pc,pc_config in dfs_tree_interm(tree,c,config.copy()):
#             yield pc,pc_config

def dfs_tree_interm(tree,p,config={'flag':True}):
    for pc,c in dfs_tree(tree,p,config.copy()):
        yield pc,c

    for par in tree[p]['all_parents']:
        for br in tree[par]['right_borthers']:
            for pc,c in dfs_tree(tree,br,config.copy()):
                yield pc,c




def dfs_tree_direct(tree,p):
    for c in tree[p]['children']:
        yield c

def maximum_tree(tree,set_tag):
    return sorted(set_tag-{tag_parent for tag in set_tag for tag_parent in tree[tag]['all_parents_exclusive']})


def pattern_cover_object_hmt(tree,pattern,refinement_index,record,attribute):
    return set(pattern) <= {par for x in record[attribute] for par in tree[x]['all_parents']}



def pattern_cover_object_hmt_index(pattern,record,attribute):
    return set(pattern) <= record[attribute]
#{par for x in record[attribute] for par in tree[x]['all_parents']}

def object_value_for_index_hmt(tree,record,attribute):
    if len(record[attribute])==0:
        record[attribute]=[''] ####PARLIAMENT
    
    return {par for x in record[attribute] for par in tree[get_hmt_from_value(x)]['all_parents']}

def infimum_hmt(tree,p1,p2):
    toRet=set()
    if p1!=p2:
        toRet=set(maximum_tree(tree,{par for x in p1 for par in tree[x]['all_parents']} & {par for x in p2 for par in tree[x]['all_parents']}))
    else :
        toRet=set(maximum_tree(tree,set(p1)))
    return sorted(toRet)


def closed_hmt(tree,list_patterns):
    list_patterns_new=[{par for x in pat for par in tree[x]['all_parents']} for pat in list_patterns]
    #list_set_patterns = map(set,list_patterns)
    return maximum_tree(tree, reduce(set.intersection,list_patterns_new))




    
    

def respect_order_hmt(p1,p2,refinement_index):
    if p1==p2:
        return True
    range_len_min_comp=reversed(range(refinement_index))
    res=True
    
    if (p1[refinement_index]>p2[refinement_index]):
        return False
    
    for i in range_len_min_comp:
        res&=(p1[i]==p2[i])
        if not res:
            return res
    return True

def respect_order_hmt_not_after_closure(p1,p2,refinement_index_1,refinement_index_2):
    if p1==p2:
        return True
    range_len_min_comp=reversed(range(refinement_index_1))
    res=True
    
    if (p1[refinement_index_1]>p2[refinement_index_1]):
        return False
    
    for i in range_len_min_comp:
        res&=(p1[i]==p2[i])
        if not res:
            return res
    return True


def closure_continueFrom_hmt(tree,pattern,closed,refinement_index): #what is the pattern which represent the one that we need to continue from after closing (it's none if the lexicographic order is not respected)
    return closed

def closure_continueFrom_hmt_new(tree,patternArray,closed,refinement_index): #what is the pattern which represent the one that we need to continue from after closing (it's none if the lexicographic order is not respected)
    ret=[];ret_extend=ret.extend;
    if type(patternArray[0]) is not list:
        ret_extend(closure_continueFrom_hmt(tree,patternArray,closed,refinement_index))
        ret_new=ret
    else :
        for pattern in patternArray:
            ret_extend(closure_continueFrom_hmt(tree,pattern,closed,refinement_index))
    
        ret_set={tuple(x) for x in ret}
        ret_sorted=[sorted(s) for s in ret_set]
        ret_refs=[(ret_sorted[i][refinement_index],ret_sorted[i],len(ret_sorted[i])) for i in range(len(ret_sorted))]
    
            
        ret_refs_dict={}
        for refin,pat,length_pat in ret_refs:
            if length_pat not in ret_refs_dict:
                ret_refs_dict[length_pat]=[]
            ret_refs_dict[length_pat].append((refin,pat))
        
        ret_new=[min(ret_refs_dict[k],key=lambda x : x[0])[1] for k in ret_refs_dict]

    return ret_new

   
def equality_hmt(p1,p2):
    return p1==p2


def encode(arr_pos,len_map_keys):
    to_shift_in_last=len_map_keys-arr_pos[-1]
    for i in range(1,len(arr_pos))[::-1]:
        arr_pos[i]-=arr_pos[i-1]
    ret=int(1)
    for i in arr_pos:
        ret=(ret<<i)|1
    ret=ret<<to_shift_in_last
    ##return ret
    return int(bin(ret)[2:][::-1],2)



def decode_int_in_tags(res_integer,mapping,map_index_to_tag_binary={}):
    
    res_n=bin(res_integer)
    len_res_n=len(res_n)-3
    res=set(mapping[len_res_n-(i-2)] for i in xrange(2,len(res_n)) if res_n[i]=='1')
    return res
    
# def trailing_zeros(s):
#     return len(s)-len(s.rstrip('0'))
def pos_0(n):
    count=0
    while n>0:
        n&=(n-1)
        count+=1
    return count

def encoder(arr_pos,len_map_keys):
    to_shift_in_last=len_map_keys-arr_pos[-1]
    for i in range(1,len(arr_pos))[::-1]:
        arr_pos[i]-=arr_pos[i-1]
    ret=int(1)
    for i in arr_pos:
        ret=(ret<<i)|1
    ret=ret<<to_shift_in_last
    return ret

def decode_int_in_tagsr(res_integer,mapping,map_index_to_tag_binary={}):
    
    #res_n=bin(res_integer)[2:]
    
    #res=set(mapping[i] for i in pos_0(res_integer))
    
    res_n=bin(res_integer)
    res=set(mapping[i-2] for i in xrange(2,len(res_n)) if res_n[i]=='1')
    
#     n=res_integer
#     nb_bits_to_consider=len(mapping)-1
#     root_representation=encode([0],nb_bits_to_consider)
#     res2={''}
#     for x in map_index_to_tag_binary:
#         if x & n != root_representation: res2|={map_index_to_tag_binary[x]}
#     
#     res=res2
    
#     len_mapping=len(mapping)-1
#     newres=set();newres_add=newres.add
#     rmap=xrange(len(mapping))
#     for k in rmap:
#         if res_integer%2:
#             newres_add(mapping[len_mapping-k])
#         res_integer=res_integer>>1
#     res=newres

    return res


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


def index_correspondant_to_hmt(attr,indexall):
    attr_name=attr['name']
    index_attr={key:set() for key in attr['domain'].keys()}
    len_indexall=len(indexall)
    #print index_attr.keys()
    
    for i in range(len(indexall)):
        for t in indexall[i][attr_name]:
            index_attr[t]|={i}

    ############REMOVE RIGHT BROTHERS THAT HAVE NO INTERSECTION WITH THE CURRENT TAG######
    sup_thres=1
    tree_dom=attr['domain']
    for t in tree_dom:
        new_right_brothers=[];new_right_brothers_append=new_right_brothers.append
        for t2 in tree_dom[t]['right_borthers']:
            if len(index_attr[t] & index_attr[t2])>=sup_thres:
                new_right_brothers_append(t2)
        tree_dom[t]['right_borthers']=new_right_brothers

    ############REMOVE RIGHT BROTHERS THAT HAVE NO INTERSECTION WITH THE CURRENT TAG######
    
    index_attr_bitset={}
    for t in index_attr:
        index_attr_bitset[t]=encode_sup(sorted(index_attr[t]),len_indexall)
    attr['index_attr_bitset']=index_attr_bitset


    attr['index_attr']=index_attr #Index_attr associate each tag to a set of index of objects

def inter_num(a,b):
    return a&b


def closed_hmt_index_old(tree,datasetIndices,list_patterns,attr):
    attr_name=attr['name']


    map_index_to_tag=attr['map_index_to_tag']
    map_obj_to_tags=attr['map_obj_to_tags']
    
    datasetIndicesIter=iter(datasetIndices)
    res_n=map_obj_to_tags[next(datasetIndicesIter)]
    for b in datasetIndicesIter : res_n&=map_obj_to_tags[b]
    map_index_to_tag_binary=attr['map_index_to_tag_binary']
    res=decode_int_in_tags(res_n, map_index_to_tag,map_index_to_tag_binary)
    #ret=maximum_tree(tree,res)
    ret=sorted(res)
    return ret


def canonical_order_went_down_hmt(tree,index_attr,pattern,refinement_index,datasetIndices):
    stop_verif=False
    #pattern=attr['pattern']
    set_pattern=set(pattern)
    #refinement_index=attr['refinement_index']
    p_refin=pattern[refinement_index]
    
    for k in range(refinement_index):
        pk=pattern[k]
        for c in tree[pk]['children']:#dfs_tree_direct(tree,pk):
            if c>=p_refin:
                break
            if c not in set_pattern and datasetIndices <= index_attr[c]:
                stop_verif=True
                break
        if stop_verif: break
    return stop_verif




def closed_hmt_indexs(tree,datasetIndices,list_patterns,attr):
    attr_name=attr['name']
    pattern=attr['pattern']
    set_pattern=set(pattern)
    refinement_index=attr['refinement_index']
    p_refin=pattern[refinement_index]
    index_attr=attr['index_attr']
    cl=pattern[:]
    cl_append=cl.append

    # stop_verif=False
    # for k in range(refinement_index):
    #     pk=pattern[k]
    #     for c in tree[pk]['children']:#dfs_tree_direct(tree,pk):
    #         if c>=p_refin:
    #             break
    #         if c not in set_pattern and datasetIndices <= index_attr[c]:
    #             cl_append(c)
    #             stop_verif=True
    #             break
    #     if stop_verif: break
        
    for p,c in dfs_tree(tree,''):
        if p in set_pattern :
            continue
        if datasetIndices <= index_attr[p]:
            if p not in set_pattern :
                cl_append(p)
                # if p<p_refin:
                #     break
        else:
            c['flag']=False
    ret=sorted(cl)
    return ret


def closed_hmt_index(tree,datasetIndices,list_patterns,attr):
    attr_name=attr['name']
    pattern=attr['pattern']
    set_pattern=set(pattern)
    refinement_index=attr['refinement_index']
    p_refin=pattern[refinement_index]
    index_attr=attr['index_attr']
    cl=pattern[:]
    cl_append=cl.append
    for p,c in dfs_tree_interm(tree,p_refin):
        if p in set_pattern :
            continue
        if datasetIndices <= index_attr[p]:
            cl_append(p)
        else:
            c['flag']=False

    ret=sorted(cl)
    #print pattern,ret,stop_verif,canonical_order_went_down(tree,datasetIndices,attr)
    #raw_input('...')
    return ret
    
def compute_full_support_hmt(set_indices_prec,attr,closed=True):
    #print attr['pattern'],'aha'
    index_attr=attr['index_attr']
    index_attr_bitset=attr['index_attr_bitset']
    pattern=attr['pattern']
    refin=attr['refinement_index']
    
    # index_attr_bitset=attr['index_attr_bitset']
    # attr['support_bitset']=attr['support_bitset']&index_attr_bitset[pattern[refin]]

    return set_indices_prec&index_attr[pattern[refin]]#reduce(set.intersection,(index_attr[p] for p in pattern[refin:]))
    

def compute_full_support_hmt_with_bitset(set_indices_prec,datasetIndices_bitset,attr,closed=True):
    #print attr['pattern'],'aha'
    index_attr=attr['index_attr']

    pattern=attr['pattern']
    refin=attr['refinement_index']
    
    # attr['support_bitset']=attr['support_bitset']&index_attr_bitset[pattern[refin]]


    if closed:
        return set_indices_prec&index_attr[pattern[refin]],datasetIndices_bitset&attr['index_attr_bitset'][pattern[refin]]
    else:
        return set_indices_prec&reduce(set.intersection,[index_attr[p] for p in attr['pattern']]),datasetIndices_bitset&reduce(and_,[index_attr_bitset[p] for p in attr['pattern']])
    #return set_indices_prec&index_attr[pattern[refin]],datasetIndices_bitset&attr['index_attr_bitset'][pattern[refin]]

    
def similarity_between_descriptions(d1,d2):
    d1_extended=reduce(set.union,(all_parents_tag(t1)-{''} for t1 in d1))
    d2_extended=reduce(set.union,(all_parents_tag(t2)-{''} for t2 in d2))
    return True if  len(d1_extended&d2_extended)>0 else False
    #return True if  d1_extended<=d2_extended or set(d2)<=d1_extended else False


def p1_subsume_p2_hmt_old(p1,p2):
    if len_p1>len_p2:
        return False
    ret=True
    for t in p1:
        try:
            ret&=any(t2[:len(t)]==t for t2 in p2 if t<=t2)#any(t2.find(t,0,len(t))==0 for t2 in p2)
            if not ret:
                return False
                
        except:
            return False
    return ret

def p1_subsume_p2_hmt(p1,p2):
    # p1_all={par for t in p1 for par in all_parents_tag(t)}
    # p2_all={par for t in p2 for par in all_parents_tag(t)}
    #return p1_all<=p2_all
    ret=True
    len_p1=len(p1)
    len_p2=len(p2)
    if len_p1>len_p2:
        return False
    
    k1=0
    k2=0
    t2=p2[k2]
    t1=p1[k1]
    while k1 < len_p1 and k2 < len_p2:
        while t1>t2:
            k2+=1
            if k2==len_p2:
                break
            t2=p2[k2]
        if k2==len_p2:
            break
        if t2[:len(t1)]==t1:
            k1+=1
            if k1==len_p1:
                break
            t1=p1[k1]
        else:
            k2+=1
            if k2==len_p2:
                break
            t2=p2[k2]
    if k1==len_p1:
        return True
    return False






    # for t in p1:
    #     try:
    #         ret&=any(t2[:len(t)]==t for t2 in p2 if t<=t2)#any(t2.find(t,0,len(t))==0 for t2 in p2)
    #         if not ret:
    #             return False
                
    #     except:
    #         return False
        
    # return ret
    #return p1_all<=p2_all   
    
    