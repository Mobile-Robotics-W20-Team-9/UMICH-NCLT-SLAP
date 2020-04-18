import pickle

# file to print current pickle files to text file
# this allows us to monitor current dictionaries
def printPickle(filename):
    pickle_in = open(filename + '.pkl',"rb")
    currDict = pickle.load(pickle_in)
    f = open(filename + '.txt',"w")
    for x in currDict:
        f.write('%s\n' % x )
    f.close()

# update pickle files to update dictionaries
# example: grades = {'Bart', 'Lisa', 'Milhouse', 'Nelson'}
def createPickle(filename, pklList):
    f = open(filename + '.pkl', 'wb')   # Pickle file is newly created where foo1.py is
    pickle.dump(pklList, f)          # dump data to f
    f.close()

def updatePickle(filename, pklList):
    pickle_in = open(filename + '.pkl',"rb")
    currDict = pickle.load(pickle_in)
    f = open(filename + '.pkl', 'wb')   # Pickle file is newly created where foo1.py is
    pickle.dump(currDict|pklList, f)          # dump data to f
    f.close()

printPickle("classes")
printPickle("words")

# Example usage
#   createPickle('test', {'Bart', 'Lisa', 'Milhouse', 'Nelson'})
#   updatePickle('test', {'Theo'})
#   printPickle("test")
