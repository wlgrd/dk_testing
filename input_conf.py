#########################################
#Equipment used for testing
#EX:IQXEL_280,IQXEL_160,IQXEL_80,RnS
#########################################
tester='IQXEL_280'

#########################################
#Hostname/IP-Address of equipment(which ever is reachable)
#########################################
# tester_hostname='10.90.48.127'
tester_hostname='10.90.48.124'

#########################################
#DUT Mode Name
#EX:Donatello
#########################################
dutModel='nRF'

#########################################
#Com Port of DUT detected
#########################################
com_port='/dev/ttyACM1'

#########################################
#Release Name
#########################################
release='BIT_REL_1.0.6_REL_CALDER_5920692_C0'
release='PR_8493'

#########################################

#DUT Base Board Number
#########################################
board_num='VCU108_3'

#########################################
#DUT RF Board Number
#########################################
rf_num='ES3-2'

#########################################
#DUT Reboot Time
#########################################
reboot_time=6
#########################################
#DUT Reboot Time
#########################################
num_of_pkts_from_vsg=100

#########################################
#DUT Codescape Debug
#########################################
codescape_debug='no'

################################################################
#####################	SSH ACCESS	#########################
################################################################
#Below params are mandatory if execution of DUT is with SSH
dut_mgmt_ip='10.90.48.182'
# dut_mgmt_ip='10.90.48.178'
dut_username='root'
dut_password='root123'
dut_wlan_mac='0019f5060220'
base_addr='0xe1057'
#########################################
#Cable Loss of both the cables in the channels where production calibration is performed
# '24G_BAND':2, #All 2.4G Channels
# '5G_BAND1':2, #All 5G Channels from 36-52
# '5G_BAND2':2, #All 5G Channels from -108
# '5G_BAND3':2, #All 5G Channels from -132
# '5G_BAND4':2  #All 5G Channels from -165
#########################################


cable_loss_dict={'1x1':
					{ 
						'1':0.2,
						'2':0.2,
						'3':0.2,
						'4':0.2,
						'5':0.2,
						'6':0.2,
						'7':0.2,
						'8':0.2,
						'9':0.2,
						'10':0.2,
						'11':0.2,
						'12':0.2,
						'13':0.2,
						'14':0.2,
						'36':0.77,
						'38':0.77,
						'40':0.78,
						'44':0.83,
						'46':0.84,
						'48':0.86,
						'52':0.88,
						'54':0.86,
						'56':0.84,
						'60':0.82,
						'62':0.81,
						'64':0.79,
						'100':0.83,
						'102':0.84,
						'104':0.85,
						'108':0.88,
						'110':0.89,
						'112':0.9,
						'116':0.94,
						'118':0.92,
						'120':0.91,
						'124':0.97,
						'126':0.95,
						'128':0.94,
						'132':0.94,
						'134':0.95,
						'136':0.96,
						'140':1.01,
						'142':1.01,
						'144':1.01,
						'149':0.99,
						'151':0.98,
						'153':0.98,
						'157':0.96,
						'159':0.92,
						'161':0.91,
						'165':0.9
					},
				'2x2':
					{
						'1':0.41,
						'2':0.48,
						'3':0.42,
						'4':0.49,
						'5':0.44,
						'6':0.51,
						'7':0.47,
						'8':0.49,
						'9':0.48,
						'10':0.51,
						'11':0.49,
						'12':0.49,
						'13':0.5,
						'14':0.5,
						'36':0.77,
						'38':0.77,
						'40':0.78,
						'44':0.83,
						'46':0.84,
						'48':0.86,
						'52':0.88,
						'54':0.86,
						'56':0.84,
						'60':0.82,
						'62':0.81,
						'64':0.79,
						'100':0.83,
						'102':0.84,
						'104':0.85,
						'108':0.88,
						'110':0.89,
						'112':0.9,
						'116':0.94,
						'118':0.92,
						'120':0.91,
						'124':0.97,
						'126':0.95,
						'128':0.94,
						'132':0.94,
						'134':0.95,
						'136':0.96,
						'140':1.01,
						'142':1.01,
						'144':1.01,
						'149':0.99,
						'151':0.98,
						'153':0.98,
						'157':0.96,
						'159':0.92,
						'161':0.91,
						'165':0.9
					}
				}
pcb_loss_dict={'20':
					{
						'1':1.3,
						'2':1.3,
						'3':1.3,
						'3':1.3,
						'4':1.3,
						'5':1.3,
						'6':1.3,
						'7':1.3,
						'8':1.3,
						'9':1.3,
						'10':1.3,
						'11':1.3,
						'12':1.3,
						'13':1.3,
						'14':1.3,
						'14':1.3,
						'36':2.5,
						'38':2.5,
						'40':2.5,
						'44':2.5,
						'48':2.5,
						'52':2.5,
						'56':2.5,
						'60':2.5,
						'64':2.5,
						'100':2.5,
						'102':2.5,
						'104':2.5,
						'108':2.5,
						'112':2.5,
						'116':2.5,
						'120':2.5,
						'124':2.5,
						'128':2.5,
						'132':2.5,
						'136':2.5,
						'140':2.5,
						'144':2.5,
						'149':2.5,
						'153':2.5,
						'157':2.5,
						'161':2.5,
						'165':2.5
					},
				'40':
					{
						'1':0.6,
						'2':0.6,
						'3':0.6,
						'3':0.6,
						'4':0.6,
						'5':0.6,
						'6':0.6,
						'7':0.6,
						'8':0.6,
						'9':0.6,
						'10':0.6,
						'11':0.6,
						'12':0.6,
						'13':0.6,
						'14':0.6,
						'38':1.178,
						'46':1.172,
						'54':1.15,
						'62':1.13,
						'102':1.13,
						'110':1.155,
						'118':1.195,
						'126':1.22,
						'134':1.365,
						'142':1.5,
						'144':1.5,
						'151':1.675,
						'159':1.635
					}
				}

#########################################
#Splitter Loss
#########################################
splitter_loss_24G=4
splitter_loss_5G=3.8

attenuation=0
#########################################
#Debug Script
#########################################
debug_script='yes'
