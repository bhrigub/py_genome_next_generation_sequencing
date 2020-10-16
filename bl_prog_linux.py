###############################################################################
# Variables:
# loci_data: Data from loci file
# self.reads_data: Data from reads file
# count: Temporary variable used to check sanity data with user understanding
# read_data_len: Length of reads data
# loci_data_len: Length of loci data
# loci_data_values: Count of loci in reads data
# ##############################################################################
import unittest
loci_data_values_global=[]
class FindLociReadsMatch:
    def __init__(self,location_reads,location_loci):
        self.read_data_len=0
        self.loci_data_len=0
        self.reads_data=""
        self.loci_data=""
        self.reads_hash_map=dict()
        self.loci_data_values=[]
        self.location_reads=location_reads
        self.location_loci=location_loci
        
    #################################################
    ########### Load data from reads/loci ###########
    #################################################

    def load_data(self):
        #print(self.location_reads,self.location_loci)
        try:
            loci_file=open(self.location_loci,"r")
            self.loci_data=loci_file.read()  
            loci_file.close()    
            self.loci_data=self.loci_data.replace(',','')    
            self.loci_data=self.loci_data.splitlines()
            self.loci_data=(self.loci_data[1:])
            self.loci_data_len=len(self.loci_data)
            self.loci_data=[int(self.loci_data[j]) for j in range (self.loci_data_len)]
            #print(loci_data[:20])
            reads_file=open(self.location_reads,"r")
            self.reads_data=reads_file.read()  
            reads_file.close() 
            self.reads_data=self.reads_data.splitlines()
            self.reads_data=[self.reads_data[i].split(',') for i in range (len(self.reads_data))]
            self.reads_data=(self.reads_data[1:])
            self.read_data_len=len(self.reads_data)
            self.reads_data=[[int(self.reads_data[j][i]) for i in range (2)] for j in range (self.read_data_len)]    

        except FileNotFoundError:
            print("Error: Loci/Reads File Not Found")
        except Exception as e: 
            print(e)
        finally:
            print("Loci and Data File Operation Completed \n")

    ###################################
    ##### Add elements to Hashmap #####
    ################################### 

    def add_ele_to_hashmap(self, val, i):
        #Add values to dictionary with counter from start of data point till end
        for j in range(self.reads_data[i][0],self.reads_data[i][0]+self.reads_data[i][1],1):
            #Check if value exists in dictionary
            if not self.reads_hash_map[val].get(j):
                self.reads_hash_map[val][j]=1
            else:
                #Increase count of existing value
                self.reads_hash_map[val][j]+=1

    ##############################
    ##### Preprocessing data #####
    ############################## 

    def preprocessing_data(self):
        print("Starting preprocessing...")
        #Initialize reads Hash Map
        for digits_len in range (10):
            self.reads_hash_map[digits_len]={}

        try:
            for i in range (self.read_data_len):
                #Compare reads string length and add to appropriate key hashmap
                read_data_length=len(str(self.reads_data[i][0]))
                self.add_ele_to_hashmap(read_data_length,i)                      
        except Exception as e: 
            print(e)
        finally:
            #print(self.reads_hash_map[5])
            print("Data preprocessing completed.\n") 

    ##############################
    ###### Assign loci data ######
    ############################## 
     
    def assign_value_loci (self, val, i):
        if self.reads_hash_map[val].get(self.loci_data[i]):
            self.loci_data_values[i]=self.reads_hash_map[val][self.loci_data[i]]
        else:
            self.loci_data_values[i]=0

    ##############################
    ###### Search loci data ######
    ############################## 

    def search_loci_reads (self):        
        try:
            self.loci_data_values=[0 for k in range (self.loci_data_len)]       
            print("Value search started...")
            for i in range (self.loci_data_len):
                loci_data_length=len(str(self.loci_data[i]))
                #Check if value exists in hash map else assign value 0
                self.assign_value_loci(loci_data_length,i)
                                        
        except Exception as e: 
            print(e)
        finally: 
            #print(self.loci_data_values[:200])
            loci_data_values_global[:]=self.loci_data_values[:]
            #print(loci_data_values_global[:50])
            print("Value search completed.\n")     

    ##################################
    ###### Write loci file data ######
    ##################################    

    def file_write_loci(self):
        try: 
            #loci_file=open(self.location_loci,"w")
            loci_file=open("./lociOP.csv","w")#open("B:\Work\Interviews\Boston Lighthouse\lociOP.csv","w")
            
            loci_file.write("position, coverage \n")
            for i in range(self.loci_data_len):
                loci_file.write(str(self.loci_data[i])+", "+str(self.loci_data_values[i])+" \n")
            loci_file.close()
        except Exception as e: 
            print(e)
        finally:
            print("Loci file updated.\n")

#######################################
###### UnitTest loci file output ######
####################################### 
class UnittestLociValues(unittest.TestCase): 
    def __init__(self):        
        self.sanity_check_arr=[1190, 12206, 141295, 6809, 6993, 1096, 62732, 43740, 78510, 42854, 62, 221, 24560, 1, 2581, 84, 6209, 36, 431 ,213040]
        #self.search_loci=FindLociReadsMatch("B:\Work\Interviews\Boston Lighthouse\\reads.csv","B:\Work\Interviews\Boston Lighthouse\loci.csv")
        self.search_loci=FindLociReadsMatch("./reads.csv","./loci.csv")
        self.search_loci.load_data()
        self.search_loci.preprocessing_data()
        self.search_loci.search_loci_reads()  
        self.search_loci.file_write_loci() 

    def runtest_loci_values(self):
        try:
            result=[True if (loci_data_values_global[i]==self.sanity_check_arr[i]) else False for i in range(len(self.sanity_check_arr))]
            #for i in range(range(len(self.sanity_check_arr)):
            #   self.assertEqual(loci_data_values_global[i],self.sanity_check_arr[i])
        except Exception as e:
            print(e)
        finally:
            true_val=0
            false_val=0
            for i in range (len(result)):
                if result[i]==True:
                    true_val+=1
                else:
                    false_val+=1   
            print("Unittest results:")  
            print("Valid case count %d \n" % true_val,"Invalid case count %d" % false_val)
    
###########################
###### Main function ######
########################### 

if __name__ == "__main__":    
    unittest_output=UnittestLociValues()
    unittest_output.runtest_loci_values()
    #print(loci_data_values_global)
    pass