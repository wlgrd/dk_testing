#-------------------------------------------------------------------------------
# Name:		   commonUtils
# Purpose:	  All the functions which are common are listed in this module
# Author:	   Imagination Technologies Ltd
# Copyright:   Imagination Technologies Ltd
#-------------------------------------------------------------------------------
import time
import re
import os
import sys
import xlsxwriter
import numpy
import telnetlib
import subprocess
import matplotlib
import paramiko
import serial
import openpyxl
import shutil
from bisect import *
import numpy as np
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from commands import *
from docx import *
from docx.shared import Inches
sys.path.insert(0, 'dut_config_files/')
sys.path.insert(0, 'equipment_config_files/')
from input_conf import *

standard_evm_dict={
	'2.4':
	{
		'1':'-9','2':'-9','5.5':'-9','11':'-9',
		'6':'-5','9':'-8','12':'-10','18':'-13','24':'-16','36':'-19','48':'-22','54':'-25',
		'MCS0':'-5','MCS1':'-10','MCS2':'-13','MCS3':'-16','MCS4':'-19','MCS5':'-22','MCS6':'-25','MCS7':'-27',
		'MCS8':'-5','MCS9':'-10','MCS10':'-13','MCS11':'-16','MCS12':'-19','MCS13':'-22','MCS14':'-25','MCS15':'-27',
	},
	'5':
	{
		'6':'-5','9':'-8','12':'-10','18':'-13','24':'-16','36':'-19','48':'-22','54':'-25',
		'MCS0':'-5','MCS1':'-10','MCS2':'-13','MCS3':'-16','MCS4':'-19','MCS5':'-22','MCS6':'-25','MCS7':'-27','MCS8':'-30','MCS9':'-32'
	}
}

best_evm_power_byte_location={
	'2.4':
		{
		'11b':{
				'20':{'1':'211','2':'212','5.5':'213','11':'214'}
			},
		'11g':{
				'20':{'9':'216'}
			},
		'11n':{
				'20':{'MCS0':'215','MCS1':'217','MCS2':'218','MCS3':'219','MCS4':'220','MCS5':'221','MCS6':'222','MCS7':'223'},
				'40':{'MCS0':'228','MCS1':'230','MCS2':'231','MCS3':'232','MCS4':'233','MCS5':'234','MCS6':'235','MCS7':'236'}
			}
		},
	'5':{	
		'11a':{
				'20':{'9':'238'}
			},
		'11n':{
				'20':{'MCS0':'237','MCS1':'238','MCS2':'239','MCS3':'240','MCS4':'241','MCS5':'242','MCS6':'243','MCS7':'244'},
				'40':{'MCS0':'248','MCS1':'249','MCS2':'250','MCS3':'251','MCS4':'252','MCS5':'253','MCS6':'254','MCS7':'255'}
			},
		'11ac':
			{	
				'20':{'MCS0':'237','MCS1':'239','MCS2':'240','MCS3':'241','MCS4':'242','MCS5':'243','MCS6':'244','MCS7':'245','MCS8':'246','MCS9':'247'},
				'40':{'MCS0':'248','MCS1':'250','MCS2':'251','MCS3':'252','MCS4':'253','MCS5':'254','MCS6':'255','MCS7':'256','MCS8':'257','MCS9':'258'},
				'80':{'MCS0':'259','MCS1':'261','MCS2':'262','MCS3':'263','MCS4':'264','MCS5':'265','MCS6':'266','MCS7':'267','MCS8':'268','MCS9':'269'}
			}
		}
	}

prime_20_sec_20_flags_dict={
							'20in40':{
								'1':'r','2':'r','3':'r','4':'r',
								'36':'r','44':'r',
								'52':'r','60':'r',
								'100':'r','108':'r',
								'116':'r','124':'r',
								'132':'r','140':'r',
								'149':'r','157':'r',
								},
							'40':{
								'1':'r','2':'r','3':'r','4':'r',
								'36':'r','44':'r',
								'52':'r','60':'r',
								'100':'r','108':'r',
								'116':'r','124':'r',
								'132':'r','140':'r',
								'149':'r','157':'r',
								},
							'80':{'36':'r','40':'lr','44':'rl','48':'l',
								'52':'r','56':'lr','60':'rl','64':'l',
								'100':'r','104':'lr','108':'rl','112':'l',
								'116':'r','120':'lr','124':'rl','128':'l',
								'132':'r','136':'lr','140':'rl','144':'l',
								'149':'r','153':'lr','157':'rl','161':'l'
								},
							'20in80':{'36':'r','40':'lr','44':'rl','48':'l',
								'52':'r','56':'lr','60':'rl','64':'l',
								'100':'r','104':'lr','108':'rl','112':'l',
								'116':'r','120':'lr','124':'rl','128':'l',
								'132':'r','136':'lr','140':'rl','144':'l',
								'149':'r','153':'lr','157':'rl','161':'l'
								}
							}
