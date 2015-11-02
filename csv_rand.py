# 
# 
import pandas as pd 
import glob 
import random
import numpy as np
import progressbar

def samp_csv(fil,n,s,nsz=1000000): 
	# nchunks
	nch = n/nsz
	# subsample per chunk
	ss = s / nch
	odf = pd.DataFrame()
	srow = 0
	print(nch)
	bar = progressbar.ProgressBar()
	
	for i in bar(range(nch)):
		dat = pd.read_csv(fil,skiprows=srow,nrows=nsz,header=0)
		if i ==0: 
			dat.columns = [str.strip(ii) for ii in dat.keys()]
			coln = dat.columns
		dat.columns = coln
		srow += nsz
		odat=dat.sample(ss)
		odf=odf.append(odat)

	return odf

if 0:
	# get file lengths from get_csvlen.txt
	clen = pd.read_csv('./data/get_csvlen.txt',sep=' ',usecols=[2,5])

	fils = glob.glob('./data/*2014*csv')
	ii =0
	fil = fils[ii]
	#fil='./data/yellow_tst2.csv'
	oo='./data/'+clen.filenames==fils[1]
	n = clen.lines[oo].values[0]
	n=100000
	s = 9000 #desired sample size
	#skip = sorted(random.sample(xrange(n),n-s))
	lskip = np.random.choice(np.arange(1,n+1), (n-s), replace=False)
	df = pd.read_csv(fil,skiprows=lskip)

clen = pd.read_csv('./data/get_csvlen.txt',sep=' ',usecols=[2,5])
fils = glob.glob('./data/*2014*csv')

if 0:
	fil=fils[0]
	oo='./data/'+clen.filenames==fils[1]
	n = clen.lines[oo].values[0]
	odf=samp_csv(fil,n,1000000,nsz=500000)
	odf.to_pickle(fils[0]+'.samp1M.pk')

if 1: 
	for fil in fils[1:]:
		print(fil)
		oo='./data/'+clen.filenames==fil
		n = clen.lines[oo].values[0]
		odf=samp_csv(fil,n,1000000,nsz=500000)
		odf.to_pickle(fil+'.samp1M.pk')