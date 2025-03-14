import warnings
import numpy as np
import matplotlib.pyplot as plt

def Watt2dBm(x):
	'''
	converts from units of watts to dBm
	'''
	return 10.*np.log10(x*1000.)
	
def dBm2Watt(x):
	'''
	converts from units of watts to dBm
	'''
	return 10**(x/10.) /1000.	

class plotting(object):
	'''
	some helper functions for plotting
	'''
	def plotall(self):
		real = self.z_data_raw.real
		imag = self.z_data_raw.imag
		real2 = self.z_data_sim.real
		imag2 = self.z_data_sim.imag

		fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

		# Labels for enumeration
		labels = ['(a)', '(b)', '(c)']
		positions = [(-0.20, 0.95)] * 3  # Position for top-left corner

		ax[0].plot(real, imag, label='rawdata')
		ax[0].plot(real2, imag2, label='fit')
		ax[0].set_xlabel('Re(S21)')
		ax[0].set_ylabel('Im(S21)')
		ax[0].legend()
		ax[0].set_aspect('equal')  # Make square
		ax[0].text(*positions[0], labels[0], transform=ax[0].transAxes, fontsize=14)

		ax[1].plot(self.f_data * 1e-9, np.absolute(self.z_data_raw), label='rawdata')
		ax[1].plot(self.f_data * 1e-9, np.absolute(self.z_data_sim), label='fit')
		ax[1].set_xlabel('f (GHz)')
		ax[1].set_ylabel('|S21|')
		ax[1].legend()
		ax[1].set_aspect(1.0 / ax[1].get_data_ratio())  # Keep reasonable proportions
		ax[1].text(*positions[1], labels[1], transform=ax[1].transAxes, fontsize=14)

		ax[2].plot(self.f_data * 1e-9, np.angle(self.z_data_raw), label='rawdata')
		ax[2].plot(self.f_data * 1e-9, np.angle(self.z_data_sim), label='fit')
		ax[2].set_xlabel('f (GHz)')
		ax[2].set_ylabel('arg(|S21|)')
		ax[2].legend()
		ax[2].set_aspect(1.0 / ax[2].get_data_ratio())  # Keep reasonable proportions
		ax[2].text(*positions[2], labels[2], transform=ax[2].transAxes, fontsize=14)

		plt.subplots_adjust(wspace=0.25)  # Increase spacing between plots
		plt.show()

	def plotcalibrateddata(self):
		real = self.z_data.real
		imag = self.z_data.imag
		plt.subplot(221)
		plt.plot(real, imag, label='rawdata')
		plt.xlabel('Re(S21)')
		plt.ylabel('Im(S21)')
		plt.legend()
		plt.subplot(222)
		plt.plot(self.f_data*1e-9, np.absolute(self.z_data), label='rawdata')
		plt.xlabel('f (GHz)')
		plt.ylabel('|S21|')
		plt.legend()
		plt.subplot(223)
		plt.plot(self.f_data*1e-9, np.angle(self.z_data), label='rawdata')
		plt.xlabel('f (GHz)')
		plt.ylabel('arg(|S21|)')
		plt.legend()
		plt.show()
		
	def plotrawdata(self):
		real = self.z_data_raw.real
		imag = self.z_data_raw.imag
		plt.subplot(221)
		plt.plot(real,imag,label='rawdata')
		plt.xlabel('Re(S21)')
		plt.ylabel('Im(S21)')
		plt.legend()
		plt.subplot(222)
		plt.plot(self.f_data*1e-9, np.absolute(self.z_data_raw),label='rawdata')
		plt.xlabel('f (GHz)')
		plt.ylabel('|S21|')
		plt.legend()
		plt.subplot(223)
		plt.plot(self.f_data*1e-9,np.angle(self.z_data_raw),label='rawdata')
		plt.xlabel('f (GHz)')
		plt.ylabel('arg(|S21|)')
		plt.legend()
		plt.show()

