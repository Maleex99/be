# -*- coding: utf-8 -*-

from mgd import t03_MGD as MGD
from mgi import MGI
import numpy as np
import util as u

t34 = u.get_t34()
m = 2

print(np.dot( np.round( MGD(MGI((0.5, 0.5, 3), m, t34, 1, 1),m), 2), t34))