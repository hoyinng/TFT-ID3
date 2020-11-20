import sys
import six
#`from sklearn.externals import six` is deprecated 
sys.modules['sklearn.externals.six'] = six
from id3 import Id3Estimator, export_graphviz
import numpy as np
from os import path
from io import StringIO

trainning_data_col_lower = 1
trainning_data_col_upper = 26
leaf_type = int
leaf_col = 29

attributes = ["Player Name", "Galaxy","Blaster","Rebel","ManaReaver","Demolitionist","Cybernetic","Infiltrator","StarGuardian","Paragon","Sniper","Set3_Celestial","MechPilot",
"Set3_Sorcerer","Astro","Chrono","Battlecast","Set3_Brawler","SpacePirate","DarkStar","Vanguard","Starship","Mercenary","Protector","Set3_Mystic","Set3_Blademaster","DamageToPlayer",
"Top4","Win","Placement"]

TESTCASE_DATASET = path.realpath(path.join(path.realpath(__file__), '..','data','CSV','predict.csv'))
RESULT_DATASET = path.realpath(path.join(path.realpath(__file__),'..','data','CSV','result.csv'))

TRAINNING_DATASET_FILE_LOCATION = path.realpath(path.join(path.realpath(__file__),'..','data','CSV','tftmatchdata.csv'))
UNIQUECASES_FILE_LOCATION = path.realpath(path.join(path.realpath(__file__),'..','data','CSV','uniquecases.csv'))

bX = np.genfromtxt(UNIQUECASES_FILE_LOCATION,delimiter=",",skip_header=1,dtype=str,usecols=(tuple(range(trainning_data_col_lower,trainning_data_col_upper))))
bY = np.genfromtxt(UNIQUECASES_FILE_LOCATION,delimiter=",",skip_header=1,dtype=leaf_type,usecols=leaf_col)

X = np.genfromtxt(TRAINNING_DATASET_FILE_LOCATION,delimiter=",",skip_header=1,dtype=str,usecols=(tuple(range(trainning_data_col_lower,trainning_data_col_upper))))
Y = np.genfromtxt(TRAINNING_DATASET_FILE_LOCATION,delimiter=",",skip_header=1,dtype=leaf_type,usecols=leaf_col)

# Merge
X = np.vstack([X,bX])
Y = np.concatenate([bY,Y])

clf = Id3Estimator(min_samples_split=4,prune=False,is_repeating=False,gain_ratio=False)
clf.fit(X,Y,check_input=True)

J = np.genfromtxt(TESTCASE_DATASET,delimiter=",",skip_header=1,dtype=str,usecols=(tuple(range(1,trainning_data_col_upper))))

K = clf.predict(J)
predict_table = np.genfromtxt(TESTCASE_DATASET,delimiter=",",dtype=str)
left, right = np.hsplit(predict_table,[leaf_col])
right = np.hsplit(right,[1])[1] # without the predicted column

K = np.hstack([("Predicted" + attributes[leaf_col]),K]).reshape(-1,1)
I = np.hstack((left,K,right))

print ("Writing result (.csv) in {}".format(RESULT_DATASET))
np.savetxt(RESULT_DATASET,I,delimiter=",",fmt="%s")

output = path.realpath(path.join(path.realpath(__file__),'..','out.dot'))
print ("Writing dt in %s" %(output))
export_graphviz(clf.tree_, output, attributes[trainning_data_col_lower:trainning_data_col_upper])