prod_mode_flag_dict={
					'11n':{'20':{'sgi':'12','lgi':'8'},'40':{'sgi':'14','lgi':'10'}},
					'11ac':{'20':{'sgi':'20','lgi':'16'},'40':{'sgi':'22','lgi':'18'},'80':{'sgi':'52','lgi':'48'}}	
					}							
sensitivity_dict_range={
					'11ac':{
							'1x1':{
									'20':{
										'MCS0':[-85,-95],'MCS1':[-80,-90],'MCS2':[-80,-90],'MCS3':[-80,-90],
										'MCS4':[-70,-90],'MCS5':[-70,-80],'MCS6':[-70,-80],'MCS7':[-70,-80],
										'MCS8':[-60,-70]
										},
									'40':{
										'MCS0':[-80,-90],'MCS1':[-80,-90],'MCS2':[-80,-90],'MCS3':[-70,-90],
										'MCS4':[-70,-80],'MCS5':[-70,-80],'MCS6':[-70,-80],'MCS7':[-60,-80],
										'MCS8':[-60,-70],'MCS9':[-50,-70]
										},
									'80':{
										'MCS0':[-70,-90],'MCS1':[-70,-90],'MCS2':[-70,-90],'MCS3':[-70,-80],
										'MCS4':[-70,-80],'MCS5':[-60,-70],'MCS6':[-60,-70],'MCS7':[-60,-70],
										'MCS8':[-50,-60],'MCS9':[-50,-60]
										}
									},
							'2x2':{
									'20':{
										'MCS0':[-80,-90],'MCS1':[-80,-90],'MCS2':[-80,-90],'MCS3':[-80,-90],
										'MCS4':[-70,-90],'MCS5':[-60,-80],'MCS6':[-60,-80],'MCS7':[-60,-80],
										'MCS8':[-50,-70]
										},
									'40':{
										'MCS0':[-80,-90],'MCS1':[-80,-90],'MCS2':[-80,-90],'MCS3':[-70,-90],
										'MCS4':[-70,-90],'MCS5':[-70,-80],'MCS6':[-70,-80],'MCS7':[-60,-70],
										'MCS8':[-50,-70],'MCS9':[-50,-70]
										},
									'80':{
										'MCS0':[-70,-90],'MCS1':[-70,-90],'MCS2':[-70,-90],'MCS3':[-70,-80],
										'MCS4':[-70,-80],'MCS5':[-60,-70],'MCS6':[-60,-70],'MCS7':[-60,-70],
										'MCS8':[-50,-60],'MCS9':[-50,-60]
										}
									}		
							},
					'11n':{
							'1x1':{
								'20':{
									'MCS0':[-85,-95],'MCS1':[-70,-90],'MCS2':[-80,-90],'MCS3':[-70,-80],
									'MCS4':[-70,-90],'MCS5':[-70,-80],'MCS6':[-70,-80],'MCS7':[-60,-80],
									},
								'40':{
									'MCS0':[-80,-90],'MCS1':[-80,-90],'MCS2':[-80,-90],'MCS3':[-70,-80],
									'MCS4':[-70,-80],'MCS5':[-60,-80],'MCS6':[-60,-80],'MCS7':[-60,-80]
									}
								},
								'2x2':{
								'20':{
									'MCS8':[-80,-90],'MCS9':[-70,-90],'MCS10':[-70,-90],'MCS11':[-70,-80],
									'MCS12':[-70,-90],'MCS13':[-70,-80],'MCS14':[-70,-80],'MCS15':[-60,-70],
									},
								'40':{
									'MCS8':[-80,-90],'MCS9':[-80,-90],'MCS10':[-80,-90],'MCS11':[-70,-80],
									'MCS12':[-70,-80],'MCS13':[-60,-80],'MCS14':[-60,-80],'MCS15':[-60,-80]
									}
								}
						},
					'11b':{
						'1x1':{
							'20':{
								'1':[-80,-100],'2':[-80,-100],'5.5':[-80,-100],'11':[-80,-90]
								}
							}
						},	
					'11g':{
						'1x1':{
							'20':{
								'6':[-85,-95],'9':[-80,-90],'12':[-80,-90],'18':[-80,-90],
								'24':[-70,-90],'36':[-70,-90],'48':[-70,-80],'54':[-70,-80]
								}
							}
						},
					'11a':{
						'1x1':{
							'20':{
								'6':[-85,-95],'9':[-80,-90],'12':[-80,-90],'18':[-80,-90],
								'24':[-70,-90],'36':[-70,-90],'48':[-70,-80],'54':[-70,-80]
								}
							}
						}							
				}					

