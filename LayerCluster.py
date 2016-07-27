#coding="utf-8"
import sys,os,time,math,traceback,json
from Docs import Docs
from sim_algorathm import sim_algorathm

class Cluster() :
    def __init__(self, id,data ,cid,left = None, right=None):
        self.id = id
        self.cid = cid
        self.data = data  
        self.left = left
        self.right = right
    
    def print_clut(self,indent=1,deep=1,docs=None ):
        dig = ""
        if self.cid>=0:
            dig = json.dumps(docs.get_label_vec(self.id),ensure_ascii = False)
            #dig = ""
        print "%d%s[%d]:%s" % (deep,"-"*indent*deep,self.cid , dig) 
        if self.left != None:
            self.left.print_clut(indent,deep+1 ,docs)    
        if self.right != None:
            self.right.print_clut(indent,deep+1 ,docs)    
class LayerCluster():
    def __init__(self,data_file):
        self.docs = Docs(data_file) 
        self.algo = sim_algorathm()
        
    def run(self):
        self.docs.load()
        clusters = [ Cluster(k,self.docs.doc_vec_dict[k],cid = 1 )  \
                 for k,v in self.docs.tf_dict.items() if k in self.docs.doc_vec_dict ]
        for i in range(len(clusters)) : clusters[i].cid = i

        print "ori_cluster_num:" , len(clusters)
        compute_note = {}
        cid = -1 
        while len(clusters) > 1:
            nearest_pair = (0,1)
            nearest_dis = self.algo.sim_pearson( clusters[0].data, clusters[1].data    )
            for i in range(len(clusters) ):
                for j in range(i+1,len(clusters)):
                    if (clusters[i].cid ,clusters[j].cid ) not in compute_note:
                        compute_note[(clusters[i].cid,clusters[j].cid)] = self.algo.sim_pearson(clusters[i].data,clusters[j].data)
                    dis = compute_note[ (clusters[i].cid, clusters[j].cid )  ] 
                    if dis < nearest_dis:
                        nearest_dis = dis
                        nearest_pair = (i,j)
                #if i % 10 == 0:print i
            vec_data = [ (clusters[nearest_pair[0]].data[index] + clusters[nearest_pair[1]].data[index])/2.0  for index in range(len( clusters[0].data )) ]

            clus = Cluster(None,vec_data,cid = cid,left = clusters[nearest_pair[0]],right = clusters[nearest_pair[1] ] )
            print "%d %d => %d %d" % ( clusters[nearest_pair[0]].cid ,\
                clusters[nearest_pair[1]].cid,cid,len(clusters) -1)
            clusters.append(clus)
            del clusters[nearest_pair[1]]
            del clusters[nearest_pair[0]]
            cid -= 1
            #print cid 
        print len(clusters)
        clusters[0].print_clut(docs=self.docs)           
        #print json.dumps(clusters,ensure_ascii=False)          
        
if __name__ == '__main__': 
    lc = LayerCluster(sys.argv[1])
    lc.run()
