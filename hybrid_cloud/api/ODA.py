# -*- coding: utf-8 -*-
"""
Created on Sat Dec 03 09:33:57 2016

@author: Sheila
"""
#import numpy as np
import random 
import math
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import copy as cp
def intTo2Str( X , K ):
    """ intTo2Str( X , K )
        将整数 X 转化为 K位2进制字符串
    """
    try:
      X = long( X)
    except:
      X = 0
    try:
      K = int( K)
    except:
      K = 0
    if K<1 :
       K = 1 
    if X<0 :
       FH = 1 ; X = -X
    else:
       FH = 0 
    A =[ 0 for J in xrange( 0, K ) ]
    J = K-1
    while (J>=0) and ( X>0):
          Y = X % 2
          X = X / 2
          A[ J ] = Y
          J = J - 1   
    if FH==1:
       # 求反
       for J in xrange( 0, K):
           if A[J] ==1 :
              A[J] = 0
           else:
              A[J] = 1
       # 末位加1
       J = K - 1
       while J>=0:
             A[J] = A[J] +1
             if A[J]<=1:
                break
             A[J] = 0
             J = J -1
    return "".join([ chr(j+48) for j in A ])


def ODA(R_private, R_any, T, h):
    VM_S=[[1,1,10],[1,2,20],[2,4,40],[4,8,80]]#虚机的规格
    Pr=[0.13,0.25,0.65,1.33]#对应类型虚机在EC2上的价格
    V=3    #调节值
    w=0.05 #拒绝率阈值
    R=R_private+R_any#在当前时隙中所有请求对虚机的请求量
    E_cloud=0#租用公有云的所有花费
    f_cpu=0
    f_memory=0
    f_disk=0
    for f in range(len(R)):
        for f1 in range(4):
            f_cpu+=R[f][f1]*VM_S[f1][0]
            f_memory+=R[f][f1]*VM_S[f1][1]
            f_disk+=R[f][f1]*VM_S[f1][2]
    if (f_cpu<=T[0])and(f_memory<=T[1])and(f_disk<=T[2]):
        x = [1 for raw in range(len(R))]  # 初始所有的值为1
        x_private=[]
        x_any=[]
        for i in range(len(R_private)):
            x_private.append(x[i])
        for i1 in range(len(R_private),len(R)):
            x_any.append(x[i1])
        #print "x_private=", x_private
        #print "x_any=", x_any
        if (len(R_private)*(1-w)-sum(x[:len(R_private)]))>0:
            h+=(len(R_private))*(1-w)-sum(x[:len(R_private)])
            #print "h=", h
        #else:
            #print "h=", h
        for i1 in range (len(R_private),len(R)):
            if x[i1]==0:
                for f1 in range(4):
                    E_cloud+=Pr[f1]*R[i1][f1]*R[i1][4]
        #print "Expense for renting public cloud:",E_cloud,"元"
        return(x_private,x_any,h,E_cloud)
    if (f_cpu>T[0])or(f_memory>T[1])or(f_disk>T[2]):#该时隙所有请求对虚机请求的总量大于私有云剩下的所有量
        p1=[]#装所有请求的向量
        d=[]#记录目标函数中决策变量的系数
        ec=0
        for f in range(len(R_any)):
            for f1 in range(4):
                ec+=V*R_any[f][f1]*Pr[f1]*R_any[f][4]
                d.append(ec)
        for k1 in range(len(R_private)):
            p1.append([h,R_private[k1],k1])#所有请求i的向量，第一项表示请求i的系数，第二三项分别表示请求i对虚机的请求量和请求的时隙
        for k2 in range(len(R_any)):
            p1.append([d[k2],R_any[k2],k2+len(R_private)])#所有请求i的向量，第一项表示请求i的系数，第二三项分别表示请求i对虚机的请求量和请求的时隙
        p=sorted(p1)#将所有请求按照系数从小到大排列  
        As=[]#As为衰减序列
        temp=intTo2Str(0,len(R))
        temp=map(int, temp)
        temp[0]=1
        temp.append(p[0][0])
        As.append(temp)
        for i3 in range(int(math.pow(2,len(R)))):#执行算法的过程
            ds=cp.deepcopy(As[0])
            va1=0
            va2=0
            x = [1 for raw in range(len(R))]  # 初始所有的值为1
            for c in range(len(R)):#由最小衰减序列产生中间解
                if ds[c]==1:
                    index=p[c][2]
                    x[index]=abs(x[index]-1)
            f_cpu = 0
            f_memory = 0
            f_disk = 0
            for c1 in range(len(R)):#中间解下，消耗私有云的资源数
                if x[c1]==1:
                    for c2 in range(4):
                        f_cpu+=R[c1][c2]*VM_S[c2][0]
                        f_memory+=R[c1][c2]*VM_S[c2][1]
                        f_disk+=R[c1][c2]*VM_S[c2][2]
            
            if (f_cpu<=T[0]) and (f_memory<=T[1]) and (f_disk<=T[2]):#判断中间解是否满足限制条件               
                x_private=[]
                x_any=[]
                for i in range(len(R_private)):
                    x_private.append(x[i])
                for i1 in range(len(R_private),len(R)):
                    x_any.append(x[i1])
                #print "x_private:", x_private
                #print "x_any:", x_any
                if (len(R_private)*(1-w)-sum(x[:len(R_private)]))>0:
                    h+=(len(R_private))*(1-w)-sum(x[:len(R_private)])
                    #print "h=", h#求出t时隙时H(t)的值
                #else:
                    #print "h=", h
            
                for i1 in range (len(R_private),len(R)):
                    if x[i1]==0:
                        for i2 in range(4):
                            E_cloud+=Pr[i2]*R[i1][i2]*R[i1][4]
                #print "Expense for renting public cloud:",E_cloud,"元"
                return(x_private,x_any,h,E_cloud)
            if (f_cpu>T[0])or(f_memory>T[1])or(f_disk>T[2]):#中间解不满足限制条件，变异当前衰减序列，产生新的As
                if ds[len(R) - 1] == 0:
                    del As[0]
                    key_index = 0
                    for j1 in range(len(R))[::-1]:
                        if ds[j1] == 1 and j1 < len(R) - 1:
                            key_index = j1
                            break
                    tem1 = cp.deepcopy(ds)
                    tem1[key_index + 1] = 1
                    for j3 in range(len(tem1) - 1):
                        if tem1[j3] == 1:
                            va1 += p[j3][0]
                    tem1[len(tem1) - 1] = va1
                    n = len(As)
                    if n == 0:
                        As.append(tem1)
                    if n > 0:
                        flag = 0  # 标识As中的衰减值是否有大于新衰减值的
                        for j4 in range(n):
                            if As[j4][len(As[j4]) - 1] >= va1:
                                flag = 1
                                break
                        if flag == 0:
                            As.append(tem1)
                        if flag == 1:
                            As.insert(j4, tem1)
                    m = len(As)
                    tem2 = cp.deepcopy(tem1)
                    tem2[key_index] = 0
                    for j3 in range(len(tem2) - 1):
                        if tem2[j3] == 1:
                            va2 += p[j3][0]
                    tem2[len(tem2) - 1] = va2
                    if m == 0:
                        As.append(tem2)
                    if m > 0:
                        flag = 0  # 标识As中的衰减值是否有大于新衰减值的
                        for j4 in range(m):
                            if As[j4][len(As[j4]) - 1] >= va2:
                                flag = 1
                                break
                        if flag == 0:
                            As.append(tem2)
                        if flag == 1:
                            As.insert(j4, tem2)
                if ds[len(R) - 1] == 1:
                    del As[0]