snr_dict_range={
					'11ac':{
							'1x1':{
									'20':{
										'MCS0':[-40,35],'MCS1':[-40,35],'MCS2':[-40,35],'MCS3':[-40,35],
										'MCS4':[-40,35],'MCS5':[-40,35],'MCS6':[-40,35],'MCS7':[-40,35],
										'MCS8':[-40,35]
										},
									'40':{
										'MCS0':[-40,35],'MCS1':[-40,35],'MCS2':[-40,35],'MCS3':[-40,35],
										'MCS4':[-40,35],'MCS5':[-40,35],'MCS6':[-40,35],'MCS7':[-40,35],
										'MCS8':[-40,35],'MCS9':[-40,35]
										},
									'80':{
										'MCS0':[-40,35],'MCS1':[-40,35],'MCS2':[-40,35],'MCS3':[-40,35],
										'MCS4':[-40,35],'MCS5':[-40,35],'MCS6':[-40,35],'MCS7':[-40,35],
										'MCS8':[-40,35],'MCS9':[-40,35]
										}
									},
							'2x2':{
									'20':{
										'MCS0':[-40,35],'MCS1':[-40,35],'MCS2':[-40,35],'MCS3':[-40,35],
										'MCS4':[-40,35],'MCS5':[-40,35],'MCS6':[-40,35],'MCS7':[-40,35],
										'MCS8':[-40,35]		
										},		
									'40':{		
										'MCS0':[-40,35],'MCS1':[-40,35],'MCS2':[-40,35],'MCS3':[-40,35],
										'MCS4':[-40,35],'MCS5':[-40,35],'MCS6':[-40,35],'MCS7':[-40,35],
										'MCS8':[-40,35],'MCS9':[-40,35]
										},		
									'80':{		
										'MCS0':[-40,35],'MCS1':[-40,35],'MCS2':[-40,35],'MCS3':[-40,35],
										'MCS4':[-40,35],'MCS5':[-40,35],'MCS6':[-40,35],'MCS7':[-40,35],
										'MCS8':[-40,35],'MCS9':[-40,40]
										}
									}		
							},
					'11n':{
							'1x1':{
								'20':{
									'MCS0':[-40,30],'MCS1':[-40,10],'MCS2':[-40,10],'MCS3':[-40,30],
									'MCS4':[-40,30],'MCS5':[-40,30],'MCS6':[-40,30],'MCS7':[-40,30],
									},	   
								'40':{	   
									'MCS0':[-40,30],'MCS1':[-40,30],'MCS2':[-40,30],'MCS3':[-40,30],
									'MCS4':[-40,30],'MCS5':[-40,30],'MCS6':[-40,30],'MCS7':[-40,30]
									}	   
								},		   
								'2x2':{	   
								'20':{	   
									'MCS8':[-40,30],'MCS9':[-40,30],'MCS10':[-40,30],'MCS11':[-40,30],
									'MCS12':[-40,30],'MCS13':[-40,30],'MCS14':[-40,30],'MCS15':[-40,30],
									},
								'40':{
									'MCS8':[-40,30],'MCS9':[-40,30],'MCS10':[-40,30],'MCS11':[-40,30],
									'MCS12':[-40,30],'MCS13':[-40,30],'MCS14':[-40,30],'MCS15':[-40,30]
									}
								}
						},
					'11b':{
						'1x1':{
							'20':{
								'1':[-40,30],'2':[-40,30],'5.5':[-40,30],'11':[-40,30]
								}
							}
						},	
					'11g':{
						'1x1':{
							'20':{
								'6':[-40,30],'9':[-40,30],'12':[-40,30],'18':[-40,30],
								'24':[-40,30],'36':[-40,30],'48':[-40,30],'54':[-40,30]
								}
							}
						},
					'11a':{
						'1x1':{
							'20':{
								'6':[-40,30],'9':[-40,30],'12':[-40,30],'18':[-40,30],
								'24':[-40,30],'36':[-40,30],'48':[-40,30],'54':[-40,30]
								}
							}
						}							
				}			

