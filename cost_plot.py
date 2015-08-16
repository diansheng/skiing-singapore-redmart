import matplotlib.pyplot as plt
import numpy as np
import math

x=np.array([ 10,  20,  40, 100, 200])
y=np.array([  0.407,   0.481,   0.779,   3.511,  22.525])

logy=np.log10(y)

plt.figure(1)
plt.suptitle('computational cost vs size of data')
plt.subplot(121)
plt.title('log10(y) against log10(x)')
plt.plot(np.log10(x),logy,'ro')
plt.plot(np.log10(x),logy,'b')

plt.subplot(122)
plt.title('log10(y) against x')
plt.plot(x,logy,'ro')
plt.plot(x,logy)
plt.draw()

from scipy import stats
slope, intercept, r_value, p_value, std_err = stats.linregress(x,logy)
a=10**slope
b=10**intercept
print std_err

print "computation cost in secs = %f x %f ^ length of column of the data matrix" % (b,a)
print "estimated cost for 1000x1000 data matrix= %fsecs" % (b*a**1000)

plt.show()