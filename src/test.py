from tabulate import tabulate
from common.AtlasSet import AtlasSet

from common.Queryer import Queryer
atlas_set = AtlasSet('./src/data', lang = 'ZH-Hans')
queryer = Queryer(atlas_set)
a = queryer.query(
    [{'a':1,'b':2,'c':3,'coord':(1,2,3)},{'a':1,'b':2,'c':3,'coord':(7,8,9)},{'a':1,'b':2,'c':3,'coord':(41,32,50)}], 
    10, no_coord = False)

print(tabulate(a, headers="keys"))