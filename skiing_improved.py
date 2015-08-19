import numpy as np
import time

def deep_search(i,j,data_matrix,cost_matrix):
    data=data_matrix[i,j]
    cost=cost_matrix[i,j]
    
    #use transformation matrix to change direction by 90 degrees clockwise
    dir_vector=np.array([[-1],[0]])
    transform_matrix=np.array([[0,1],[-1,0]])
    for iter in range(4):
        next_i=i+dir_vector[0,0]
        next_j=j+dir_vector[1,0]
        if next_i>=0 and next_i<a_row and next_j>=0 and next_j<a_col:
            next_data=data_matrix[next_i,next_j]
            #update cost
            if next_data<data and (cost+1)>cost_matrix[next_i,next_j]:
                cost_matrix[next_i,next_j]=cost+1
                deep_search(next_i,next_j,data_matrix,cost_matrix)
        dir_vector=transform_matrix.dot(dir_vector)

def explore_start_from_position(start_i,start_j):
    #print "start position: (%d,%d), starting value= %d" % (start_i,start_j,start_value)
    start_value=data_matrix[start_i,start_j]
    log="start value:%d\tstart position:(%d,%d)" % (start_value,start_i,start_j)
    #clear cost matrix each time starting from a new position
    cost_matrix=np.zeros(data_matrix.shape)
    cost_matrix[start_i,start_j]=1
    #calculate
    deep_search(start_i,start_j,data_matrix,cost_matrix)
    
    #post process
    #print "cost matrix"
    #print cost_matrix
    #get the longest length
    length=cost_matrix.max()
    #among multiple longest paths, pick the lowest end point
    indices = np.where(cost_matrix == length)
    end_value=data_matrix[indices].min()
    log="length=%d\tend value=%d\t" % (length,end_value) +log
    time1=[]
    time1.append(time.time()-start_time)
    #print log
    #print "computation time=%fsecs" % (time1[0])
    return length,end_value

def explore_start_from_value(start_value,data_matrix):
    #print "start value: %d" % start_value    
    indices = np.where( data_matrix ==  start_value)
    #print "there is(are) %d start position(s)." % indices[0].size
    
    cml=1;cmd=0;   #current_max_length, current_max_drop   
    for i in range(indices[0].size):
        start_i=indices[0][i]
        start_j=indices[1][i];
        # approach 1, used for small data matrix
        #length,end_value=explore_start_from_position(start_i,start_j)
        # approach 2, used for large data matrix
        length,end_value=get_max_cost_for_position(start_i,start_j)
        drop=start_value-end_value
        if length>cml:
            cml=length;cmd=drop;
        elif length==cml and drop>cmd:
            cmd=drop
   # print "start_value=%d  length=%d  drop=%d" % (start_value,cml,cmd)
    return cml,cmd

# convert coordinate of data matrix 2d into that of data_4d
def convert_coordinate_2d_to_4d(i,j):
    return i/a_row,j/a_col,i%a_row,j%a_col

# convert coordinate of data matrix 4d into that of data_2d
def convert_coordinate_4d_to_2d(p,q,m,n):
    return p*a_row+m,q*a_col+n

