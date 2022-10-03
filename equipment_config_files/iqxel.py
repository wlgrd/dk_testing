#-------------------------------------------------------------------------------
# Name:		   iqxel
# Purpose:	   This module has all the APIs(SCPI commands) for configurint Litepoint iQxel-160/280 VSG/VSA.
# Author:	   kranthi.kishore
# Created:	   14-06-2015
# Copyright:   Imagination Technologies Ltd
#-------------------------------------------------------------------------------
from   socket import *
import time
from commonUtils import *
from input_conf import *

datarate_dict={
				'11a':{'6':'MCS 0','9':'MCS 1','12':'MCS 2','18':'MCS 3','24':'MCS 4','36':'MCS 5','48':'MCS 6','54':'MCS 7'},	
				'11n':{'MCS0':'MCS 0','MCS1':'MCS 1','MCS2':'MCS 2','MCS3':'MCS 3','MCS4':'MCS 4','MCS5':'MCS 5','MCS6':'MCS 6','MCS7':'MCS 7',
						'MCS8':'MCS 8','MCS9':'MCS 9','MCS10':'MCS 10','MCS11':'MCS 11','MCS12':'MCS 12','MCS13':'MCS 13','MCS14':'MCS 14','MCS15':'MCS 15'},
				'11g':{'6':'MCS 0','9':'MCS 1','12':'MCS 2','18':'MCS 3','24':'MCS 4','36':'MCS 5','48':'MCS 6','54':'MCS 7'},	
				'11b':{'1':'DRAT RATE1','2':'DRAT RATE2','5.5':'DRAT RATE5_5','11':'DRAT RATE11'},	
				'11ac':{'MCS0':'MCS 0','MCS1':'MCS 1','MCS2':'MCS 2','MCS3':'MCS 3','MCS4':'MCS 4','MCS5':'MCS 5','MCS6':'MCS 6','MCS7':'MCS 7',
						'MCS8':'MCS 8','MCS9':'MCS 9','MCS10':'MCS 10','MCS11':'MCS 11','MCS12':'MCS 12','MCS13':'MCS 13','MCS14':'MCS 14','MCS15':'MCS 15'}
				}
class IQXEL:
	def __init__(self,tester='iqxel_280'):
		self.tester=tester.split('_')[-1]
		self.hostName = tester_hostname
		self.port = 24000
