#coding="utf-8"
import sys,os,time,math,traceback,json
from random import random
from Docs import Docs
from sim_algorathm import sim_algorathm

class kmeans():
    def __init__(self,datafile):
        self.docs = Docs(datafile)
        self.docs.load()
        self.algo = sim_algorathm()        
    def run(self,centers_num=5,loop_cnt = 100):
        rows = self.docs.get_docs_vec()
        #print len(rows)
        #print json.dumps(rows,ensure_ascii=False)
        limits = [[0,0]] * len(rows[0]) 
        for i in range(len(rows)):
            for j in range(len(rows[0]) ) :
                limits[j] = [ min(limits[j][0],rows[i][j] ), max(limits[j][1],rows[i][j])]
        #print len(limits),limits
        centers = [ [ limits[j][0] + (limits[j][1] - limits[j][0])*random() \
           for j in range(len(rows[0])) ] \
                for i in range(centers_num) ]
        #print len(centers),centers[0]
        lastmatch=[[]] * centers_num
        for i in range(loop_cnt):
            print "iter:%d"  % (i)
            bestmatch=[[]] * centers_num
            mindis = 3
            bestcenter = 0
            for j in range( len(rows)) :
                for k in range(len(centers)):
                    #print centers[k]
                    dis = self.algo.sim_pearson( centers[k]  ,rows[j])
                    if dis < mindis:
                        mindis = dis
                        bestcenter = k
                bestmatch[k].append(rows[j])
                #print bestmatch[k]
            if bestmatch == lastmatch:
                break
            lastmatch = bestmatch
            print len(bestmatch)        
            for j in range(len(bestmatch)):
                avg = [0] * len(rows[0])
                if len(bestmatch) ==0:
                    continue
                for k in range(len( bestmatch[j])) :
                    for m in range( len( bestmatch[j][k])):
                        avg[m] += bestmatch[j][k][m]         
                for k in range(len(avg)):
                    avg[k] = float(avg[k])/len( bestmatch[j])
                print j
                centers[j]  = avg   
        print lastmatch[0]
if __name__ == '__main__':
    km = kmeans(sys.argv[1])
    km.run()