intf_dict_range={
					'11ac':{
							'1x1':{
									'20':{
										'MCS0':[-10,-60],'MCS1':[-10,-60],'MCS2':[-10,-60],'MCS3':[-10,-60],
										'MCS4':[-10,-60],'MCS5':[-10,-60],'MCS6':[-10,-60],'MCS7':[-10,-60],
										'MCS8':[-10,-70]
										},
									'40':{
										'MCS0':[-10,-60],'MCS1':[-10,-60],'MCS2':[-10,-60],'MCS3':[-10,-60],
										'MCS4':[-10,-60],'MCS5':[-10,-60],'MCS6':[-10,-60],'MCS7':[-10,-60],
										'MCS8':[-10,-70],'MCS9':[-10,-70]
										},
									'80':{
										'MCS0':[-10,-60],'MCS1':[-10,-60],'MCS2':[-10,-60],'MCS3':[-10,-60],
										'MCS4':[-10,-60],'MCS5':[-10,-60],'MCS6':[-10,-60],'MCS7':[-10,-60],
										'MCS8':[-10,-70],'MCS9':[-10,-70]
										}
									},
							'2x2':{
									'20':{
										'MCS0':[-80,-90],'MCS1':[-80,-90],'MCS2':[-80,-90],'MCS3':[-80,-90],
										'MCS4':[-70,-90],'MCS5':[-60,-80],'MCS6':[-60,-80],'MCS7':[-60,-80],
										'MCS8':[-50,-70]
										},
									'40':{
										'MCS0':[-80,-90],'MCS1':[-80,-90],'MCS2':[-80,-90],'MCS3':[-70,-90],
										'MCS4':[-70,-90],'MCS5':[-70,-80],'MCS6':[-70,-80],'MCS7':[-60,-70],
										'MCS8':[-50,-70],'MCS9':[-50,-70]
										},
									'80':{
										'MCS0':[-70,-90],'MCS1':[-70,-90],'MCS2':[-70,-90],'MCS3':[-70,-80],
										'MCS4':[-70,-80],'MCS5':[-60,-70],'MCS6':[-60,-70],'MCS7':[-60,-70],
										'MCS8':[-50,-60],'MCS9':[-50,-60]
										}
									}		
							},
					'11n':{
							'1x1':{
								'20':{
									'MCS0':[-10,-60],'MCS1':[-10,-60],'MCS2':[-10,-60],'MCS3':[-10,-60],
									'MCS4':[-10,-60],'MCS5':[-10,-60],'MCS6':[-10,-60],'MCS7':[-10,-60]
									},
								'40':{
									'MCS0':[-10,-60],'MCS1':[-10,-60],'MCS2':[-10,-60],'MCS3':[-10,-60],
									'MCS4':[-10,-60],'MCS5':[-10,-60],'MCS6':[-10,-60],'MCS7':[-10,-60]
									}
								},
								'2x2':{
								'20':{
									'MCS8':[-80,-90],'MCS9':[-70,-90],'MCS10':[-70,-90],'MCS11':[-70,-80],
									'MCS12':[-70,-90],'MCS13':[-70,-80],'MCS14':[-70,-80],'MCS15':[-60,-70]
									},
								'40':{
									'MCS8':[-80,-90],'MCS9':[-80,-90],'MCS10':[-80,-90],'MCS11':[-70,-80],
									'MCS12':[-70,-80],'MCS13':[-60,-80],'MCS14':[-60,-80],'MCS15':[-60,-80]
									}
								}
						},
					'11b':{
						'1x1':{
							'20':{
								'1':[-10,-60],'2':[-10,-60],'5.5':[-10,-60],'11':[-10,-60]
								}
							}
						},	
					'11g':{
						'1x1':{
							'20':{
								'6':[-10,-60],'9':[-10,-60],'12':[-10,-60],'18':[-10,-60],
								'24':[-10,-60],'36':[-10,-60],'48':[-10,-60],'54':[-10,-60]
								}
							}
						},
					'11a':{
						'1x1':{
							'20':{
								'6':[-10,-60],'9':[-10,-60],'12':[-10,-60],'18':[-10,-60],
								'24':[-10,-60],'36':[-10,-60],'48':[-10,-60],'54':[-10,-60]
								}
							}
						}							
				}		
