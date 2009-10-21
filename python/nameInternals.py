#!/usr/bin/python
import sys, re, copy
log=False
for line in sys.stdin.readlines():
    if ';' in line:
        treeString = line.strip()
newTreeString = copy.deepcopy(treeString)

def isUnique(list):
    for item in list:
        if list.count(item) >=2:
            return False
    return True

def makeUnique(list):
    out = []
    for item in list:
        if not item in out:
            out.append(item)
    return out

def isSubset(small, big):
    for item in small:
        if not item in big:
            return False
    return True

try:
    grouping = int(sys.argv[1])
except:
    sys.stderr.write('Grouping assumed to be filename list.\n')
    grouping = sys.argv[1:]
if type(grouping)==int:
    lengths = []
    ranges = []
    toReplace = []
    lengthMatch = re.finditer('\)(:\s*([0-9]+\.[0-9]+))',treeString)
    for i in lengthMatch:
        if i.group(1).count('(') == i.group(1).count(')'):
            lengths.append(float(i.group(2)))
            toReplace.append(i.group(1))
            ranges.append( i.span() )
    ordLengths =  [i for i in reversed(sorted(lengths))]
    ordRanges = copy.deepcopy(ranges)
    ordRanges.sort(key=lambda x: lengths[ranges.index(x)], reverse=True)
    ordToReplace = copy.deepcopy(toReplace)
    ordToReplace.sort(key=lambda x: lengths[toReplace.index(x)], reverse=True)
    for i,repString in enumerate(ordToReplace[:grouping]):
        newTreeString = newTreeString.replace(repString,'Node_'+str(i)+repString)
        if log:
            print 'replaced:', repString,'with: Node_'+str(i)+repString
    print newTreeString     

if type(grouping) == list:
    # a list of filenames is assumed
    groups = []
    groupNames = []
    for filename in grouping:
        groups.append([i.strip() for i in open(filename).readlines()])
        groupNames.append(filename.split('/')[-1].replace('.group',''))
    if log:
        'print groups read as:', groups
    clades = []
    for start in range(len(treeString)):
        if not treeString[start] == '(':
            continue
        end = start+1
        while 1:
            match = treeString[start:end]
            if match.count('(') == match.count(')'):
                clades.append(match)
                break
            else:
                end += 1
    clades = makeUnique(clades)


    cladeDict = {}
    for clade in clades:
        replaceRE = re.compile('[\)\(]')
        splitRE = re.compile('[,:]')
        species = [ i for i in splitRE.split(replaceRE.sub('',clade)) if not re.match('[0-9]+\.[0-9]+', i)]
        cladeDict[clade] = species
        if log:
            print 'species for clade string:', clade, ':    ', species
    if log:
        print '----------- matching groups to clade ----------'
    for index, group in enumerate(groups):
        if log:
            print 'Finding clade for group:', group
        minLength = None
        for clade in cladeDict.keys():
            if isSubset(group, cladeDict[clade]):
                if log:
                    print 'Candidate clade w/species:', cladeDict[clade]
                if minLength:
                    if len(cladeDict[clade]) < minLength:
                        minLength = len(cladeDict[clade])
                        smallestClade = clade
                else:
                    minLength = len(cladeDict[clade])
                    smallestClade = clade
        if log:
            print 'smallest clade for ', group,':    ', smallestClade
            print 'replacing ', smallestClade, ' with ', smallestClade+'NODE_'+str(index)
        treeString = treeString.replace(smallestClade, smallestClade+groupNames[index])
    print treeString.replace(';','root;')