#Start VSG	
	def start_vsg(self):
		print "\nConfiguring ",self.tester	
		debugPrint("\nConfiguring "+self.tester)
		global cntrl_sckt
		ADDR = (self.hostName,self.port)
		cntrl_sckt = socket(AF_INET, SOCK_STREAM)	# Create and
		cntrl_sckt.connect(ADDR) 
		time.sleep(1)

	#Close VSG
	def close_vsg(self):
		debugPrint('Closing VSG')
		cntrl_sckt.close()
		time.sleep(1)

	#802.11a Initialization settings
	def config_11a(self):
		cntrl_sckt.sendall('CHAN1;WIFI;CONF:WAVE:STAN A\n')
	
	#802.11b Initialization settings
	def config_11b(self):
		cntrl_sckt.sendall('CHAN1;WIFI;CONF:WAVE:STAN B\n')
	
	#802.11g Initialization settings
	def config_11g(self):
		cntrl_sckt.sendall('CHAN1;WIFI;CONF:WAVE:STAN A\n')
	
	#802.11n Initialization settings
	def config_11n(self):
		cntrl_sckt.sendall('CHAN1;WIFI;CONF:WAVE:STAN N\n')
	
	#802.11ac Initialization settings
	def config_11ac(self):
		cntrl_sckt.sendall('CHAN1;WIFI;CONF:WAVE:STAN AC\n')
	
	#Set Default
	def set_equip_default(self):
		print "\nSetting VSA to default"
		debugPrint("\nSetting VSA to default")
		cntrl_sckt.sendall('*RST\n')
		if(self.tester.lower()=='280'):
			cntrl_sckt.sendall('MROUT1;PORT:RES RF1A,OFF\n')
			cntrl_sckt.sendall('MROUT2;PORT:RES RF2A,OFF\n')
			cntrl_sckt.sendall('SYS;MVSA:DEL\n')
			cntrl_sckt.sendall('SYS;MVSG:DEL\n')
			cntrl_sckt.sendall('SYS;MROUT:DEL\n')
		elif(self.tester.lower()=='160'):
			cntrl_sckt.sendall('*RST\n')
			cntrl_sckt.sendall('MROUT1;PORT:RES RF1A,OFF\n')
			cntrl_sckt.sendall('MROUT2;PORT:RES RF2A,OFF\n')
			cntrl_sckt.sendall('SYS;MVSA:DEL\n')
			cntrl_sckt.sendall('SYS;MVSG:DEL\n')
			cntrl_sckt.sendall('SYS;MROUT:DEL\n')
		time.sleep(1)
	
	#Modulation Type
	def set_modulation(self,standard):
		print "\nSetting "+standard+" in VSA"
		debugPrint("\nSetting "+standard+" in VSA")
		eval('self.config_'+standard+'()')

		
	#Setting Datarate
	def set_datarate(self,modulation,standard,data_rate):
		print "\nSetting data rate ",data_rate
		debugPrint("\nSetting data rate "+data_rate)
		cntrl_sckt.sendall('CHAN1;WIFI;CONF:WAVE:'+modulation+':'+datarate_dict[standard][data_rate]+'\n')

	#Setting Payload
	def set_payload(self,standard,payload):
		print "\nSetting payload ",payload
		debugPrint("\nSetting payload "+str(payload))
		cntrl_sckt.sendall('CHAN1;WIFI;CONF:WAVE:PSDU:NBYT '+payload+'\n')

	#Setting MAC Header OFF
	def set_macheader(self):
		cntrl_sckt.sendall('CHAN1;WIFI;CONF:WAVE:PSDU:MACH OFF\n')

	#Setting Channel
	def apply_vsg(self,bw='',chn='',streams='2x2'):
		debugPrint('Applying VSG channel '+str(chn)+' and BW '+str(bw))
		if(bw=='20') or (bw=='20in40') or (bw=='20in80'):
			cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:IND1 '+str(chn)+'\n')
			cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:CBW 20000000\n')#20MHz
		elif(bw=='40'):
			if str(chn) in prime_20_sec_20_flags_dict[bw].keys():
				cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:IND1 '+str(chn)+'\n')#For Plus
			else:	
				cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:IND1 '+str(int(chn)-4)+'\n')#For Minus
			cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:CBW 40000000\n')#40MHz
		elif(bw=='80'):
			if(prime_20_sec_20_flags_dict[bw][str(chn)]=='l'):	
				cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:IND1 '+str(int(chn)-6)+'\n')#For Minus
			elif(prime_20_sec_20_flags_dict[bw][str(chn)]=='lr'):
				cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:IND1 '+str(int(chn)+2)+'\n')		
			elif(prime_20_sec_20_flags_dict[bw][str(chn)]=='rl'):
				cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:IND1 '+str(int(chn)-2)+'\n')		
			elif(prime_20_sec_20_flags_dict[bw][str(chn)]=='r'):
				cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:IND1 '+str(int(chn)+6)+'\n')#For Plus
			cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:CBW 80000000\n')#80MHz
		if(int(chn)<20):
			cntrl_sckt.sendall('CHAN1;WIFI;CONF:BAND 2G4\n')
		else:
			cntrl_sckt.sendall('CHAN1;WIFI;CONF:BAND 5G\n')
		if(streams=='1x1'):
			cntrl_sckt.sendall('CHAN1;WIFI; HSET:ALL VSG1'+chain_sel_scpi_cmd+'\n')
		elif(streams=='2x2'):
			cntrl_sckt.sendall('CHAN1;WIFI; HSET:ALL MVSGALL\n')
	
	#Setting Amplitude	
	def set_amplitude(self,streams,ampl):
		# print "\nSetting amplitude ",ampl
		debugPrint("\nSetting amplitude "+str(ampl))
		if(streams=='1x1'):
			cntrl_sckt.sendall("VSG1"+chain_sel_scpi_cmd+";POW "+ampl+"\n")
		elif(streams=='2x2'):
			cntrl_sckt.sendall("MVSGALL;POW "+ampl+"\n")
	
	#Set Bandwidth 20/40 MHz
	def set_bandwidth(self,standard='',bw=''):
		debugPrint('Setting BW '+str(bw))
		if(bw=='20') or (bw=='20in40') or (bw=='20in80'):
			cntrl_sckt.sendall('CHAN1;WIFI;CONF:WAVE:OFDM:CBW 20000000\n')#20MHz
		elif(bw=='40'):
			cntrl_sckt.sendall('CHAN1;WIFI;CONF:WAVE:OFDM:CBW 40000000\n')#40MHz
		elif(bw=='80'):
			cntrl_sckt.sendall('CHAN1;WIFI;CONF:WAVE:OFDM:CBW 80000000\n')#80MHz
	
	#Setting Wavegap/Idle Interval
	def set_idleinterval(self,intv):
		print "\nSetting interval ",intv
		debugPrint("\nSetting interval "+str(intv))
		cntrl_sckt.sendall('CHAN1;WIFI;CONF:WAVE:GAP '+str(float(intv)/1000000)+'\n')
	
			
	#Set Spatial Streams
	def set_streams(self,standard,streams):
		print "\nSetting streams ",streams
		debugPrint("\nSetting streams "+streams)
		if(streams=='1x1'):
			cntrl_sckt.sendall("CHAN1;WIFI;CONF:WAVE:OFDM:NSST 1\n")#1x1		
		elif(streams=='2x2'):
			if(standard=='11ac'):
				cntrl_sckt.sendall("CHAN1;WIFI;CONF:WAVE:OFDM:NSST 2\n")#2x2

	#Set Guard Interval
	def set_guardinterval(self,gi):
		print "\nSetting Guard Interval ",gi
		debugPrint("\nSetting Guard Interval "+gi)
		if(gi.lower()=='sgi'):
			cntrl_sckt.sendall("CHAN1;WIFI;CONF:WAVE:OFDM:SGI ON\n")#SGI
		elif(gi.lower()=='lgi'):
			cntrl_sckt.sendall("CHAN1;WIFI;CONF:WAVE:OFDM:SGI OFF\n")#LGI

	#Set STBC
	def set_stbc(self,stbc):
		print "\nSetting STBC ",stbc
		debugPrint("\nSetting STBC "+stbc)
		cntrl_sckt.sendall("CHAN1;WIFI;CONF:WAVE:OFDM:STBC "+str(stbc)[-1]+"\n")

	#Set Coding Type
	def set_coding(self,coding):
		print "\nSetting Coding Technique ",coding
		debugPrint("\nSetting Coding Technique "+coding)
		if(coding.lower()=='ldpc'):
			cntrl_sckt.sendall("CHAN1;WIFI;CONF:WAVE:OFDM:COD LDPC\n")#LDPC
		elif(coding.lower()=='bcc'):
			cntrl_sckt.sendall("CHAN1;WIFI;CONF:WAVE:OFDM:COD BCC\n")#BCC

	#Set Greenfield Mode
	def set_greenfield(self,greenfield_mode):
		print "\nSetting Greenfield Mode ",greenfield_mode
		debugPrint("\nSetting Greenfield Mode "+greenfield_mode)
		if(greenfield_mode.lower()=='greenfield'):
			cntrl_sckt.sendall("CHAN1;WIFI;CONF:WAVE:OFDM:GRE ON\n")#Greenfield
		elif(greenfield_mode.lower()=='mixed'):
			cntrl_sckt.sendall("CHAN1;WIFI;CONF:WAVE:OFDM:GRE OFF\n")#Mixed
	
	#Set Preamble
	def set_preamble(self,preamble):
		print "\nSetting preamble ",preamble
		debugPrint("\nSetting preamble "+preamble)
		if(preamble.lower=='short'):
			cntrl_sckt.sendall("CHAN1;WIFI;CONF:WAVE:DSSS:PRE SHORT\n")#Short
		elif(preamble.lower=='long'):
			cntrl_sckt.sendall("CHAN1;WIFI;CONF:WAVE:DSSS:PRE LONG\n")#Long
	
	#RF ON/OFF
	def rf_on_off(self,rf_state='on',streams='2x2'):
		# print "\nSetting RF ",rf_state
		debugPrint("\nSetting RF "+rf_state)
		if(rf_state=='off'):
			if(streams=='1x1'):
				cntrl_sckt.sendall("VSG1"+chain_sel_scpi_cmd+";POW:STAT"+" "+"OFF\n")			
			elif(streams=='2x2'):
				cntrl_sckt.sendall("MVSGALL;POW:STAT"+" "+"OFF\n")
		elif(rf_state=='on'):
			if(streams=='1x1'):
				cntrl_sckt.sendall("VSG1"+chain_sel_scpi_cmd+";POW:STAT"+" "+"ON\n")			
			elif(streams=='2x2'):
				cntrl_sckt.sendall("MVSGALL;POW:STAT"+" "+"ON\n")

	#Generate Waveform
	def generate_waveform(self,streams='2x2',count='2000'):
		print "\nGenerating waveform "
		debugPrint("\nGenerating waveform ")
		# cntrl_sckt.sendall("CHAN1;WIFI\n")
		# cntrl_sckt.sendall('wave:gen:mmem "\//user/wf.iqvsg", "WIFI wave generation from GUI"\n')
		#return
		if(streams=='1x1'):
			#cntrl_sckt.sendall('*wai;VSG1 ;wave:load "\//user/wf.iqvsg";wave:exec on\n')
			cntrl_sckt.sendall('VSG1'+chain_sel_scpi_cmd+';WLIS:COUN '+count+'\n')
			#cntrl_sckt.sendall('VSG1 ;wave:exec off;WLIST:WSEG1:DATA "\//user/wf.iqvsg";wlist:wseg1:save;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1\n')
		elif(streams=='2x2'):
			#
			cntrl_sckt.sendall('MVSGALL;WLIS:COUN '+count+'\n')
			#cntrl_sckt.sendall('MVSGALL ;wave:exec off;WLIST:WSEG1:DATA "\//user/wf.iqvsg";wlist:wseg1:save;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1\n')

	#Start Pumping	
	def send_packets(self,streams='2x2',action='run',wave_type='default'):
		# print 'Start Pumping'
		debugPrint('Start Pumping')
		self.rf_on_off(rf_state='on',streams=streams)
		if(wave_type=='default'):
			cntrl_sckt.sendall("CHAN1;WIFI\n")
			# cntrl_sckt.sendall('wave:gen:mmem "\//user/wf.iqvsg", "WIFI wave generation from GUI"\n')	
			cntrl_sckt.sendall('wave:gen:mmem "/user/wf.iqvsg", "WIFI wave generation from GUI"\n')	
			if(action=='run'):
				if(streams=='1x1'):
					cntrl_sckt.sendall('VSG1'+chain_sel_scpi_cmd+';WLIS:COUN '+str(num_of_pkts_from_vsg)+'\n')
					cntrl_sckt.sendall('*wai;VSG1'+chain_sel_scpi_cmd+' ;wave:load "/user/wf.iqvsg";wave:exec on\n')
					# cntrl_sckt.sendall('*wai;VSG1'+chain_sel_scpi_cmd+' ;wave:load "\//user/wf.iqvsg";wave:exec on\n')
					cntrl_sckt.sendall('VSG1'+chain_sel_scpi_cmd+' ;wave:exec off;WLIST:WSEG1:DATA "/user/wf.iqvsg";wlist:wseg1:save;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1\n')
				elif(streams=='2x2'):
					cntrl_sckt.sendall('MVSGALL;WLIS:COUN '+str(num_of_pkts_from_vsg)+'\n')
					cntrl_sckt.sendall('*wai;MVSGALL ;wave:load "/user/wf.iqvsg";wave:exec on\n')
					# cntrl_sckt.sendall('*wai;MVSGALL ;wave:load "\//user/wf.iqvsg";wave:exec on\n')
					cntrl_sckt.sendall('MVSGALL ;wave:exec off;WLIST:WSEG1:DATA "/user/wf.iqvsg";wlist:wseg1:save;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1\n')			
					# cntrl_sckt.sendall('MVSGALL ;wave:exec off;WLIST:WSEG1:DATA "\//user/wf.iqvsg";wlist:wseg1:save;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1\n')			
			elif(action=='disable'):
				if(streams=='1x1'):
					cntrl_sckt.sendall('VSG1'+chain_sel_scpi_cmd+'; WAVE:EXEC OFF;WLIST:COUNT:DISABLE WSEG1\n')
				elif(streams=='2x2'):
					cntrl_sckt.sendall('MVSGALL; WAVE:EXEC OFF;WLIST:COUNT:DISABLE WSEG1\n')
		else:
			self.load_degrade_waveform(streams=streams,action=action)

	#Set RF Port on VSA
	def set_rf(self,streams='2x2',test='rx',chain_sel='1'):
		global chain_sel_scpi_cmd
		chain_sel_scpi_cmd=""
		print 'Setting RF Port in ',self.tester
		debugPrint('Setting RF Port in '+self.tester)
		if(test=='rx'):
			if(self.tester.lower()=='80'):
				if(streams=='1x1'):
					if(chain_sel=='1'):
						cntrl_sckt.sendall("ROUT1;PORT:RES RF1,VSG1\n")#RF1
					elif(chain_sel=='2'):
						cntrl_sckt.sendall("ROUT1;PORT:RES RF2,VSG1\n")#RF1
			elif(self.tester.lower()=='160'):
					if(streams=='1x1'):
						cntrl_sckt.sendall("ROUT1;PORT:RES RF1A,VSG11\n")#RF1
					elif(streams=='2x2'):
						cntrl_sckt.sendall("MVSG:DEF:ADD VSG11\n")#RF1
						cntrl_sckt.sendall("MVSG:DEF:ADD VSG12\n")#RF2
						cntrl_sckt.sendall("MROUT:DEF:ADD ROUT11\n")
						cntrl_sckt.sendall("MROUT:DEF:ADD ROUT12\n")#Adding Module
						time.sleep(2)
						cntrl_sckt.sendall('MROUT1;PORT:RES RF1A,VSG11\n')#Adding Module
						cntrl_sckt.sendall('MROUT2;PORT:RES RF2A,VSG12\n')

			elif(self.tester.lower()=='280'):			
				if(streams=='1x1'):
					if(chain_sel=='1'):
						cntrl_sckt.sendall("ROUT1;PORT:RES RF1A,VSG11\n")#RF1
					elif(chain_sel=='2'):
						cntrl_sckt.sendall("ROUT12;PORT:RES RF1B,VSG12\n")#RF1
						chain_sel_scpi_cmd=chain_sel
				elif(streams=='2x2'):
					cntrl_sckt.sendall("MVSG:DEF:ADD VSG11\n")#RF1
					cntrl_sckt.sendall("MVSG:DEF:ADD VSG12\n")#RF2
					cntrl_sckt.sendall("MROUT:DEF:ADD ROUT11\n")
					cntrl_sckt.sendall("MROUT:DEF:ADD ROUT12\n")#Adding Module
					time.sleep(2)
					cntrl_sckt.sendall('MROUT1;PORT:RES RF1B,VSG12\n')#Adding Module
					cntrl_sckt.sendall('MROUT2;PORT:RES RF1A,VSG11\n')
					cntrl_sckt.sendall('MROUT1;PORT:RES RF1A,VSG11\n')				
					cntrl_sckt.sendall('MROUT2;PORT:RES RF1B,VSG12\n')
		elif(test=='tx'):
			if(self.tester.lower()=='80'):
				if(streams=='1x1'):
					if(chain_sel=='1'):
						cntrl_sckt.sendall("ROUT1;PORT:RES RF1,VSA1\n")#RF1
					elif(chain_sel=='2'):	
						cntrl_sckt.sendall("ROUT1;PORT:RES RF2,VSA1\n")#RF1
			elif(self.tester.lower()=='160'):
				if(streams=='1x1'):
					if(chain_sel=='1'):
						cntrl_sckt.sendall("ROUT1;PORT:RES RF1A,VSA11\n")#RF1
					elif(chain_sel=='2'):	
						cntrl_sckt.sendall("ROUT12;PORT:RES RF1B,VSA12\n")#RF1
				elif(streams=='2x2'):
					cntrl_sckt.sendall("MVSA:DEF:ADD VSA11\n")#RF1
					cntrl_sckt.sendall("MVSA:DEF:ADD VSA12\n")#RF2
					cntrl_sckt.sendall("MROUT:DEF:ADD ROUT11\n")#ADD ROUT11
					cntrl_sckt.sendall("MROUT:DEF:ADD ROUT12\n")#Adding Module
					time.sleep(2)
					cntrl_sckt.sendall('MROUT2;PORT:RES RF2A,VSA12\n')
					cntrl_sckt.sendall('MROUT1;PORT:RES RF1A,VSA11\n')
			elif(self.tester.lower()=='280'):			
				if(streams=='1x1'):
					if(chain_sel=='1'): 
						cntrl_sckt.sendall("ROUT1;PORT:RES RF1A,VSA11\n")#RF1
					elif(chain_sel=='2'):	
						cntrl_sckt.sendall("ROUT12;PORT:RES RF1B,VSA12\n")#RF1
						chain_sel_scpi_cmd=chain_sel
				elif(streams=='2x2'):
					cntrl_sckt.sendall("MVSA:DEF:ADD VSA11\n")#RF1
					cntrl_sckt.sendall("MVSA:DEF:ADD VSA12\n")#RF2
					cntrl_sckt.sendall("MROUT:DEF:ADD ROUT11\n")
					cntrl_sckt.sendall("MROUT:DEF:ADD ROUT12\n")#Adding Module
					time.sleep(2)
					cntrl_sckt.sendall('MROUT1;PORT:RES RF1B,VSA12\n')#Adding Module
					cntrl_sckt.sendall('MROUT2;PORT:RES RF1A,VSA11\n')
					cntrl_sckt.sendall('MROUT1;PORT:RES RF1A,VSA11\n')				
					cntrl_sckt.sendall('MROUT2;PORT:RES RF1B,VSA12\n')

	def generate_degrade_waveform(self,awgn_snr='200',bw='20',standard='11n',dr='MCS7'):
		# print 'Generating noise wave'
		cntrl_sckt.sendall("CHAN1;GPRF;WAVE:DEGR:AWGN:SBW "+bw+"000000\n")
		cntrl_sckt.sendall("CHAN1;WIFI\n")
		
		cntrl_sckt.sendall('wave:gen:mmem "/user/wf.iqvsg", "WIFI wave generation from GUI"\n')	
		cntrl_sckt.sendall("CHAN1;GPRF;WAVE:DEGR:AWGN:SNR ("+awgn_snr+7*(','+awgn_snr)+")\n")
		cntrl_sckt.sendall('GPRF;WAVE:DEGR:APPL "\User\wf_degrade.iqvsg","\user/wf.iqvsg"\n')
	
	def load_degrade_waveform(self,streams='2x2',action='run'):		
		# print 'Loading noise wave'
		if(streams=='1x1'):
			cntrl_sckt.sendall('VSG1; WAVE:LOAD "/user/wf_degrade.iqvsg"\n')
		elif(streams=='2x2'):
			cntrl_sckt.sendall('MVSGALL; WAVE:LOAD "/user/wf_degrade.iqvsg"\n')

		if(action=='run'):
			if(streams=='1x1'):
				#VSG1 ;wave:exec off;WLIST:WSEG1:DATA "/user/deg.iqvsg";wlist:wseg1:save;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1

				cntrl_sckt.sendall('VSG1'+chain_sel_scpi_cmd+';WLIS:COUN 2000\n')
				cntrl_sckt.sendall('*wai;VSG1'+chain_sel_scpi_cmd+' ;wave:load "\//user/wf_degrade.iqvsg";wave:exec on\n')
				cntrl_sckt.sendall('VSG1'+chain_sel_scpi_cmd+' ;wave:exec off;WLIST:WSEG1:DATA "\//user/wf_degrade.iqvsg";wlist:wseg1:save;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1\n')
			elif(streams=='2x2'):
				cntrl_sckt.sendall('MVSGALL;WLIS:COUN 2000\n')
				cntrl_sckt.sendall('*wai;MVSGALL ;wave:load "\//user/wf_degrade.iqvsg";wave:exec on\n')
				cntrl_sckt.sendall('MVSGALL ;wave:exec off;WLIST:WSEG1:DATA "\//user/wf_degrade.iqvsg";wlist:wseg1:save;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1\n')			
		elif(action=='disable'):
			if(streams=='1x1'):
				cntrl_sckt.sendall('VSG1'+chain_sel_scpi_cmd+'; WAVE:EXEC OFF;WLIST:COUNT:DISABLE WSEG1\n')
			elif(streams=='2x2'):
				cntrl_sckt.sendall('MVSGALL; WAVE:EXEC OFF;WLIST:COUNT:DISABLE WSEG1\n')
			
	def init_vsg_funcs(self,standard='11ac',bw='20',streams='2x2',stbc='STBC_0',gi='LGI',coding='BCC',greenfield_mode='Mixed',preamble='LONG',payload='1024',test='rx',chain_sel='1'):
		self.start_vsg()
		self.set_equip_default()
		self.set_rf(streams=streams,test=test,chain_sel=chain_sel)
		self.set_modulation(standard)
		self.set_bandwidth(bw=bw,standard=standard)
		self.set_idleinterval(100)
		if((standard=='11n')or(standard=='11ac')):
			self.set_streams(standard,streams)
			self.set_stbc(stbc)
			self.set_guardinterval(gi)
			self.set_coding(coding)
		if(standard=='11n'):
			self.set_greenfield(greenfield_mode)
		if(standard=='11b'):
			self.set_preamble(preamble)		
		self.generate_waveform(streams=streams)		
		self.rf_on_off(rf_state='on',streams=streams)

	#Modulation Type
	def set_vsa_modulation(self,standard):
		debugPrint('Setting VSA Modulation as '+modulation)
		if(standard=='11b'):
			modulation='dsss'
		else:
			modulation='ofdm'
		print "\nSetting "+modulation+" in VSA"
		cntrl_sckt.sendall("CHAN1;WIFI;CONF:STAN "+modulation.upper()+"\n")
		if(standard=='11b'):
			cntrl_sckt.sendall("CHAN1;WIFI;CONF:STAN DSSS\n")
	
	#Setting Capture Length
	def set_capturelength(self,len,streams):
		print "\nSetting interval ",len
		debugPrint("\nSetting interval "+str(len))
		if(streams=='1x1'):
			cntrl_sckt.sendall('VSA1'+chain_sel_scpi_cmd+';CAPT:TIME '+str(float(len)/1000)+'\n')
		elif(streams=='2x2'):
			cntrl_sckt.sendall('MVSAALL;CAPT:TIME '+str(float(len)/1000)+'\n')
	
	#Apply to VSA
	def apply_vsa(self,chn='',bw='',streams='2x2',chain_sel_scpi_cmd='1'):
		print "\nApply settings to VSA",chn
		debugPrint("\nApply settings to VSA"+str(chn))
		if(bw=='20'):
			cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:IND1 '+str(chn)+'\n')
			cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:CBW 20000000\n')#20MHz
		elif(bw=='40'):
			if str(chn) in prime_20_sec_20_flags_dict[bw].keys():		
				cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:IND1 '+str(chn)+'\n')#For Plus
			else:
				cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:IND1 '+str(int(chn)-4)+'\n')#For Minus
			cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:CBW 40000000\n')#40MHz
		elif(bw=='80'):
			if(prime_20_sec_20_flags_dict[bw][str(chn)]=='l'):	
				cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:IND1 '+str(int(chn)-6)+'\n')#For Minus
			elif(prime_20_sec_20_flags_dict[bw][str(chn)]=='lr'):
				cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:IND1 '+str(int(chn)+2)+'\n')		
			elif(prime_20_sec_20_flags_dict[bw][str(chn)]=='rl'):
				cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:IND1 '+str(int(chn)-2)+'\n')		
			elif(prime_20_sec_20_flags_dict[bw][str(chn)]=='r'):
				cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:IND1 '+str(int(chn)+6)+'\n')#For Plus
			cntrl_sckt.sendall('CHAN1;WIFI;CONF:CHAN:CBW 80000000\n')#80MHz
		if(int(chn)<20):
			cntrl_sckt.sendall('CHAN1;WIFI;CONF:BAND 2G4\n')
		else:
			cntrl_sckt.sendall('CHAN1;WIFI;CONF:BAND 5G\n')
		if(streams=='1x1'):
			cntrl_sckt.sendall('CHAN1;WIFI; HSET:ALL VSA1'+chain_sel_scpi_cmd+'\n')
		elif(streams=='2x2'):
			cntrl_sckt.sendall('CHAN1;WIFI; HSET:ALL MVSAALL\n')

	#Save Power Values
	def save_power_values(self,dr,txp,ch,standard,streams,cable_loss_1x1,cable_loss_2x2):
		debugPrint('Saving Power Values')
		cntrl_sckt.sendall('WIFI\n')
		if(standard=='11b'):
			cntrl_sckt.sendall('CALC:POW 0,1\n')
		else:
			cntrl_sckt.sendall('CALC:POW 0,10\n')
		cntrl_sckt.sendall('FETCh:POW:SIGN1:AVER?\n')
		result=cntrl_sckt.recv(200)
		debugPrint(result)
		power_1x1=result.split(',')[-1]
		if(streams=='1x1'):
			debugPrint(round(float(power_1x1)+float(cable_loss_1x1),2))
			return round(float(power_1x1)+float(cable_loss_1x1),2)
		cntrl_sckt.sendall('FETCh:POW:SIGN2:AVER?\n')
		result=cntrl_sckt.recv(200)
		debugPrint(result)
		power_2x2=result.split(',')[-1]
		debugPrint(round(float(power_1x1)+float(cable_loss_1x1),2))
		debugPrint(round(float(power_2x2)+float(cable_loss_2x2),2))
		return round(float(power_1x1)+float(cable_loss_1x1),2),round(float(power_2x2)+float(cable_loss_2x2),2)

	def save_evm_txquality_stats(self,dr,txp,ch,standard,streams):
		debugPrint('Saving EVM Values')
		cntrl_sckt.sendall('FORM:READ:DATA ASC\n')
		if(standard=='11b'):
			cntrl_sckt.sendall('FETCh:TXQuality:DSSS:AVER?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			evm_1x1=result.split(',')[1]
			debugPrint(evm_1x1.rstrip())
			return evm_1x1.rstrip()
		else:
			cntrl_sckt.sendall('FETC:OFDM:EVM:DATA:ALL:AVER?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			evm_1x1=result.split(',')[1]
			if(streams=='1x1'):
				# return round(float(evm_1x1),2)
				debugPrint(evm_1x1.rstrip())
				return evm_1x1.rstrip()
			evm_2x2=result.split(',')[2]
		# print round(float(evm_1x1),2),round(float(evm_2x2),2)
		# return round(float(evm_1x1),2),round(float(evm_2x2),2)
		debugPrint(evm_1x1.rstrip())
		debugPrint(evm_2x2.rstrip())
		return evm_1x1.rstrip(),evm_2x2.rstrip()
	
	#Save Freq Err
	def save_freqerr(self,dr,txp,standard,streams):
		debugPrint('Saving SYSCLKERR Values')
		if(standard=='11b'):
			cntrl_sckt.sendall('FETCh:TXQuality:DSSS:AVER?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			freq_error_1x1=result.split(',')[4]
			# return round(float(freq_error_1x1),2)
			debugPrint(freq_error_1x1.rstrip())
			return freq_error_1x1.rstrip()
		else:
			cntrl_sckt.sendall('FETC:OFDM:FERR:ALL:AVER?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			freq_error_1x1=result.split(',')[1]
			if(streams=='1x1'):
				# return round(float(freq_error_1x1),2)
				debugPrint(freq_error_1x1.rstrip())
				return freq_error_1x1.rstrip()
			freq_error_2x2=result.split(',')[2]
		# return round(float(freq_error_1x1),2),round(float(freq_error_2x2)	,2)
		debugPrint(freq_error_1x1.rstrip())
		debugPrint(freq_error_2x2.rstrip())
		return freq_error_1x1.rstrip(),freq_error_2x2.rstrip()

	#Save Phase Err
	def save_phaseerr(self,dr,txp,standard,streams):
		debugPrint('Saving SYSCLKERR Values')
		if(standard=='11b'):
			cntrl_sckt.sendall('FETCh:TXQuality:DSSS:AVER?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			phaseerr_1x1=result.split(',')[3]
			# return round(float(phaseerr_1x1),2)
			debugPrint(phaseerr_1x1.rstrip())
			return phaseerr_1x1.rstrip()
		else:
			cntrl_sckt.sendall('FETC:OFDM:PERR:ALL:AVER?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			phaseerr_1x1=result.split(',')[1]
			if(streams=='1x1'):
				# return round(float(phaseerr_1x1),2)
				debugPrint(phaseerr_1x1.rstrip())
				return phaseerr_1x1.rstrip()
			phaseerr_2x2=result.split(',')[2]
		# return round(float(phaseerr_1x1),2),round(float(phaseerr_2x2),2)	
		debugPrint(phaseerr_1x1.rstrip())
		debugPrint(phaseerr_2x2.rstrip())
		return phaseerr_1x1.rstrip(),phaseerr_2x2.rstrip()

	#Save Gain Imb
	def save_ampimb(self,dr,txp,standard,streams):
		debugPrint('Saving GainImb Values')
		if(standard=='11b'):
			cntrl_sckt.sendall('FETCh:TXQuality:DSSS:AVER?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			ampimb_1x1=result.split(',')[8]
			# return round(float(ampimb_1x1),2)
			debugPrint(ampimb_1x1.rstrip())
			return ampimb_1x1.rstrip()
		else:
			cntrl_sckt.sendall('FETC:OFDM:AIMB:ALL:AVER?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			ampimb_1x1=result.split(',')[1]
			if(streams=='1x1'):
				# return round(float(ampimb_1x1),2)
				debugPrint(ampimb_1x1.rstrip())
				return ampimb_1x1.rstrip()
			ampimb_2x2=result.split(',')[2]
		# return round(float(ampimb_1x1),2),round(float(ampimb_2x2),2)
		debugPrint(ampimb_1x1.rstrip())
		debugPrint(ampimb_2x2.rstrip())
		return ampimb_1x1.rstrip(),ampimb_2x2.rstrip()

	#Save Phase Imb	
	def save_phaseimb(self,dr,txp,standard,streams):
		debugPrint('Saving PhaseImb Values')
		if(standard=='11b'):
			cntrl_sckt.sendall('FETCh:TXQuality:DSSS:AVER?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			phaseimb_1x1=result.split(',')[9]
			# return round(float(phaseimb_1x1),2)
			debugPrint(phaseimb_1x1.rstrip())
			return phaseimb_1x1.rstrip()
		else:	
			cntrl_sckt.sendall('FETC:OFDM:PIMB:ALL:AVER?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			phaseimb_1x1=result.split(',')[1]
			if(streams=='1x1'):
				# return round(float(phaseimb_1x1),2)
				debugPrint(phaseimb_1x1.rstrip())
				return phaseimb_1x1.rstrip()
			phaseimb_2x2=result.split(',')[2]
		# return round(float(phaseimb_1x1),2),round(float(phaseimb_2x2),2)
		debugPrint(phaseimb_1x1.rstrip())
		debugPrint(phaseimb_2x2.rstrip())
		return phaseimb_1x1.rstrip(),phaseimb_2x2.rstrip()

	#Save TX Quality Stats
	def save_txquality_stats(self,dr,txp,ch,standard,streams):
		# print('Saving EVM Values')
		debugPrint('Saving EVM Values')
		cntrl_sckt.sendall('FORM:READ:DATA ASC\n')
		if(standard=='11b'):
			cntrl_sckt.sendall('FETCh:TXQuality:DSSS?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			evm_1x1=result.split(',')[1]
			evm_2x2=result.split(',')[1]
			phaseerr_1x1=result.split(',')[3]
			phaseerr_2x2=result.split(',')[3]
			freq_error_1x1=result.split(',')[4]
			freq_error_2x2=result.split(',')[4]
			sysclkerr_1x1=result.split(',')[6]
			sysclkerr_2x2=result.split(',')[6]
			lo_leakage_1x1=result.split(',')[7]
			lo_leakage_2x2=result.split(',')[7]
			ampimb_1x1=result.split(',')[8]
			ampimb_2x2=result.split(',')[8]
			phaseimb_1x1=result.split(',')[8]
			phaseimb_2x2=result.split(',')[8]
		else:
			if(streams=='1x1'):
				phaseimb_1x1=self.save_phaseimb(dr,txp,standard,streams)
				evm_1x1=self.save_evm_txquality_stats(dr,txp,ch,standard,streams)
				phaseerr_1x1=self.save_phaseerr(dr,txp,standard,streams)
				freq_error_1x1=self.save_freqerr(dr,txp,standard,streams)
				sysclkerr_1x1=self.save_sysclkerr(dr,txp,standard,streams)
				lo_leakage_1x1=self.save_lo_leakage(dr,txp,standard,streams)
				ampimb_1x1=self.save_ampimb(dr,txp,standard,streams)
			elif(streams=='2x2'):
				phaseimb_1x1,phaseimb_2x2=self.save_phaseimb(dr,txp,standard,streams)
				evm_1x1,evm_2x2=self.save_evm_txquality_stats(dr,txp,ch,standard,streams)
				phaseerr_1x1,phaseerr_2x2=self.save_phaseerr(dr,txp,standard,streams)
				freq_error_1x1,freq_error_2x2=self.save_freqerr(dr,txp,standard,streams)
				sysclkerr_1x1,sysclkerr_2x2=self.save_sysclkerr(dr,txp,standard,streams)
				lo_leakage_1x1,lo_leakage_2x2=self.save_lo_leakage(dr,txp,standard,streams)
				ampimb_1x1,ampimb_2x2=self.save_ampimb(dr,txp,standard,streams)
		if(streams=='1x1'):
			return evm_1x1,phaseerr_1x1,freq_error_1x1,sysclkerr_1x1,lo_leakage_1x1,ampimb_1x1,phaseimb_1x1
		return evm_1x1,evm_2x2,phaseerr_1x1,phaseerr_2x2,freq_error_1x1,freq_error_2x2,sysclkerr_1x1,sysclkerr_2x2,lo_leakage_1x1,lo_leakage_2x2,ampimb_1x1,ampimb_2x2,phaseimb_1x1,phaseimb_2x2
	#Save Sys Clk Err
	def save_sysclkerr(self,dr,txp,standard,streams):
		debugPrint('Saving SYSCLKERR Values')
		if(standard=='11b'):
			cntrl_sckt.sendall('FETC:DSSS:SCER:ALL:AVER?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			sysclkerr_1x1=result.split(',')[6]
			debugPrint(sysclkerr_1x1.rstrip())
			return sysclkerr_1x1.rstrip()
		else:
			cntrl_sckt.sendall('FETC:OFDM:SCER:ALL:AVER?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			sysclkerr_1x1=result.split(',')[1]
			if(streams=='1x1'):
				# return round(float(sysclkerr_1x1),2)
				debugPrint(sysclkerr_1x1.rstrip())
				return sysclkerr_1x1.rstrip()
			sysclkerr_2x2=result.split(',')[2]
		# return round(float(sysclkerr_1x1),2),round(float(sysclkerr_2x2),2)
		debugPrint(sysclkerr_1x1.rstrip())
		debugPrint(sysclkerr_2x2.rstrip())
		return sysclkerr_1x1.rstrip(),sysclkerr_2x2.rstrip()

	#Save Gain Imb
	def save_gainimb(self,dr,txp,standard,streams):
		if(standard=='11b'):
			cntrl_sckt.sendall('FETC:DSSS:AIMB:ALL:AVER?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			gainimb_1x1=result.split(',')[8]
		else:
			cntrl_sckt.sendall('FETC:OFDM:AIMB:ALL:AVER?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			ampimb_1x1=result.split(',')[1]
			if(streams=='2x2'):
				gainimb_2x2=result.split(',')[2]
		return float(gainimb_1x1),float(gainimb_2x2)

	#Save LO Leakage
	def save_lo_leakage(self,dr,txp,standard,streams):
		debugPrint('Saving lo_leakage Values')
		if(standard=='11b'):
			cntrl_sckt.sendall('FETC:DSSS:LOLeakage:ALL:AVER?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			lo_leakage_1x1=result.split(',')[6]
			debugPrint(lo_leakage_1x1.rstrip())
			return lo_leakage_1x1.rstrip()
		else:
			cntrl_sckt.sendall('FETC:OFDM:LOLeakage:ALL:AVER?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			lo_leakage_1x1=result.split(',')[1]
			if(streams=='1x1'):
				# return round(float(lo_leakage_1x1),2)
				debugPrint(lo_leakage_1x1.rstrip())
				return lo_leakage_1x1.rstrip()
			lo_leakage_2x2=result.split(',')[2]
		# return round(float(lo_leakage_1x1),2),round(float(lo_leakage_2x2),2)
		debugPrint(lo_leakage_1x1.rstrip())
		debugPrint(lo_leakage_2x2.rstrip())
		return lo_leakage_1x1.rstrip(),lo_leakage_2x2.rstrip()

	#Save OBW
	def save_obw_values(self,standard,streams):
		cntrl_sckt.sendall('CHAN1\n')
		if(streams=='2x2'):
			cntrl_sckt.sendall('MVSAALL ;init\n')
		else:
			cntrl_sckt.sendall('VSA1'+chain_sel_scpi_cmd+' ;init\n')			
		cntrl_sckt.sendall('WIFI\n')
		if(standard=='11b'):
			cntrl_sckt.sendall('calc:pow 0, 1\n')
			cntrl_sckt.sendall('calc:txq 0, 1\n')
			cntrl_sckt.sendall('calc:ccdf 0, 1\n')
			cntrl_sckt.sendall('calc:spec 0, 1\n')		
		else:
			cntrl_sckt.sendall('calc:txq 0, 1\n')

		debugPrint('Saving OBW Values')
		if(standard=='11b'):
			obw_1x1='20000000'
		else:
			cntrl_sckt.sendall('FETCH:TXQuality:OFDM:INFO:CBW?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			obw_1x1=result.split(',')[1]
		debugPrint(str(int(obw_1x1)/1000000))
		return str(int(obw_1x1)/1000000)

	#Save Data Rate Values
	def save_datarate_values(self,standard,streams):
		debugPrint('Saving data rate Values')
		if(standard=='11b'):
			cntrl_sckt.sendall('FETCH:TXQuality:DSSS:INFO:DRATE?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			dr_1x1=result.split(',')[1].rstrip()
			debugPrint(dr_1x1)
			return dr_1x1
		elif(standard=='11g' or standard=='11a'):
			cntrl_sckt.sendall('FETCH:TXQuality:OFDM:INFO:DRATE?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			dr_1x1=result.split(',')[1].rstrip()
			debugPrint(dr_1x1)
			return dr_1x1
		else:
			cntrl_sckt.sendall('FETCH:TXQuality:OFDM:INFO:MCS?\n')
			result=cntrl_sckt.recv(200)
			debugPrint(result)
			dr_1x1=result.split(',')[1].rstrip()
			dr_1x1='MCS'+dr_1x1
			debugPrint(dr_1x1)
			return dr_1x1
			if(streams=='2x2'):
				dr_2x2=result.split(',')[2]
				dr_2x2='MCS'+dr_2x2
		debugPrint(dr_1x1)
		debugPrint(dr_2x2)
		return dr_1x1,dr_2x2

	def save_spec_margins(self,standard,ch,bw='20'):
		# if (standard == '11b'):
			# time.sleep(2)
			# cntrl_sckt.sendall('VSA1;WIFI;CLE:SPEC\n')
			# set_modulation('OFDM')
			# set_frequency(ch)
			# time.sleep(0.5)
			# cntrl_sckt.sendall('VSA1;INIT\n')
			# cntrl_sckt.sendall('WIFI\n')
			# cntrl_sckt.sendall('CALC:SPEC 0,10\n')
			# time.sleep(0.5)
		cntrl_sckt.sendall('FORM:READ:DATA ASC\n')
		cntrl_sckt.sendall('FETC:SPEC:AVER:MARG:OFR?\n')
		#time.sleep(0.5)
		result=cntrl_sckt.recv(512)
		debugPrint(result)
		# print result
		# print "Avg Spectrum margin offset frequencies in Hz: ",result[2:-1]
		spectrum_result=result.split(',')
		spectral_margins_freq = spectrum_result[1:]
		
		# for i in spectral_margins_freq:
			# spec_data.append(round(float(i),2))
		cntrl_sckt.sendall('FETC:SPEC:AVER:MARG?\n')
		#time.sleep(0.5)
		result=cntrl_sckt.recv(512)
		debugPrint(result)
		spectrum_result=result.split(',')
		spectrum_status_code = float(spectrum_result[0])
		spectral_margins = spectrum_result[1:]
		# print 'spectrum_status_code',spectrum_status_code
		if (spectrum_status_code == 0):
			# print "Avg spectrum margin (Passed) in dB: ",result[2:-1]
			debugPrint("PASS,PASS")
			return "PASS","PASS"
			# for i in spectral_margins:
				# spec_data.append(round(float(i),2))
		elif (spectrum_status_code == 1):
			# print "Avg spectrum margin (Failed) in dB: ",result[2:-1]
			debugPrint("FAIL,FAIL")
			return "FAIL","FAIL"
			# data.append('FAIL')
			# for i in spectral_margins:
				# spec_data.append(round(float(i),2))
		else:
			debugPrint("NODATA,NODATA")
			return "NODATA","NODATA"
			# for i in spectral_margins:
				# spec_data.append('NODATA')
		
		cntrl_sckt.sendall('FETC:SPEC:MAX:MARG:OFR?\n')
		#time.sleep(0.5)
		result=cntrl_sckt.recv(512)
		debugPrint(result)
		# print "Max Spectrum margin offset frequencies in Hz: ",result[2:-1]
		max_spectrum_result=result.split(',')
		max_spectral_margins_freq = max_spectrum_result[1:]
		for i in max_spectral_margins_freq:
			max_spec_data.append(i)
		
		cntrl_sckt.sendall('FETC:SPEC:MAX:MARG?\n')
		#time.sleep(0.5)
		result=cntrl_sckt.recv(512)
		debugPrint(result)
		max_spectrum_result=result.split(',')
		max_spectrum_status_code = float(max_spectrum_result[0])
		max_spectral_margins = max_spectrum_result[1:]
		if (max_spectrum_status_code == 0):
			print "Max spectrum margin (Passed) in dB: ",result[2:-1]
			return "PASS"
			for i in max_spectral_margins:
				max_spec_data.append(i)
		elif (max_spectrum_status_code == 1):
			print "Max spectrum margin (Failed) in dB: ",result[2:-1]
			return "FAIL"
			for i in max_spectral_margins:
				max_spec_data.append(i)
		else:
			return "NODATA"
			for i in max_spectral_margins:
				max_spec_data.append('NODATA')
		if (standard == '11b') and (bwcfg != '20C'):
			set_modulation('DSSS') #Revert to DSSS

	def save_ofdm_spec_flatness(self,standard):
		if (standard == '11b'):
			return 'NODATA','NODATA'
		else:
			cntrl_sckt.sendall('FETC:TXQ:OFDM:SFL:MARG?\n')
		result=cntrl_sckt.recv(2048)
		sfl_check_result=result.split(',')
		if all(float(sf)==0 for sf in sfl_check_result[::5]):
			if all(float(s_f)>=0 for s_f in sfl_check_result):
				# print "OFDM spectral flatness check: PASS"
				return "PASS","PASS"
				cntrl_sckt.sendall('FETC:TXQ:OFDM:SFL:AVER:MARG?\n')
				result=cntrl_sckt.recv(512)
				if (float(result.split(',')[0]) == 0):
					print "Average OFDM spectral flatness margins in dB:",result[2:-1]
			else:
				# print "OFDM spectral flatness check: FAIL"
				# print "OFDM spectral flatness margins:",result[:-1]
				return "FAIL","FAIL"
		else:
			# print "OFDM SPECTRAL FLATNESS CHECK: NODATA"
			# print "OFDM spectral flatness check result:",result[:-1]
			return 'NODATA','NODATA'

	def save_psdu_crc(self,standard,d_rate):
			if(standard=='11b'):
				cntrl_sckt.sendall('FETC:TXQ:DSSS:PSDU:CRC?\n')
			else:
				cntrl_sckt.sendall('FETC:TXQ:OFDM:PSDU:CRC?\n')
			result=cntrl_sckt.recv(512)
			debugPrint(result)
			psdu_crc_result=result.split(',')
			if all(float(pc)==0 for pc in psdu_crc_result[::2]):
				if all(float(pc)==1 for pc in psdu_crc_result[1::2]):
					# print "PSDU CRC: PASS"
					return "PASS","PASS"
				else:
					# print "PSDU CRC result:",result[:-1]
					# print "PSDU CRC: FAIL"
					return "FAIL","FAIL"
			else:
				# print "PSDU CRC result:",result[:-1]
				# print "PSDU CRC: NODATA"
				return 'NODATA','NODATA'

	#Click AGC Button	
	def click_agc(self,standard,streams,ref_level='AUTO',chain_sel_scpi_cmd='1'):
		debugPrint('Click AGC')
		if(streams=='2x2'):
			cntrl_sckt.sendall('MVSAALL ;RLEVel '+ref_level+'\n')
		else:
			cntrl_sckt.sendall('VSA1'+chain_sel_scpi_cmd+' ;RLEVel:AUTO\n')
			# # cntrl_sckt.sendall('VSA1;RLEV 25\n')
			# cntrl_sckt.sendall('VSA1;RLEV '+ref_level+'\n')
		return
		cntrl_sckt.sendall('CHAN1\n')
		if(streams=='2x2'):
			cntrl_sckt.sendall('MVSAALL ;init\n')
		else:
			cntrl_sckt.sendall('VSA1'+chain_sel_scpi_cmd+' ;init\n')
		cntrl_sckt.sendall('WIFI\n')
		if(standard=='11b'):
			cntrl_sckt.sendall('calc:pow 0, 1\n')
			cntrl_sckt.sendall('calc:txq 0, 1\n')
			cntrl_sckt.sendall('calc:ccdf 0, 1\n')
			cntrl_sckt.sendall('calc:spec 0, 1\n')
		else:
			cntrl_sckt.sendall('calc:pow 0, 10\n')
			cntrl_sckt.sendall('calc:txq 0, 10\n')
			cntrl_sckt.sendall('calc:ccdf 0, 10\n')
			cntrl_sckt.sendall('calc:ramp 0, 10\n')
			cntrl_sckt.sendall('calc:spec 0, 10\n')

	#Start Packet Analyses
	def click_analyser(self,standard,streams,chain_sel_scpi_cmd='1'):
		debugPrint('Click Analyser')
		cntrl_sckt.sendall('CHAN1\n')
		if(streams=='2x2'):
			cntrl_sckt.sendall('MVSAALL ;init\n')
		else:
			cntrl_sckt.sendall('VSA1'+chain_sel_scpi_cmd+' ;init\n')			
		cntrl_sckt.sendall('WIFI\n')
		if(standard=='11b'):
			cntrl_sckt.sendall('calc:pow 0, 1\n')
			cntrl_sckt.sendall('calc:txq 0, 1\n')
			cntrl_sckt.sendall('calc:ccdf 0, 1\n')
			cntrl_sckt.sendall('calc:spec 0, 1\n')		
		else:
			cntrl_sckt.sendall('calc:pow 0, 10\n')
			cntrl_sckt.sendall('calc:txq 0, 1\n')
			cntrl_sckt.sendall('calc:ccdf 0, 10\n')
			cntrl_sckt.sendall('calc:spec 0, 10\n')		

	#Modulation Type
	def set_vsa_modulation(self,standard):
		debugPrint('Setting VSA standard '+standard)
		if(standard=='11b'):
			modulation='dsss'
		else:
			modulation='ofdm'
		print "\nSetting "+modulation+" in VSA"
		debugPrint("\nSetting "+modulation+" in VSA")
		cntrl_sckt.sendall("CHAN1;WIFI;CONF:STAN "+modulation.upper()+"\n")
		if(standard=='11b'):
			cntrl_sckt.sendall("CHAN1;WIFI;CONF:STAN DSSS\n")

	def init_vsa_funcs(self,standard='11ac',bw='20',streams='2x2',stbc='STBC_0',gi='LGI',coding='BCC',greenfield_mode='Mixed',preamble='LONG',payload='1024',chain_sel='1'):	
		self.start_vsg()
		self.set_equip_default()
		self.set_rf(streams=streams,test='tx',chain_sel=chain_sel)
		self.set_vsa_modulation(standard)
		self.set_capturelength(100,streams)
	def config_adj_11a(self):
		return
		
	#802.11b Initialization settings
	def config_adj_11b(self):
		return
	#802.11g Initialization settings
	def config_adj_11g(self):
		return
		
	#802.11n Initialization settings
	def config_adj_11n(self):
		return
		
	#802.11ac Initialization settings
	def config_adj_11ac(self):
		return
		
		
	#Modulation Type
	def set_adj_modulation(self,standard):	
		print "\nSetting "+standard+" in VSA"
		return

	#Setting Payload
	def set_adj_payload(self,standard,payload):
		print "\nSetting payload ",payload
		return
			

	#Setting MAC Header OFF
	def set_adj_macheader(self):
		print 'Set adj MACHeader'
		return

	#Setting Channel
	def apply_adjacent_vsg(self,bw='',chn='',streams='2x2',config='adj'):
		print 'apply_adjacent_vsg'
		return
		
	#Setting Adj Amplitude	
	def set_adj_amplitude(self,streams,ampl):
		print "\nSetting adj amplitude ",ampl
		return
		
	def set_adj_bandwidth(self,standard='',bw=''):
		print 'set_adj_bandwidth'
		return

	#RF ON/OFF
	def rf_on_off_adj(self,rf_state='on',streams='1x1'):
		print "\nSetting RF ",rf_state
		return

	def set_pop_trigger(self,packet_delay='',packet_cnt='2000'):
		print 'Setting packet delay ',packet_delay 
		return	