class save_load(object):
	'''
	procedures for loading and saving data used by other classes
	'''
	def _ConvToCompl(self,x,y,dtype):
		'''
		dtype = 'realimag', 'dBmagphaserad', 'linmagphaserad', 'dBmagphasedeg', 'linmagphasedeg'
		'''
		if dtype=='realimag':
			return x+1j*y
		elif dtype=='linmagphaserad':
			return x*np.exp(1j*y)
		elif dtype=='dBmagphaserad':
			return 10**(x/20.)*np.exp(1j*y)
		elif dtype=='linmagphasedeg':
			return x*np.exp(1j*y/180.*np.pi)
		elif dtype=='dBmagphasedeg':
			return 10**(x/20.)*np.exp(1j*y/180.*np.pi)	 
		else: warnings.warn("Undefined input type! Use 'realimag', 'dBmagphaserad', 'linmagphaserad', 'dBmagphasedeg' or 'linmagphasedeg'.", SyntaxWarning)
	
	def add_data(self,f_data,z_data):
		self.f_data = np.array(f_data)
		self.z_data_raw = np.array(z_data)
		
	def cut_data(self,f1,f2):
		def findpos(f_data,val):
			pos = 0
			for i in range(len(f_data)):
				if f_data[i]<val: pos=i
			return pos
		pos1 = findpos(self.f_data,f1)
		pos2 = findpos(self.f_data,f2)
		self.f_data = self.f_data[pos1:pos2]
		self.z_data_raw = self.z_data_raw[pos1:pos2]
		
	def add_fromtxt(self,fname,dtype,header_rows,usecols=(0,1,2),fdata_unit=1.,delimiter=None):
		'''
		dtype = 'realimag', 'dBmagphaserad', 'linmagphaserad', 'dBmagphasedeg', 'linmagphasedeg'
		'''
		data = np.loadtxt(fname,usecols=usecols,skiprows=header_rows,delimiter=delimiter)
		self.f_data = data[:,0]*fdata_unit
		self.z_data_raw = self._ConvToCompl(data[:,1],data[:,2],dtype=dtype)
		
	def add_fromhdf():
		pass
	
	def add_froms2p(self,fname,y1_col,y2_col,dtype,fdata_unit=1.,delimiter=None):
		'''
		dtype = 'realimag', 'dBmagphaserad', 'linmagphaserad', 'dBmagphasedeg', 'linmagphasedeg'
		'''
		if dtype == 'dBmagphasedeg' or dtype == 'linmagphasedeg':
			phase_conversion = 1./180.*np.pi
		else: 
			phase_conversion = 1.
		f = open(fname)
		lines = f.readlines()
		f.close()
		z_data_raw = []
		f_data = []
		if dtype=='realimag':
			for line in lines:
				if ((line!="\n") and (line[0]!="#") and (line[0]!="!")) :
					lineinfo = line.split(delimiter)
					f_data.append(float(lineinfo[0])*fdata_unit)
					z_data_raw.append(complex(float(lineinfo[y1_col]),float(lineinfo[y2_col])))
		elif dtype=='linmagphaserad' or dtype=='linmagphasedeg':
			for line in lines:
				if ((line!="\n") and (line[0]!="#") and (line[0]!="!") and (line[0]!="M") and (line[0]!="P")):
					lineinfo = line.split(delimiter)
					f_data.append(float(lineinfo[0])*fdata_unit)
					z_data_raw.append(float(lineinfo[y1_col])*np.exp( complex(0.,phase_conversion*float(lineinfo[y2_col]))))
		elif dtype=='dBmagphaserad' or dtype=='dBmagphasedeg':
			for line in lines:
				if ((line!="\n") and (line[0]!="#") and (line[0]!="!") and (line[0]!="M") and (line[0]!="P")):
					lineinfo = line.split(delimiter)
					f_data.append(float(lineinfo[0])*fdata_unit)
					linamp = 10**(float(lineinfo[y1_col])/20.)
					z_data_raw.append(linamp*np.exp( complex(0.,phase_conversion*float(lineinfo[y2_col]))))
		else:
			warnings.warn("Undefined input type! Use 'realimag', 'dBmagphaserad', 'linmagphaserad', 'dBmagphasedeg' or 'linmagphasedeg'.", SyntaxWarning)
		self.f_data = np.array(f_data)
		self.z_data_raw = np.array(z_data_raw)
		
	def save_fitresults(self,fname):
		pass
	


