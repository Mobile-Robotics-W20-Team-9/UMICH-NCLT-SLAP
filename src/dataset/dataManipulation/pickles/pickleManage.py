import pickle

# Usage: file to print current pickle files to text file
#           this allows us to monitor current dictionaries
# Example: printPickle("BuildingMappings")
# Output: Text file of dictonary keys
def printPickle(filename):
    pickle_in = open(filename + '.pkl',"rb")
    currDict = pickle.load(pickle_in)
    f = open(filename + '.txt',"w")
    for x in currDict:
        f.write('%s\n' % x )
    f.close()

# Usage: creates pickle files from given dictionaries
# Example: createPickle('test', {'Bart', 'Lisa', 'Milhouse', 'Nelson'})
# Output: new Pickle file
def createPickle(filename, pklList):
    f = open(filename + '.pkl', 'wb')   # Pickle file is newly created where foo1.py is
    pickle.dump(pklList, f)          # dump data to f
    f.close()

# Usage: updates pickle files from given dictionaries
# Example: updatePickle('test', {'Bart', 'Lisa', 'Milhouse', 'Nelson'})
# Output: Pickle file
def updatePickle(filename, pklList):
    pickle_in = open(filename + '.pkl',"rb")
    currDict = pickle.load(pickle_in)
    f = open(filename + '.pkl', 'wb')   # Pickle file is newly created where foo1.py is
    pickle.dump(currDict + pklList, f)          # dump data to f
    f.close()