sensitivity_dict={
		'36':{
			'20':{
				'MCS0':'-82.31','MCS1':'-79.03','MCS2':'-77','MCS3':'-74.19',
				'MCS4':'-71.06','MCS5':'-66.69','MCS6':'-65.13','MCS7':'-64.19',
				'MCS8':'-69.6',
				'6':'-82.94','9':'-81.84','12':'-79.66','18':'-77.7','24':'-74.5','36':'-71.53','48':'-67.47','54':'-66.06',
				}
				},
		'38':{
			'40':{
				'MCS0':'-79.81','MCS1':'-76.38','MCS2':'-74.03','MCS3':'-70.75',
				'MCS4':'-67.84','MCS5':'-63.25','MCS6':'-62.16','MCS7':'-60.75',
				'MCS8':'-66.5','MCS9':'-64.5'
				},
			'80':{
				'MCS0':'-85.25','MCS1':'-82.125','MCS2':'-80.875','MCS3':'-78.37',
				'MCS4':'-75.25','MCS5':'-70.87','MCS6':'-69.39','MCS7':'-67.71',
				'MCS8':'-61.5','MCS9':'-60.87'
				}	
		},
		'1':{
			'20':{
				'MCS0':'-82.36','MCS1':'-79.08','MCS2':'-77.05','MCS3':'-74.24',
				'MCS4':'-71.11','MCS5':'-66.74','MCS6':'-65.33','MCS7':'-64.24',
				'6':'-82.99','9':'-81.89','12':'-79.78','18':'-77.67','24':'-74.71','36':'-71.74','48':'-67.6','54':'-66.11',
				'1':'-86.74','2':'-84.86','5.5':'-84.86','11':'-79.55'

				},
			'40':{
				'MCS0':'-79.86','MCS1':'-76.42','MCS2':'-73.92','MCS3':'-70.96',
				'MCS4':'-63.98','MCS5':'-63.3','MCS6':'-62.05','MCS7':'-60.49'
				}
		}
		}

pop_pkt_ifs_dict=	{
		'20':{
			'11b_11a':64,'11b_11g':64,'11b_11n':136,'11b_11ac':128,'11b_11b':368,
			'11a_11a':396,'11a_11g':396,'11a_11n':468,'11a_11ac':460,'11a_11b':700,
			'11g_11a':396,'11g_11g':396,'11g_11n':468,'11g_11ac':460,'11g_11b':700,
			'11n_11a':320,'11n_11g':320,'11n_11n':392,'11n_11ac':384,'11n_11b':624,
			'11ac_11a':322,'11a_11g':322,'11ac_11n':404,'11ac_11ac':396,'11ac_11b':636
			},
		'40':{
			'11n_11n':404,'11n_11ac':396,
			'11ac_11n':408,'11ac_11ac':400
			},
		'80':{
			'11ac_11ac':400
			}
	}

def build_results_path(release='',standard='',streams='',freq='',bw='',data_rate='',stbc='',coding='',gi='',greenfield_mode='',preamble=''):
	global op_file_path
	op_file_path=os.getcwd()
	op_file_path=os.path.join(op_file_path,'Results')
	op_file_path=os.path.join(op_file_path,release)
	op_file_path=os.path.join(op_file_path,standard)
	if((standard=='11n') or (standard=='11ac')):
		op_file_path=os.path.join(op_file_path,streams)
		op_file_path=os.path.join(op_file_path,stbc)
		op_file_path=os.path.join(op_file_path,coding)
		op_file_path=os.path.join(op_file_path,gi)
	if(standard=='11n'):
		op_file_path=os.path.join(op_file_path,greenfield_mode)
	if(standard=='11b'):
		op_file_path=os.path.join(op_file_path,preamble)
	op_file_path=os.path.join(op_file_path,time.strftime("%d-%B-%Y_%H-%M-%S"))
	try:
		os.makedirs(op_file_path)
	except:
		pass
	return op_file_path

