from commonUtils import *

class NRF:
	phy_stats_headings=['VSG_CNT','CRC32_PASS_CNT','CRC32_FAIL_CNT','PER %','RSSI']
	def __init__(self,com_port):
		self.com_port = com_port
		
	#Set Streams
	def set_dut_streams(self,streams='2x2'):
		return

		
	#Set Production Mode Settings
	def set_dut_production_mode_settings(self,standard='',ch='',bw='',stbc='',gi='',coding='',greenfield_mode='',preamble='',test='rx',action=''):
		# print'\nSetting DUT in production mode\n'
		debugPrint('\nSetting DUT in production mode\n')
		self.dut_write('wifi_radio_test tx 0')
		self.dut_write('wifi_radio_test rx 0')
		self.dut_write('wifi_radio_test tx_pkt_rate -1')
		self.dut_write('wifi_radio_test tx_pkt_mcs -1')
		self.dut_write('wifi_radio_test tx_pkt_tput_mode 0')
		# self.dut_write('wifi_radio_test rf_params 0000000000002C00000000000000006060606060606060600000000050EC000000000000000000000000')
		self.set_rf_params()
		self.dut_write('wifi_radio_test phy_calib_rxdc 1')
		self.dut_write('wifi_radio_test phy_calib_txdc 1')
		self.dut_write('wifi_radio_test phy_calib_txpow 1')
		self.dut_write('wifi_radio_test phy_calib_rxiq 1')
		self.dut_write('wifi_radio_test phy_calib_txiq 1')
		# self.dut_write('wifi_radio_test phy_calib_dpd 1')
		if('tx' in test):
			if((standard=='11n')or(standard=='11ac')):
				self.dut_write('wifi_radio_test tx_pkt_len 4096 ')
			elif((standard=='11a')or(standard=='11b')or(standard=='11g')):
				self.dut_write('wifi_radio_test tx_pkt_len 1024')
			elif(standard=='11b'):
				self.dut_write('wifi_radio_test tx_pkt_len 1024')
				if(preamble.lower()=='short'):
					self.dut_write('wifi_radio_test tx_pkt_preamble 0')#SHORT
				elif(preamble.lower()=='long'):
					self.dut_write('wifi_radio_test tx_pkt_preamble 1')#LONG
		
	#SET IBSS Mode
	def set_dut_ibss(self,standard='11ac',channel='144',bw='20',streams='2x2',wait='yes'):
		return
	
	def set_dut_channel(self,ch):
		# print'Setting DUT in Channel -',ch
		debugPrint('Setting DUT in Channel -',ch)
		self.dut_write('wifi_radio_test tx 0')
		self.dut_write('wifi_radio_test rx 0')
		res=self.dut_write_read('wifi_radio_test chnl_primary '+ch.rstrip())	
		if(('FAIL' in res) or ('Intf not ready for 1000' in res) or ('RPU_WIFI_HAL' in res)):
			return 'FAIL'
		return 'SUCCESS'
	
	def dut_check_prompt(self):
		return

	def dut_get_ipaddr(self):
		return

	
	def dut_login(self,res=''):
		return

	def load_release_files(self,load='0'):
		self.get_stats_path()
		return

	def	get_phy_stats(self):
		res=self.dut_write_read('wifi_radio_test get_stats')
		return res

	def compute_per(self,modulation,dr,ch,streams,standard,tester,dut,equipment,wave_type):
		per=0
		global per_clmn
		global row_num
		global row_num_dr
		try:
			del per_data[:]
		except:
			per_data=[]
		res=dut.dut_down_up(action='up_down',ch=ch)
		equipment.send_packets(streams=streams,action='run',wave_type=wave_type)
		start_time=time.time()
		end_time=time.time()
		if(('LMAC Initialization Failed' in res) or ('SIOCSIFFLAGS' in res) or ('cut here' in res) or ('Intf not ready for 1000ms' in res) or ('Spurious interrupt received' in res) or ('RPU_WIFI_HAL' in res)):
			per_data.append('LOCKUP')
			per_data.append('LOCKUP')
			per_data.append('LOCKUP')
			per=float(0)
			return per_data,'FAIL'
		execution_step=1
		if(str(dr)=='1'):
			est_time_tm=25
		else:
			est_time_tm=15
		while(1):
			res=dut.get_phy_stats()

			m=re.compile("ofdm_crc32_pass_cnt=(.*)")
			if(len(m.findall(res))>0):
				if(standard!='11b'):
					m=re.compile("ofdm_crc32_pass_cnt=(.*)")
					crc32_pass_cnt=int(m.findall(res)[0])
					m=re.compile("ofdm_crc32_fail_cnt=(.*)")
					crc32_fail_cnt=int(m.findall(res)[0])
				else:
					m=re.compile("dsss_crc32_pass_cnt=(.*)")
					crc32_pass_cnt=int(m.findall(res)[0])
					m=re.compile("dsss_crc32_fail_cnt=(.*)")
					crc32_fail_cnt=int(m.findall(res)[0])
				actual_pkt_cnt=crc32_pass_cnt+crc32_fail_cnt
				if(execution_step==1):
					prev_actual_pkt_cnt=actual_pkt_cnt
					curr_actual_pkt_cnt=actual_pkt_cnt
				else:
					prev_actual_pkt_cnt=curr_actual_pkt_cnt
					curr_actual_pkt_cnt=actual_pkt_cnt
				if(actual_pkt_cnt>=num_of_pkts_from_vsg):	
					break
				if((end_time-start_time)>est_time_tm):
					break
				elif((end_time-start_time)>3):
					if(actual_pkt_cnt<100):
						break
					if(curr_actual_pkt_cnt-prev_actual_pkt_cnt<5):
						break
				execution_step+=1
			elif('FAIL' in res):
				print res
				print m.findall(res)

				per_data.append('LOCKUP')
				per_data.append('LOCKUP')
				per_data.append('LOCKUP')
				per_data.append('LOCKUP')
				per=float(0)
				return per_data,'FAIL'

			else:
				print (m.findall(res))
				print len(m.findall(res))
				print res
				per_data.append('NODATA')
				per_data.append('NODATA')
				per_data.append('NODATA')
				per_data.append('NODATA')
				per=float(0)
				return per_data,'FAIL'

			end_time=time.time()
		per_data.append(int(num_of_pkts_from_vsg))
		per_data.append(int(crc32_pass_cnt))
		per_data.append(int(crc32_fail_cnt))
		try:
			if(int(actual_pkt_cnt)<100):
				per=100
				per_data.append(100)
			else:
				if(int(ch)<15):
					if('iqxel' in tester.lower()):
						per=round(((num_of_pkts_from_vsg+2-crc32_pass_cnt) * 100) / float(num_of_pkts_from_vsg+2))
					else:	
						per=round(((num_of_pkts_from_vsg+2-crc32_pass_cnt) * 100) / float(num_of_pkts_from_vsg+2))
				else:
					if('iqxel' in tester.lower()):
						per=round(((num_of_pkts_from_vsg+2-crc32_pass_cnt) * 100) / float(num_of_pkts_from_vsg+2)) 
					else:	
						per=round(((num_of_pkts_from_vsg+2-crc32_pass_cnt) * 100) / float(num_of_pkts_from_vsg+2)) 
				debugPrint('PER -> '+str(per))
				if('-' in str(per)):
					if(actual_pkt_cnt>num_of_pkts_from_vsg):

						if(crc32_pass_cnt<num_of_pkts_from_vsg):
							per=round(((actual_pkt_cnt-crc32_pass_cnt) * 100) / float(actual_pkt_cnt))
						else:
							per=0
					per=0
				per_data.append(float(per))
		except Exception,E:
			print E.args
			print '\nDUT hard reboot'

			per_data.append('LOCKUP')
			per_data.append('LOCKUP')
			per_data.append('LOCKUP')
			per_data.append('LOCKUP')
			per=float(0)
			return per_data,'FAIL'		
		try:
			m=re.compile("rssi_avg[\t ]*=[\t ]*(.*)[\t ]*dBm")
			rssi_avg=int(m.findall(res)[0])
			per_data.append(int(rssi_avg))
		except:
			per_data.append('NODATA')

		return per_data,"PASS"

	def get_stats_path(self):
		global stats_path
		stats_path=''
		
	def dut_reboot(self):
		# print('DUT Reboot')
		os.system('nrfjprog -f NRF53 --reset')

	#Setting Datarate
	def set_dut_datarate(self,data_rate,standard):
		debugPrint("\nStandard : " + standard)
		# print"\nSetting data rate ",data_rate
		debugPrint("\nSetting data rate " + data_rate)
		if('MCS' in data_rate):
			op_str="""p=`cat /sys/kernel/debug/img/wlan/conf | grep tx_pkt_rate | cut -f2 -d'='`
			if [ $p -ne "-1" ]
			then
				wifi_radio_test tx_pkt_rate -1" > /sys/kernel/debug/img/wlan/conf
			fi 
			"""
			# res=self.dut_write_read(op_str)
			# debugPrint( res )
			res=self.dut_write('wifi_radio_test tx 0')
			debugPrint( res )
			if (standard=='11n'):
				res=self.dut_write('wifi_radio_test tx_pkt_tput_mode 1')
			elif (standard=='11ac'):
				res=self.dut_write('wifi_radio_test tx_pkt_tput_mode 2')
				
			self.dut_write('wifi_radio_test tx_pkt_rate -1')
			self.dut_write('wifi_radio_test tx_pkt_mcs '+data_rate.lower().split('mcs')[-1])
		else:
			op_str="""q=`cat /sys/kernel/debug/img/wlan/conf | grep tx_pkt_mcs | cut -f2 -d'='`
			if [ $q -ne "-1" ]
			then	
				wifi_radio_test tx_pkt_mcs -1" > /sys/kernel/debug/img/wlan/conf
			fi
			"""
			# res=self.dut_write_read(op_str)
			# debugPrint( res )
			self.dut_write('wifi_radio_test tx 0')
			self.dut_write('wifi_radio_test tx_pkt_mcs -1')

			self.dut_write('wifi_radio_test tx_pkt_rate '+data_rate)

	#Setting TXPower
	def set_dut_txpower(self,txp):
		debugPrint("\nSetting TX Power "+str(txp))
		self.dut_write('wifi_radio_test tx 0')
		# time.sleep(1)
		self.dut_write('wifi_radio_test tx_power '+txp)
		# time.sleep(1)
		self.dut_write('wifi_radio_test tx 1')
		# time.sleep(1)

	#Setting RF Params 
	def set_rf_params(self, xo = "2C"):
		if os.path.exists('xo_val_board_'+board_num+'.txt'):
			fopen = open('xo_val_board_'+board_num+'.txt', 'r')
			xo=fopen.read()
			fopen.close()
			if xo == "":
				xo = "2C"
		self.dut_write('wifi_radio_test rf_params 000000000000'+xo+'00000000000000006060606060606060600000000050EC000000000000000000000000')

	#Setting XO 
	def set_dut_xo(self,xo='2C'):
		if os.path.exists('xo_val_board_'+board_num+'.txt'):
			fopen = open('xo_val_board_'+board_num+'.txt', 'r')
			xo=fopen.read()
			fopen.close()
			if xo == "":
				xo = xo
		# print ("\nSetting XO "+str(xo))
		debugPrint("\nSetting XO "+str(xo))
		self.dut_write('wifi_radio_test tx 0')
		time.sleep(0.5)
		# self.dut_write('wifi_radio_test rf_params 00000000000000000000000000006060606060606060600000000050EC000000000000000000000000')
		self.dut_write('wifi_radio_test rf_params 000000000000'+xo+'00000000000000006060606060606060600000000050EC000000000000000000000000')
		time.sleep(0.5)
		self.dut_write('wifi_radio_test tx 1')
		time.sleep(0.5)

	#Start/Kill pktgen
	def pktgen_tool(self,status):
		debugPrint('Pktgen '+status)
		global per_clmn
		global row_num_dr
		if(status=='write'):
			return
		elif(status=='run'):
			self.dut_write('wifi_radio_test tx 1')
		elif(status=='kill'):
			self.dut_write('wifi_radio_test tx 0')
		time.sleep(0.5)

	#Set RF Params
	def set_dut_rfconf(self,release):
		return
		if(os.path.exists('rf_conf_'+release)):
			print 'Reading rf from file'
			debugPrint('Reading rf from file')
			f_rfconf=open('rf_conf_'+release,'r')		
			rfconf_string=f_rfconf.read()
			f_rfconf.close()
		else:
			print 'Reading default RF Params'
			debugPrint('Reading default RF Params')
			res=self.dut_write_read('cat '+stats_path+'conf |grep rf_conf\ ')
			rfconf_string_read=res
			rfconf_string=rfconf_string_read.split('rf_conf =')[1].split('\r\n')[0].replace(' ','').replace('0808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808080808','2828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828282828')	
		self.dut_write('wifi_radio_test rf_conf '+rfconf_string)	
		return rfconf_string

	def set_production_calib_txpower(self,txp):
		# print"\nSetting TX Power ",txp
		debugPrint("\nSetting TX Power "+str(txp))
		self.dut_write('wifi_radio_test set_tx_power '+txp)

	def save_pdout_values(self,dr,txp):
		return

	def dut_state_handle(self,prompt):	
		return

	def check_dut_stuck_state(self):
		debugPrint('Trying to check_dut_stuck_state')
		res=self.dut_write_read('pwd')
		if(res.find('root')>=0):
			return 'alive'
		else:
			return 'stuck'
			
	def check_dut_load_issues(self):
		debugPrint('Trying to check_dut_load_issues')
		res=self.dut_write('\n')
		print res
		if(res.find('login:')>=0) or (res.find('#')>=0):
			return 'alive'
		else:
			return 'stuck'

	def dut_down_up(self,action='down',ch='36'):
		debugPrint('Ifconfig '+action)
		if(action=='down'):
			self.dut_write('wifi_radio_test tx 0 ')
			self.dut_write('wifi_radio_test rx 0 ')
			time.sleep(1)
		elif(action=='up'):
			time.sleep(1)
			return res
		elif(action=='up_down'):
			time.sleep(1)
			#self.dut_write('wifi_radio_test tx=0 ')
			self.dut_write('wifi_radio_test rx 0')
			self.dut_write('wifi_radio_test rx 1')			
			res=self.dut_write_read('\n')	
			time.sleep(1)
			
			return res
		
	def dut_read(self,num_of_bytes=1000):
		return
		
	def dut_write(self,cmd):
		# print('Command Passed ->  '+ cmd)
		debugPrint('Command Passed ->  '+ cmd)
		try:
			dut_obj.write(cmd+'\n')
			time.sleep(0.5)
		except Exception,e:
			print e.args
			print 'FAIL'
			return 'FAIL'

	def dut_write_read(self,cmd='',seconds=0.5,num_of_bytes=1000):
		# print('Command Passed ->  '+ cmd)
		debugPrint('Command Passed ->  '+ cmd)
		try:
			dut_obj.write(cmd+'\n')
			time.sleep(seconds)
			res= dut_obj.read(num_of_bytes)
			debugPrint('Result Obtained')
			debugPrint('======================')
			# print(res)
			debugPrint(res)
			return res
		except Exception,e:
			print e.args
			print 'FAIL'
			return 'FAIL'
		
	def dut_access(self,dut_mgmt_ip='',dut_username='',dut_password=''):
		debugPrint('SSH Access to '+dut_mgmt_ip)
		global dut_obj
		if(1):			
			# os.system('taskkill /F /im ttermpro.exe;killall -9 minicom')
			dut_obj=serial.Serial(self.com_port,'115200',parity=serial.PARITY_NONE,bytesize=serial.EIGHTBITS,timeout=4)
			return 'SUCCESS'
		# except Exception,e:
			# err_args=e.args
			
			# if 10060 in err_args:
				# print 'CONNECT_FAIL'
				# debugPrint('CONNECT_FAIL')
				# return 'CONNECT_FAIL'
			# elif 10061 in err_args:
				# print 'CONNECT_FAIL'
				# debugPrint('CONNECT_FAIL')
				# return 'CONNECT_FAIL'
			# else:
				# print err_args
				# debugPrint(err_args)
				# print 'AUTH_FAIL'
				# debugPrint('AUTH_FAIL')
				# return 'AUTH_FAIL'

	#Load DUT
	def load_dut(self,standard='',channel='',bw='',streams='',reboot=0,release='',stbc='1',gi='LGI',coding='BCC',greenfield_mode='Mixed',preamble='LONG',test='rx'):
		debugPrint('Load DUT')
		global dbg_print
		prompt=0
		self.dut_write('\n')
		if(self.check_dut_load_issues()=='alive'):
			debugPrint('DUT is alive')
			self.dut_reboot()
		else:
			print 'DUT is stuck'
			debugPrint('DUT is stuck')
		debugPrint('Waiting for DUT to reboot')
		time.sleep(reboot_time)
		prompt=self.dut_login()
		self.dut_state_handle(prompt)
		self.load_release_files()
		self.set_dut_streams(streams=streams)	
		self.set_dut_production_mode_settings(standard=standard,ch=channel,stbc=stbc,bw=bw,gi=gi,coding=coding,greenfield_mode=greenfield_mode,preamble=preamble,test=test,action='only_enable')
		self.set_dut_channel(channel)
		self.set_dut_ibss(channel=channel)
		self.set_dut_rfconf(release)

	def init_dut(self,com_port='COM1',reboot=0,standard='',streams='2x2',channel='',bw='',stbc='1',gi='LGI',coding='BCC',greenfield_mode='Mixed',preamble='LONG',release='',test='rx',chain_sel='1'):	
		global chain_sel_cmd
		chain_sel_cmd=chain_sel
		debugPrint('Init DUT')
		status=self.dut_access()
		debugPrint(status)
		# printstatus
		if(status=='AUTH_FAIL' or status=='CONNECT_FAIL'):
			status=self.dut_access()
			if(status=='AUTH_FAIL' or status=='CONNECT_FAIL'):
				debugPrint('Script Execution stopped as SSH to DUT failed after reboot')
				print 'Script Execution stopped as SSH to DUT failed after reboot'
				exit(0)
		# self.get_stats_path()
		# status=self.load_release_files()
		# self.set_dut_streams(streams=streams)
		# self.set_dut_production_mode_settings(standard=standard,ch=channel,bw=bw,stbc=stbc,gi=gi,coding=coding,greenfield_mode=greenfield_mode,preamble=preamble,test=test,action='only_enable')
		# # res=self.set_dut_channel(channel)
		# if('rx' not in test):
			# self.set_dut_rfconf(release)
		# self.dut_down_up(action='up_down',ch=channel)

	def dut_close(self):
		debugPrint('DUT SSH Session Close')
		dut_obj.close()		
		time.sleep(4)
