import pandas as pd 
import glob 
import random
import numpy as np
import progressbar
import fiona 
import shapely
from shapely.geometry import Point, shape
import seaborn as sns 

def replace_neigh(dfi,n1,n2):
    dfi.loc[dfi.pickup_neigh==n1,'pickup_neigh']=n2
    dfi.loc[dfi.dropoff_neigh==n1,'dropoff_neigh']=n2
    return dfi

def remove_neigh(dfi,neigh):
    dfi=dfi[dfi.pickup_neigh != neigh]
    dfi=dfi[dfi.dropoff_neigh != neigh]
    return dfi 

def plotHeatPickDrop(dat,tit='', nrm=1):
	grp_pckneigh = dat.groupby('pickup_neigh')
	grps = grp_pckneigh.groups
	nns = np.sort(grps.keys())
	opd = pd.DataFrame()
	opd.columns.name = 'Pickup Neighborhood'+tit
	opd.index.name = 'Dropoff Neighborhood'
	#opd.set_index(nns)
	for name, grp in grp_pckneigh:
		#cnts = [grp['dropoff_neigh'].count(nm) for nm in nns]
		dnms = list(grp['dropoff_neigh'])
		cnts = [dnms.count(nm) for nm in nns]
		opd[name]=cnts
	opd.index=nns
	opd.index.name='Dropoff Neighborhood'      
	sns.set_context("poster")
	opd=opd/nrm
	sns.heatmap(opd, linewidths=0.1) 
	return opd	

def plotHeatPickDrop(dat,tit='', nrm=1):
	grp_pckneigh = dat.groupby('pickup_neigh')
	grps = grp_pckneigh.groups
	nns = np.sort(grps.keys())
	opd = pd.DataFrame()
	opd.columns.name = 'Pickup Neighborhood'+tit
	opd.index.name = 'Dropoff Neighborhood'
	#opd.set_index(nns)
	for name, grp in grp_pckneigh:
		#cnts = [grp['dropoff_neigh'].count(nm) for nm in nns]
		dnms = list(grp['dropoff_neigh'])
		cnts = [dnms.count(nm) for nm in nns]
		opd[name]=cnts
	opd.index=nns
	opd.index.name='Dropoff Neighborhood'      
	sns.set_context("poster")
	opd=opd/nrm
	sns.heatmap(opd, cmap="YlGnBu", linewidths=0.1) 
	return opd	

def dow_counter(dat):
	dows=np.unique(dat.dow)
	ol = [len(np.unique(dat[dat.dow==dw]['day'])) for dw in dows]
	return ol

def dfilts(filn, dowmax=5, dowmin=0, hourmax=22, hourmin=6):
	dat = pd.read_pickle(filn)
	dat = dat[(dat.dow <= dowmax) & (dat.dow >= dowmin)].copy()
	dat= dat[(dat.hour >= hourmin) & (dat.hour <= hourmax)]

	dat=remove_neigh(dat, 'Inwood')
	dat=remove_neigh(dat, "Randall's Island")
	dat=remove_neigh(dat, 'Roosevelt Island')
	dat=remove_neigh(dat, 'Marble Hill')
	dat=remove_neigh(dat, 'None')
	dat=remove_neigh(dat, 'Washington Heights')

	dat = replace_neigh(dat,'Battery Park City', 'Financial District')
	dat = replace_neigh(dat, 'Nolita', 'SoHo')
	dat = replace_neigh(dat, 'Little Italy','Chinatown')
	dat = replace_neigh(dat, 'Two Bridges','Chinatown')
	dat = replace_neigh(dat, 'Civic Center','Chinatown')

	dat = replace_neigh(dat, 'Stuyvesant Town','Gramercy')
	dat = replace_neigh(dat, 'Flatiron District','Gramercy')
	dat = replace_neigh(dat, 'Kips Bay','Gramercy')
	dat = replace_neigh(dat, 'Murray Hill','Gramercy')

	dat = replace_neigh(dat, 'Theater District',"Hell's Kitchen")
	dat = replace_neigh(dat, 'NoHo','East Village')
	dat = replace_neigh(dat, 'West Village','Greenwich Village')
	
	dat = replace_neigh(dat, 'Morningside Heights','Harlem')
	dat = replace_neigh(dat, 'SoHo','Tribeca-SoHo')
	dat = replace_neigh(dat, 'Tribeca','Tribeca-SoHo')

	return dat