def copy_file(op_dr_file_path='',dutModel='',release='',standard='',streams='',stbc='',coding='',gi='',greenfield_mode='',preamble='',ch='',test='rx'):
	shared_location_path=os.getcwd()
	# shared_location_path='\\\\hbdc1'
	# shared_location_path='/hbdc1_wlan'
	#shared_location_path=os.path.join(shared_location_path,'Shared')
	# shared_location_path=os.path.join(shared_location_path,'WLAN')
	shared_location_path=os.path.join(shared_location_path,'Repository')
	shared_location_path=os.path.join(shared_location_path,dutModel.split('_')[0]+"_PHY_Results")
	if('rx' in test):
		shared_location_path=os.path.join(shared_location_path,"RX_Results")
	else:
		shared_location_path=os.path.join(shared_location_path,"TX_Results")
	shared_location_path=os.path.join(shared_location_path,release)
	if((ch!='') or ('All_Channels_Consolidated' in op_dr_file_path)):	
		shared_location_path=os.path.join(shared_location_path,standard)
		if((standard=='11n')or(standard=='11ac')):
			shared_location_path=os.path.join(shared_location_path,streams)
			shared_location_path=os.path.join(shared_location_path,stbc)
			shared_location_path=os.path.join(shared_location_path,coding)
			shared_location_path=os.path.join(shared_location_path,gi)
		if(standard=='11n'):	
			shared_location_path=os.path.join(shared_location_path,greenfield_mode)
		if(standard=='11b'):	
			shared_location_path=os.path.join(shared_location_path,preamble)
		if('All_Channels_Consolidated' not in op_dr_file_path):
			shared_location_path=os.path.join(shared_location_path,str(ch))		
			if('Consolidated' not in op_dr_file_path):
				shared_location_path=os.path.join(shared_location_path,'Individual')
	try:
		os.makedirs(shared_location_path)		
		shutil.copy(op_dr_file_path, shared_location_path)
	except Exception,E:
		pass

def debugPrint(string='',create='0'):
	if(create=='1'):
		global fdebug
	fdebug=open((os.path.join(op_file_path, 'debug.log')),'a')
	fdebug.write(str(string)+'\n')
	fdebug.close()

#Start PER
def start_per(modulation,dr,ch,streams,standard,tester,dut,equipment,wave_type='default'):
	return_data,per_status=dut.compute_per(modulation,dr,ch,streams,standard,tester,dut,equipment,wave_type)
	# print return_data,per_status
	if(per_status=='FAIL'):
		print return_data
		dut.set_dut_channel(ch=ch)
		time.sleep(3)
		equipment.send_packets(streams,'run',wave_type=wave_type)
		return_data,per_status=dut.compute_per(modulation,dr,ch,streams,standard,tester,dut,equipment,wave_type)
		print return_data,per_status
		if(per_status=='FAIL'):
			return_data[0]='LOCKUP'
	return "\nStandard\t:\t"+standard+"\nData Rate\t:\t"+dr+"\nMeasured PER%\t:\t"+str(return_data[-2])+"\nPER Stauts\t:\t"+per_status
	return return_data
	
