import numpy as np
import time

def deep_search(i,j):
    data=data_matrix[i,j]
    cost=cost_matrix[i,j]
    
    #use transformation matrix to change direction by 90 degrees clockwise
    dir_vector=np.array([[-1],[0]])
    transform_matrix=np.array([[0,1],[-1,0]])
    for iter in range(4):
        next_i=i+dir_vector[0,0]
        next_j=j+dir_vector[1,0]
        if next_i>=0 and next_i<l_row and next_j>=0 and next_j<l_col:
            next_data=data_matrix[next_i,next_j]
            #update cost
            if next_data<data and (cost+1)>cost_matrix[next_i,next_j]:
                cost_matrix[next_i,next_j]=cost+1
                deep_search(next_i,next_j)
        dir_vector=transform_matrix.dot(dir_vector)
    pass

def explore_start_from_position(start_i,start_j,start_value):
    #print "start position: (%d,%d), starting value= %d" % (start_i,start_j,start_value)
    
    log="start_value:%d\tstart position:(%d,%d)" % (start_value,start_i,start_j)
    #clear cost matrix each time starting from a new position
    cost_matrix[:]=1
    #calculate
    deep_search(start_i,start_j)
    
    #post process
    #print "cost matrix"
    #print cost_matrix
    length=cost_matrix.max()
    indices = np.where(cost_matrix == length)
    end_i=indices[0][0];end_j=indices[1][0];
    end_value=data_matrix[indices][0]
    #print "end position: (%d,%d), end value= %d" % (end_i,end_j,end_value)
    log=log+"\tend position:%d" % end_value
    drop=start_value-end_value
    #print "length=%d" % length
    #print "drop=%d" % drop
    log="length=%d\tdrop=%d\t" % (length,drop) +log
    time1=[]
    time1.append(time.time()-start_time)
    #print log
    #print "computation time=%fsecs" % (time1[0])
    return length,drop

def explore_start_from_value(start_value):
    #print "start value: %d" % start_value    
    indices = np.where( data_matrix ==  start_value)
    #print "there is(are) %d start position(s)." % indices[0].size
    
    cml=1;cmd=0;   #current_max_length, current_max_drop   
    for i in range(indices[0].size):
        start_i=indices[0][i]
        start_j=indices[1][i];
        length,drop=explore_start_from_position(start_i,start_j,start_value)
        if length>cml:
            cml=length;cmd=drop;
        elif length==cml and drop>cmd:
            cmd=drop
    
    return cml,cmd
 
#init
start_time=time.time()
#data_matrix=np.array([[4,8,7,3],[2,5,9,3],[6,3,2,5],[4,4,1,6]])
data_matrix=np.loadtxt('map.txt',skiprows=1)
[l_row,l_col]=data_matrix.shape
cost_matrix=np.ones(data_matrix.shape)

value_list=data_matrix.ravel()
value_list=np.unique(value_list)
value_list=value_list[::-1]
sv=value_list[value_list.size-1]#smallest value
cml=1;cmd=0;   #current_max_length, current_max_drop

for index in range(value_list.size):
    cv=value_list[index]    #current value
    lpl=cv-sv+1   #longest possible length for those starting values < current value
    if cml>lpl:
        break
    
    (length,drop)=explore_start_from_value(cv)
    if length>cml:
        cml=length;cmd=drop;
    elif length==cml and drop>cmd:
        cmd=drop
    else:
        pass
    index=index+1
print "result, length=%d and drop=%d" % (length,drop)
print "computation time=%fsecs" % (time.time()-start_time)
#prepare