# recursively search for max cost via exploring atom cost matrix
def get_max_cost_for_position(i,j):
    #print "i,j %d, %d" % (i,j)
    p,q,m,n=convert_coordinate_2d_to_4d(i,j)
    #print "p,q,m,n %d %d %d %d " %(p,q,m,n)
    #raw_input()
    max_cost=cost_6d[p,q,m,n].max()
    
    #among multiple longest paths, pick the lowest end point
    indices = np.where(cost_6d[p,q,m,n] >0 )
    end_value=(data_4d[p,q][np.where(cost_6d[p,q,m,n]==max_cost)]).min()
    
    for k in range(indices[0].size):
        k_i=indices[0][k];k_j=indices[1][k];
        #print "ki,kj %d %d" %(k_i, k_j)
        k_cost=cost_6d[p,q,m,n,k_i,k_j]
        #if end value is one upper or lower border of atom cost matrix
        #, search further in adjacent atom cost matrix
        border_flag=False
        if k_i==0 and p>0:
            border_flag=True
            next_i,next_j=convert_coordinate_4d_to_2d(p-1,q,a_row-1,k_j)
        elif k_i==a_row-1 and p<m_row-1:
            border_flag=True
            next_i,next_j=convert_coordinate_4d_to_2d(p+1,q,0,k_j)
        if border_flag and data_matrix[next_i,next_j]<data_4d[p,q,k_i,k_j]:
            #print "debug: next_i=%d next_j=%d" % (next_i,next_j)
            #raw_input()#put raw input to pause for debugging purpose
            tmp_cost,tmp_value=get_max_cost_for_position(next_i,next_j)
            if (tmp_cost+k_cost)>max_cost:
                max_cost=(tmp_cost+k_cost)
                end_value=tmp_value
            elif tmp_cost==max_cost:
                end_value=min(end_value,tmp_value) 
        border_flag=False
        #if end value is one left or right border of atom cost matrix
        #, search further in adjacent atom cost matrix
        if k_j==0 and q>0:
            border_flag=True
            next_i,next_j=convert_coordinate_4d_to_2d(p,q-1,k_i,a_col-1)
        elif k_j==a_col-1 and q<m_col-1:
            border_flag=True
            next_i,next_j=convert_coordinate_4d_to_2d(p,q+1,k_i,0)
        if border_flag and data_matrix[next_i,next_j]<data_4d[p,q,k_i,k_j]:
            #print "debug: next_i=%d next_j=%d" % (next_i,next_j)
            #raw_input()#put raw input to pause for debugging purpose
            tmp_cost,tmp_value=get_max_cost_for_position(next_i,next_j)
            if (tmp_cost+k_cost)>max_cost:
                max_cost=(tmp_cost+k_cost)
                end_value=tmp_value
            elif tmp_cost==max_cost:
                end_value=min(end_value,tmp_value)       
    return max_cost,end_value

#init
start_time=time.time()
#data_matrix=np.array([[4,8,7,3],[2,5,9,3],[6,3,2,5],[4,4,1,6]])
data_matrix=np.loadtxt('map.txt',skiprows=1,dtype=np.int16)
sdms=1000#sub data matrix size
data_matrix=data_matrix[:sdms,:sdms]
#print data_matrix
#assign data type
data_matrix.astype(int)
[l_row,l_col]=data_matrix.shape
#size of atom matrix, smallest matrix used to calculate cost
a_row=a_col=20;
#size of macro matrix, used to reshape data_matrix into data_4d
m_row=l_row/a_row;m_col=l_col/a_col;
#print m_row
#print m_col
#reshape data matrix into 4d matrix. the process is a tricky and went through trial and errs
data_3d=np.asarray(np.split(data_matrix,m_col,axis=1))
data_4d=np.asarray(np.split(data_3d,m_row,axis=1))
#print data_4d
#init empty cost matrix 6d
cost_6d=np.zeros([m_row, m_col, a_row, a_col, a_row, a_col],dtype=np.int16)

#init cost matrix 6d
print "initiate 6d cost matrix..."
for p in range(m_row):
    for q in range(m_col):
        for i in range(a_row):
            for j in range(a_col):
                cost_6d[p,q,i,j,i,j]=1
                deep_search(i,j,data_4d[p,q],cost_6d[p,q,i,j])
print "cost matrix initated, cost %f secs" % (time.time()-start_time)

#prepare
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
    
    (length,drop)=explore_start_from_value(cv,data_matrix)
    if length>cml:
        cml=length;cmd=drop;
    elif length==cml and drop>cmd:
        cmd=drop
    index=index+1
print "result, length=%d and drop=%d" % (cml,cmd)
print "computation time=%fsecs" % (time.time()-start_time)