def get_tx_stats_from_vsa(txp,dr,ch,streams,standard,bw,equipment,cable_loss_1x1,cable_loss_2x2):
	equipment.click_agc(standard,streams,ref_level=str(txp+12-cable_loss_1x1))	
	# equipment.click_agc(standard,streams)	
	equipment.click_analyser(standard,streams)
	for i in range(2):
		try:
			if('2x2' in streams):
				evm_1x1,evm_2x2,phaseerr_1x1,phaseerr_2x2,freq_error_1x1,freq_error_2x2,sysclkerr_1x1,sysclkerr_2x2,lo_leakage_1x1,lo_leakage_2x2,ampimb_1x1,ampimb_2x2,phaseimb_1x1,phaseimb_2x2=equipment.save_txquality_stats(dr,txp,ch,standard,streams)
				if('#10' in str(evm_1x1)):
					equipment.click_analyser(standard,streams)
					time.sleep(10)
					continue
				else:
					evm_1x1=round(float(evm_1x1),2)
					evm_2x2=round(float(evm_2x2),2)
					break
			else:
				evm_1x1,phaseerr_1x1,freq_error_1x1,sysclkerr_1x1,lo_leakage_1x1,ampimb_1x1,phaseimb_1x1=equipment.save_txquality_stats(dr,txp,ch,standard,streams)#CSV
				if('#' in str(evm_1x1)):
					equipment.click_analyser(standard,streams)
					#time.sleep(10)
					continue
				else:
					evm_1x1=round(float(evm_1x1),2)
					try:
						phaseerr_1x1=round(float(phaseerr_1x1),2)
					except:
						phaseerr_1x1=0
					try:
						freq_error_1x1=round(float(freq_error_1x1),2)
					except:
						freq_error_1x1=0
					try:
						sysclkerr_1x1=round(float(sysclkerr_1x1),2)
					except:
						sysclkerr_1x1=0
					try:
						lo_leakage_1x1=round(float(lo_leakage_1x1),2)
					except:
						lo_leakage_1x1=0
					try:
						ampimb_1x1=round(float(ampimb_1x1),2)
					except:
						ampimb_1x1=0
					try:
						phaseimb_1x1=round(float(phaseimb_1x1),2)
					except:
						phaseimb_1x1=0
					break
				
		except Exception,e:
			if('2x2' in streams):
				evm_1x1=evm_2x2='0'
			else:
				evm_1x1=phaseerr_1x1=freq_error_1x1=sysclkerr_1x1=lo_leakage_1x1=ampimb_1x1=phaseimb_1x1='0'
	
	try:
		obw_1x1=equipment.save_obw_values(standard,streams)	
	except Exception,e:
		obw_1x1='0'
	
	try:
		dr_1x1=equipment.save_datarate_values(standard,streams)	
	except Exception,e:
		dr_1x1='0'

	for i in range(5):
		equipment.click_agc(standard,streams,ref_level=str(txp+12-cable_loss_1x1))	
		# equipment.click_agc(standard,streams)	
		try:
			if('2x2' in streams):
				power_1x1,power_2x2=equipment.save_power_values(dr,txp,ch,standard,streams,cable_loss_1x1,cable_loss_2x2)
			else:
				power_1x1=equipment.save_power_values(dr,txp,ch,standard,streams,cable_loss_1x1,cable_loss_2x2)
			if(power_1x1 > 1000):
				equipment.click_analyser(standard,streams)
				time.sleep(3)
				continue
			else:
				break
		except Exception,e:
			power_1x1=0
			if('2x2' in streams):
				power_2x2=0	
	equipment.click_analyser(standard,streams)
	time.sleep(1)
	try:		
		spectral_mask_1x1 ,spectral_mask_2x2= equipment.save_spec_margins(standard,ch,bw)	
	except Exception,e:
		spectral_mask_1x1 = 'FAIL'
	try:		
		spectral_flatness_1x1,spectral_flatness_2x2 = equipment.save_ofdm_spec_flatness(standard)	
	except Exception,e:
		spectral_flatness_1x1 = 'FAIL'
	try:		
		psdu_crc_1x1,psdu_crc_2x2 = equipment.save_psdu_crc(standard,dr_1x1)	
	except Exception,e:
		psdu_crc_1x1 = 'FAIL'				
	tx_data=[]

	try:
		if(streams=='2x2'):
			tx_data+=[obw_1x1,dr_1x1,power_1x1,power_2x2,evm_1x1,evm_2x2,phaseerr_1x1,phaseerr_2x2,freq_error_1x1,freq_error_2x2,sysclkerr_1x1,sysclkerr_2x2,lo_leakage_1x1,lo_leakage_2x2,ampimb_1x1,ampimb_2x2,phaseimb_1x1,phaseimb_2x2,spectral_mask_1x1,spectral_mask_2x2,spectral_flatness_1x1,spectral_flatness_2x2,psdu_crc_1x1,psdu_crc_2x2]

		else:
			tx_data+=[obw_1x1,dr_1x1,power_1x1,evm_1x1,phaseerr_1x1,freq_error_1x1,sysclkerr_1x1,lo_leakage_1x1,ampimb_1x1,phaseimb_1x1,spectral_mask_1x1,spectral_flatness_1x1,psdu_crc_1x1]
	except Exception,e:				   
		if(streams=='2x2'):
			tx_data.append('0')
			tx_data.append('0')
			tx_data.append('0')
			tx_data.append('0')
		else:
			tx_data.append('0')
			tx_data.append('0')
			tx_data.append('0')
	return tx_data
	
def create_dut_equipment_objects(dutModel,com_port,tester):
	global dut
	global equipment
	dut=eval(dutModel)(com_port)	
	equipment=eval(tester.split('_')[0])(tester)	
	return dut,equipment
