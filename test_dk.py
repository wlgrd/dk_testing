from operator import itemgetter
import os
import sys
sys.path.insert(0, 'dut_config_files/')
sys.path.insert(0, 'equipment_config_files/')
from dut_details import *
from equipment_details import *
from commonUtils import *
from input_conf import *

def get_optimal_xo():
    standard = '11g'
    ch = '14'
    channel = '14'
    bw = '20'
    streams = '1x1'
    freq='2.4GHz'    
    data_rate=dr=dtr='6'    
    txp=10
    start_xo=0
    mid_xo=64
    end_xo=127
    xo_list = range(start_xo, end_xo)
    first = 0 
    if end_xo % 2 == 0:
        mid_xo = end_xo/2
    else:
        mid_xo = (end_xo+1)/2
    found = 0 
    xo_list = [start_xo, mid_xo, end_xo]
    xo_val_dict = {}
    fout = open('xo_val_board_'+board_num+'.txt', 'w')
    dut.set_dut_production_mode_settings(standard=standard,ch=ch,bw=bw,test='tx')
    dut.set_dut_channel(ch)
    dut.set_dut_datarate(dr,standard)
    dut.pktgen_tool('run')
    cable_loss_1x1=cable_loss_2x2=cable_loss_dict['1x1'][ch]+pcb_loss_dict[bw][ch]+attenuation
    equipment.init_vsa_funcs(standard=standard)
    while True :
        for xo_val in xo_list:
            if xo_val in xo_val_dict.keys():
                continue
            xo_to_set = hex(xo_val).zfill(2).replace('0x','')
            dut.set_dut_xo(str(xo_to_set))
            equipment.apply_vsa(ch,bw,streams)
            return_data=get_tx_stats_from_vsa(txp,dtr,ch,streams,standard,bw,equipment,cable_loss_1x1,cable_loss_2x2)
            sys_clk_err = abs(return_data[6])
            if -0.5 <= sys_clk_err <= 0.5:
            # if 0 == sys_clk_err:
                found = 1
                break
            else:
                xo_val_dict[xo_val] = sys_clk_err
        if found ==1 or len(list(set(xo_list)))==2:
            optimal_xo = hex(min(xo_val_dict, key=xo_val_dict.get)).zfill(2).replace('0x','')
            print "Found Optimal XO : "+str(optimal_xo)
            fout.write(optimal_xo)
            fout.close()
            return optimal_xo
        res = dict(sorted(xo_val_dict.items(), key=itemgetter(1))[:2])
        start_xo = min(res.keys())
        end_xo= max(res.keys())
        mid_xo = (start_xo+end_xo)/2
        xo_list = [start_xo, mid_xo, end_xo]

def run_tx_test(standard='11b', channel='1', data_rate='1'):
    dut.set_dut_channel(channel)
    dut.set_dut_datarate(data_rate, standard)
    dut.pktgen_tool('run')
    cable_loss_1x1=cable_loss_2x2=cable_loss_dict['1x1'][channel]+pcb_loss_dict["20"][channel]+attenuation
    equipment.init_vsa_funcs(standard=standard)
    equipment.set_vsa_modulation(standard)
    equipment.apply_vsa(channel,"20","1x1")
    return_data=get_tx_stats_from_vsa(10,data_rate,channel,"1x1",standard,"20",equipment,cable_loss_1x1,cable_loss_2x2)
    evm_1x1 =  return_data[3]
    spectral_mask_1x1 =  return_data[-1]
    if int(channel)<36 : band='2.4'
    else: band='5'
    if (float(evm_1x1) < float(standard_evm_dict[band][data_rate])):evm_status = "PASS"
    else : evm_status = "FAIL"
    print "\nStandard\t:\t"+standard+"\nData Rate\t:\t"+data_rate+"\nMeasured EVM\t:\t"+str(evm_1x1)+"\nEVM Stauts\t:\t"+evm_status+"\nSpectral Mask Status\t:\t"+spectral_mask_1x1

def run_rx_test(standard='11b', modulation="DSSS", channel='1', data_rate='1',payload='1024',amp="-50"):
    dut.set_dut_production_mode_settings(standard=standard,ch=channel,bw="20")
    dut.set_dut_channel(channel)
    equipment.init_vsg_funcs(standard=standard,bw="20",streams="1x1",payload=payload,chain_sel="1")    
    equipment.apply_vsg(bw="20",chn=int(channel),streams="1x1")
    equipment.set_macheader()
    equipment.set_payload(standard,payload)
    equipment.set_datarate(modulation,standard,data_rate)
    equipment.generate_waveform(streams="1x1")
    equipment.set_amplitude("1x1",amp)
    data = start_per(modulation,data_rate,channel,"1x1",standard,tester,dut,equipment)
    print data

if __name__ == "__main__":
    op_file_path=build_results_path(release=release)
    dut=eval(dutModel.upper())(com_port)    
    equipment=eval(tester.split('_')[0])(tester)
    equipment.start_vsg()
    dut.init_dut(release=release,test='tx')
    get_optimal_xo()
    run_tx_test(standard='11b', channel='1', data_rate='1')
    run_tx_test(standard='11b', channel='1', data_rate='11')
    run_tx_test(standard='11n', channel='36', data_rate='MCS0')
    run_tx_test(standard='11n', channel='36', data_rate='MCS7')
    run_tx_test(standard='11n', channel='149', data_rate='MCS0')
    run_tx_test(standard='11n', channel='149', data_rate='MCS7')
    run_rx_test(standard='11b', modulation="DSSS", channel='1', data_rate='1',payload='1024',amp="-50")
    run_rx_test(standard='11b', modulation="DSSS", channel='1', data_rate='11',payload='1024',amp="-50")
    run_rx_test(standard='11n', modulation="OFDM", channel='36', data_rate='MCS0',payload='1024',amp="-50")
    run_rx_test(standard='11n', modulation="OFDM", channel='36', data_rate='MCS7',payload='1024',amp="-50")
    run_rx_test(standard='11n', modulation="OFDM", channel='149', data_rate='MCS0',payload='1024',amp="-50")
    run_rx_test(standard='11n', modulation="OFDM", channel='149', data_rate='MCS7',payload='1024',amp="-50")    