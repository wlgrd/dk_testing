# -------------------------------------------------------------------------------
# Name:		   iqxel
# Purpose:	   This module has all the APIs(SCPI commands) for configurint Litepoint iQxel-160/280 VSG/VSA.
# Author:	   kranthi.kishore
# Created:	   14-06-2015
# Copyright:   Imagination Technologies Ltd
# -------------------------------------------------------------------------------
from socket import *
import time
from commonUtils import *
from input_conf import *

datarate_dict = {
    "11a": {
        "6": "MCS 0",
        "9": "MCS 1",
        "12": "MCS 2",
        "18": "MCS 3",
        "24": "MCS 4",
        "36": "MCS 5",
        "48": "MCS 6",
        "54": "MCS 7",
    },
    "11n": {
        "MCS0": "MCS 0",
        "MCS1": "MCS 1",
        "MCS2": "MCS 2",
        "MCS3": "MCS 3",
        "MCS4": "MCS 4",
        "MCS5": "MCS 5",
        "MCS6": "MCS 6",
        "MCS7": "MCS 7",
        "MCS8": "MCS 8",
        "MCS9": "MCS 9",
        "MCS10": "MCS 10",
        "MCS11": "MCS 11",
        "MCS12": "MCS 12",
        "MCS13": "MCS 13",
        "MCS14": "MCS 14",
        "MCS15": "MCS 15",
    },
    "11g": {
        "6": "MCS 0",
        "9": "MCS 1",
        "12": "MCS 2",
        "18": "MCS 3",
        "24": "MCS 4",
        "36": "MCS 5",
        "48": "MCS 6",
        "54": "MCS 7",
    },
    "11b": {"1": "DRAT RATE1", "2": "DRAT RATE2", "5.5": "DRAT RATE5_5", "11": "DRAT RATE11"},
    "11ac": {
        "MCS0": "MCS 0",
        "MCS1": "MCS 1",
        "MCS2": "MCS 2",
        "MCS3": "MCS 3",
        "MCS4": "MCS 4",
        "MCS5": "MCS 5",
        "MCS6": "MCS 6",
        "MCS7": "MCS 7",
        "MCS8": "MCS 8",
        "MCS9": "MCS 9",
        "MCS10": "MCS 10",
        "MCS11": "MCS 11",
        "MCS12": "MCS 12",
        "MCS13": "MCS 13",
        "MCS14": "MCS 14",
        "MCS15": "MCS 15",
    },
}


class IQXEL:
    def __init__(self, tester="iqxel_m4w"):
        self.tester = tester.split("_")[-1]
        self.hostName = tester_hostname
        self.port = 24000

    # Start VSG
    def start_vsg(self):
        # print "\nConfiguring ",self.tester
        debugPrint("\nConfiguring " + self.tester)
        global cntrl_sckt
        ADDR = (self.hostName, self.port)
        cntrl_sckt = socket(AF_INET, SOCK_STREAM)  # Create and
        cntrl_sckt.connect(ADDR)
        time.sleep(1)

    # Close VSG
    def close_vsg(self):
        debugPrint("Closing VSG")
        cntrl_sckt.close()
        time.sleep(1)

    def socket_send(self, msg):
        cntrl_sckt.sendall(msg.encode("UTF-8"))

    # 802.11a Initialization settings
    def config_11a(self):
        self.socket_send("CHAN1;WIFI;CONF:WAVE:STAN A\n")

    # 802.11b Initialization settings
    def config_11b(self):
        self.socket_send("CHAN1;WIFI;CONF:WAVE:STAN B\n")

    # 802.11g Initialization settings
    def config_11g(self):
        self.socket_send("CHAN1;WIFI;CONF:WAVE:STAN A\n")

    # 802.11n Initialization settings
    def config_11n(self):
        self.socket_send("CHAN1;WIFI;CONF:WAVE:STAN N\n")

    # 802.11ac Initialization settings
    def config_11ac(self):
        self.socket_send("CHAN1;WIFI;CONF:WAVE:STAN AC\n")

    # Set Default
    def set_equip_default(self):
        # print "\nSetting VSA to default"
        debugPrint("\nSetting VSA to default")
        self.socket_send("*RST\n")
        if self.tester.lower() == "280":
            self.socket_send("MROUT1;PORT:RES RF1A,OFF\n")
            self.socket_send("MROUT2;PORT:RES RF2A,OFF\n")
            self.socket_send("SYS;MVSA:DEL\n")
            self.socket_send("SYS;MVSG:DEL\n")
            self.socket_send("SYS;MROUT:DEL\n")
        elif self.tester.lower() == "160":
            self.socket_send("*RST\n")
            self.socket_send("MROUT1;PORT:RES RF1A,OFF\n")
            self.socket_send("MROUT2;PORT:RES RF2A,OFF\n")
            self.socket_send("SYS;MVSA:DEL\n")
            self.socket_send("SYS;MVSG:DEL\n")
            self.socket_send("SYS;MROUT:DEL\n")
        time.sleep(1)

    # Modulation Type
    def set_modulation(self, standard):
        # print"\nSetting "+standard+" in VSA"
        debugPrint("\nSetting " + standard + " in VSA")
        eval("self.config_" + standard + "()")

    # Setting Datarate
    def set_datarate(self, modulation, standard, data_rate):
        # print"\nSetting data rate ",data_rate
        debugPrint("\nSetting data rate " + data_rate)
        self.socket_send("CHAN1;WIFI;CONF:WAVE:" + modulation + ":" + datarate_dict[standard][data_rate] + "\n")

    # Setting Payload
    def set_payload(self, standard, payload):
        # print"\nSetting payload ",payload
        debugPrint("\nSetting payload " + str(payload))
        self.socket_send("CHAN1;WIFI;CONF:WAVE:PSDU:NBYT " + payload + "\n")

    # Setting MAC Header OFF
    def set_macheader(self):
        self.socket_send("CHAN1;WIFI;CONF:WAVE:PSDU:MACH OFF\n")

    # Setting Channel
    def apply_vsg(self, bw="", chn="", streams="2x2"):
        debugPrint("Applying VSG channel " + str(chn) + " and BW " + str(bw))
        if (bw == "20") or (bw == "20in40") or (bw == "20in80"):
            self.socket_send("CHAN1;WIFI;CONF:CHAN:IND1 " + str(chn) + "\n")
            self.socket_send("CHAN1;WIFI;CONF:CHAN:CBW 20000000\n")  # 20MHz
        elif bw == "40":
            if str(chn) in prime_20_sec_20_flags_dict[bw].keys():
                self.socket_send("CHAN1;WIFI;CONF:CHAN:IND1 " + str(chn) + "\n")  # For Plus
            else:
                self.socket_send("CHAN1;WIFI;CONF:CHAN:IND1 " + str(int(chn) - 4) + "\n")  # For Minus
            self.socket_send("CHAN1;WIFI;CONF:CHAN:CBW 40000000\n")  # 40MHz
        elif bw == "80":
            if prime_20_sec_20_flags_dict[bw][str(chn)] == "l":
                self.socket_send("CHAN1;WIFI;CONF:CHAN:IND1 " + str(int(chn) - 6) + "\n")  # For Minus
            elif prime_20_sec_20_flags_dict[bw][str(chn)] == "lr":
                self.socket_send("CHAN1;WIFI;CONF:CHAN:IND1 " + str(int(chn) + 2) + "\n")
            elif prime_20_sec_20_flags_dict[bw][str(chn)] == "rl":
                self.socket_send("CHAN1;WIFI;CONF:CHAN:IND1 " + str(int(chn) - 2) + "\n")
            elif prime_20_sec_20_flags_dict[bw][str(chn)] == "r":
                self.socket_send("CHAN1;WIFI;CONF:CHAN:IND1 " + str(int(chn) + 6) + "\n")  # For Plus
            self.socket_send("CHAN1;WIFI;CONF:CHAN:CBW 80000000\n")  # 80MHz
        if int(chn) < 20:
            self.socket_send("CHAN1;WIFI;CONF:BAND 2G4\n")
        else:
            self.socket_send("CHAN1;WIFI;CONF:BAND 5G\n")
        if streams == "1x1":
            self.socket_send("CHAN1;WIFI; HSET:ALL VSG1" + chain_sel_scpi_cmd + "\n")
        elif streams == "2x2":
            self.socket_send("CHAN1;WIFI; HSET:ALL MVSGALL\n")

    # Setting Amplitude
    def set_amplitude(self, streams, ampl):
        # print "\nSetting amplitude ",ampl
        debugPrint("\nSetting amplitude " + str(ampl))
        if streams == "1x1":
            self.socket_send("VSG1" + chain_sel_scpi_cmd + ";POW " + ampl + "\n")
        elif streams == "2x2":
            self.socket_send("MVSGALL;POW " + ampl + "\n")

    # Set Bandwidth 20/40 MHz
    def set_bandwidth(self, standard="", bw=""):
        debugPrint("Setting BW " + str(bw))
        if (bw == "20") or (bw == "20in40") or (bw == "20in80"):
            self.socket_send("CHAN1;WIFI;CONF:WAVE:OFDM:CBW 20000000\n")  # 20MHz
        elif bw == "40":
            self.socket_send("CHAN1;WIFI;CONF:WAVE:OFDM:CBW 40000000\n")  # 40MHz
        elif bw == "80":
            self.socket_send("CHAN1;WIFI;CONF:WAVE:OFDM:CBW 80000000\n")  # 80MHz

    # Setting Wavegap/Idle Interval
    def set_idleinterval(self, intv):
        # print"\nSetting interval ",intv
        debugPrint("\nSetting interval " + str(intv))
        self.socket_send("CHAN1;WIFI;CONF:WAVE:GAP " + str(float(intv) / 1000000) + "\n")

    # Set Spatial Streams
    def set_streams(self, standard, streams):
        # print"\nSetting streams ",streams
        debugPrint("\nSetting streams " + streams)
        if streams == "1x1":
            self.socket_send("CHAN1;WIFI;CONF:WAVE:OFDM:NSST 1\n")  # 1x1
        elif streams == "2x2":
            if standard == "11ac":
                self.socket_send("CHAN1;WIFI;CONF:WAVE:OFDM:NSST 2\n")  # 2x2

    # Set Guard Interval
    def set_guardinterval(self, gi):
        # print"\nSetting Guard Interval ",gi
        debugPrint("\nSetting Guard Interval " + gi)
        if gi.lower() == "sgi":
            self.socket_send("CHAN1;WIFI;CONF:WAVE:OFDM:SGI ON\n")  # SGI
        elif gi.lower() == "lgi":
            self.socket_send("CHAN1;WIFI;CONF:WAVE:OFDM:SGI OFF\n")  # LGI

    # Set STBC
    def set_stbc(self, stbc):
        # print"\nSetting STBC ",stbc
        debugPrint("\nSetting STBC " + stbc)
        self.socket_send("CHAN1;WIFI;CONF:WAVE:OFDM:STBC " + str(stbc)[-1] + "\n")

    # Set Coding Type
    def set_coding(self, coding):
        # print"\nSetting Coding Technique ",coding
        debugPrint("\nSetting Coding Technique " + coding)
        if coding.lower() == "ldpc":
            self.socket_send("CHAN1;WIFI;CONF:WAVE:OFDM:COD LDPC\n")  # LDPC
        elif coding.lower() == "bcc":
            self.socket_send("CHAN1;WIFI;CONF:WAVE:OFDM:COD BCC\n")  # BCC

    # Set Greenfield Mode
    def set_greenfield(self, greenfield_mode):
        # print"\nSetting Greenfield Mode ",greenfield_mode
        debugPrint("\nSetting Greenfield Mode " + greenfield_mode)
        if greenfield_mode.lower() == "greenfield":
            self.socket_send("CHAN1;WIFI;CONF:WAVE:OFDM:GRE ON\n")  # Greenfield
        elif greenfield_mode.lower() == "mixed":
            self.socket_send("CHAN1;WIFI;CONF:WAVE:OFDM:GRE OFF\n")  # Mixed

    # Set Preamble
    def set_preamble(self, preamble):
        # print"\nSetting preamble ",preamble
        debugPrint("\nSetting preamble " + preamble)
        if preamble.lower == "short":
            self.socket_send("CHAN1;WIFI;CONF:WAVE:DSSS:PRE SHORT\n")  # Short
        elif preamble.lower == "long":
            self.socket_send("CHAN1;WIFI;CONF:WAVE:DSSS:PRE LONG\n")  # Long

    # RF ON/OFF
    def rf_on_off(self, rf_state="on", streams="2x2"):
        # print "\nSetting RF ",rf_state
        debugPrint("\nSetting RF " + rf_state)
        if rf_state == "off":
            if streams == "1x1":
                self.socket_send("VSG1" + chain_sel_scpi_cmd + ";POW:STAT" + " " + "OFF\n")
            elif streams == "2x2":
                self.socket_send("MVSGALL;POW:STAT" + " " + "OFF\n")
        elif rf_state == "on":
            if streams == "1x1":
                self.socket_send("VSG1" + chain_sel_scpi_cmd + ";POW:STAT" + " " + "ON\n")
            elif streams == "2x2":
                self.socket_send("MVSGALL;POW:STAT" + " " + "ON\n")

    # Generate Waveform
    def generate_waveform(self, streams="2x2", count="2000"):
        # print"\nGenerating waveform "
        debugPrint("\nGenerating waveform ")
        # self.socket_send("CHAN1;WIFI\n")
        # self.socket_send('wave:gen:mmem "\//user/wf.iqvsg", "WIFI wave generation from GUI"\n')
        # return
        if streams == "1x1":
            # self.socket_send('*wai;VSG1 ;wave:load "\//user/wf.iqvsg";wave:exec on\n')
            self.socket_send("VSG1" + chain_sel_scpi_cmd + ";WLIS:COUN " + count + "\n")
            # self.socket_send('VSG1 ;wave:exec off;WLIST:WSEG1:DATA "\//user/wf.iqvsg";wlist:wseg1:save;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1\n')
        elif streams == "2x2":
            #
            self.socket_send("MVSGALL;WLIS:COUN " + count + "\n")
            # self.socket_send('MVSGALL ;wave:exec off;WLIST:WSEG1:DATA "\//user/wf.iqvsg";wlist:wseg1:save;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1\n')

    # Start Pumping
    def send_packets(self, streams="2x2", action="run", wave_type="default"):
        # print 'Start Pumping'
        debugPrint("Start Pumping")
        self.rf_on_off(rf_state="on", streams=streams)
        if wave_type == "default":
            self.socket_send("CHAN1;WIFI\n")
            # self.socket_send('wave:gen:mmem "\//user/wf.iqvsg", "WIFI wave generation from GUI"\n')
            self.socket_send('wave:gen:mmem "/user/wf.iqvsg", "WIFI wave generation from GUI"\n')
            if action == "run":
                if streams == "1x1":
                    self.socket_send("VSG1" + chain_sel_scpi_cmd + ";WLIS:COUN " + str(num_of_pkts_from_vsg) + "\n")
                    self.socket_send("*wai;VSG1" + chain_sel_scpi_cmd + ' ;wave:load "/user/wf.iqvsg";wave:exec on\n')
                    # self.socket_send('*wai;VSG1'+chain_sel_scpi_cmd+' ;wave:load "\//user/wf.iqvsg";wave:exec on\n')
                    self.socket_send(
                        "VSG1"
                        + chain_sel_scpi_cmd
                        + ' ;wave:exec off;WLIST:WSEG1:DATA "/user/wf.iqvsg";wlist:wseg1:save;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1\n'
                    )
                elif streams == "2x2":
                    self.socket_send("MVSGALL;WLIS:COUN " + str(num_of_pkts_from_vsg) + "\n")
                    self.socket_send('*wai;MVSGALL ;wave:load "/user/wf.iqvsg";wave:exec on\n')
                    # self.socket_send('*wai;MVSGALL ;wave:load "\//user/wf.iqvsg";wave:exec on\n')
                    self.socket_send(
                        'MVSGALL ;wave:exec off;WLIST:WSEG1:DATA "/user/wf.iqvsg";wlist:wseg1:save;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1\n'
                    )
                    # self.socket_send('MVSGALL ;wave:exec off;WLIST:WSEG1:DATA "\//user/wf.iqvsg";wlist:wseg1:save;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1\n')
            elif action == "disable":
                if streams == "1x1":
                    self.socket_send("VSG1" + chain_sel_scpi_cmd + "; WAVE:EXEC OFF;WLIST:COUNT:DISABLE WSEG1\n")
                elif streams == "2x2":
                    self.socket_send("MVSGALL; WAVE:EXEC OFF;WLIST:COUNT:DISABLE WSEG1\n")
        else:
            self.load_degrade_waveform(streams=streams, action=action)

    # Set RF Port on VSA
    def set_rf(self, streams="2x2", test="rx", chain_sel="1"):
        global chain_sel_scpi_cmd
        chain_sel_scpi_cmd = ""
        # print'Setting RF Port in ',self.tester
        debugPrint("Setting RF Port in " + self.tester)
        if test == "rx":
            if self.tester.lower() == "80":
                if streams == "1x1":
                    if chain_sel == "1":
                        self.socket_send("ROUT1;PORT:RES RF1,VSG1\n")  # RF1
                    elif chain_sel == "2":
                        self.socket_send("ROUT1;PORT:RES RF2,VSG1\n")  # RF1
            elif self.tester.lower() == "160":
                if streams == "1x1":
                    self.socket_send("ROUT1;PORT:RES RF1A,VSG11\n")  # RF1
                elif streams == "2x2":
                    self.socket_send("MVSG:DEF:ADD VSG11\n")  # RF1
                    self.socket_send("MVSG:DEF:ADD VSG12\n")  # RF2
                    self.socket_send("MROUT:DEF:ADD ROUT11\n")
                    self.socket_send("MROUT:DEF:ADD ROUT12\n")  # Adding Module
                    time.sleep(2)
                    self.socket_send("MROUT1;PORT:RES RF1A,VSG11\n")  # Adding Module
                    self.socket_send("MROUT2;PORT:RES RF2A,VSG12\n")

            elif self.tester.lower() == "280":
                if streams == "1x1":
                    if chain_sel == "1":
                        self.socket_send("ROUT1;PORT:RES RF1A,VSG11\n")  # RF1
                    elif chain_sel == "2":
                        self.socket_send("ROUT12;PORT:RES RF1B,VSG12\n")  # RF1
                        chain_sel_scpi_cmd = chain_sel
                elif streams == "2x2":
                    self.socket_send("MVSG:DEF:ADD VSG11\n")  # RF1
                    self.socket_send("MVSG:DEF:ADD VSG12\n")  # RF2
                    self.socket_send("MROUT:DEF:ADD ROUT11\n")
                    self.socket_send("MROUT:DEF:ADD ROUT12\n")  # Adding Module
                    time.sleep(2)
                    self.socket_send("MROUT1;PORT:RES RF1B,VSG12\n")  # Adding Module
                    self.socket_send("MROUT2;PORT:RES RF1A,VSG11\n")
                    self.socket_send("MROUT1;PORT:RES RF1A,VSG11\n")
                    self.socket_send("MROUT2;PORT:RES RF1B,VSG12\n")
        elif test == "tx":
            if self.tester.lower() == "80":
                if streams == "1x1":
                    if chain_sel == "1":
                        self.socket_send("ROUT1;PORT:RES RF1,VSA1\n")  # RF1
                    elif chain_sel == "2":
                        self.socket_send("ROUT1;PORT:RES RF2,VSA1\n")  # RF1
            elif self.tester.lower() == "160":
                if streams == "1x1":
                    if chain_sel == "1":
                        self.socket_send("ROUT1;PORT:RES RF1A,VSA11\n")  # RF1
                    elif chain_sel == "2":
                        self.socket_send("ROUT12;PORT:RES RF1B,VSA12\n")  # RF1
                elif streams == "2x2":
                    self.socket_send("MVSA:DEF:ADD VSA11\n")  # RF1
                    self.socket_send("MVSA:DEF:ADD VSA12\n")  # RF2
                    self.socket_send("MROUT:DEF:ADD ROUT11\n")  # ADD ROUT11
                    self.socket_send("MROUT:DEF:ADD ROUT12\n")  # Adding Module
                    time.sleep(2)
                    self.socket_send("MROUT2;PORT:RES RF2A,VSA12\n")
                    self.socket_send("MROUT1;PORT:RES RF1A,VSA11\n")
            elif self.tester.lower() == "280":
                if streams == "1x1":
                    if chain_sel == "1":
                        self.socket_send("ROUT1;PORT:RES RF1A,VSA11\n")  # RF1
                    elif chain_sel == "2":
                        self.socket_send("ROUT12;PORT:RES RF1B,VSA12\n")  # RF1
                        chain_sel_scpi_cmd = chain_sel
                elif streams == "2x2":
                    self.socket_send("MVSA:DEF:ADD VSA11\n")  # RF1
                    self.socket_send("MVSA:DEF:ADD VSA12\n")  # RF2
                    self.socket_send("MROUT:DEF:ADD ROUT11\n")
                    self.socket_send("MROUT:DEF:ADD ROUT12\n")  # Adding Module
                    time.sleep(2)
                    self.socket_send("MROUT1;PORT:RES RF1B,VSA12\n")  # Adding Module
                    self.socket_send("MROUT2;PORT:RES RF1A,VSA11\n")
                    self.socket_send("MROUT1;PORT:RES RF1A,VSA11\n")
                    self.socket_send("MROUT2;PORT:RES RF1B,VSA12\n")

    def generate_degrade_waveform(self, awgn_snr="200", bw="20", standard="11n", dr="MCS7"):
        # print 'Generating noise wave'
        self.socket_send("CHAN1;GPRF;WAVE:DEGR:AWGN:SBW " + bw + "000000\n")
        self.socket_send("CHAN1;WIFI\n")

        self.socket_send('wave:gen:mmem "/user/wf.iqvsg", "WIFI wave generation from GUI"\n')
        self.socket_send("CHAN1;GPRF;WAVE:DEGR:AWGN:SNR (" + awgn_snr + 7 * ("," + awgn_snr) + ")\n")
        self.socket_send('GPRF;WAVE:DEGR:APPL "\\User\\wf_degrade.iqvsg","\\user/wf.iqvsg"\n')

    def load_degrade_waveform(self, streams="2x2", action="run"):
        # print 'Loading noise wave'
        if streams == "1x1":
            self.socket_send('VSG1; WAVE:LOAD "/user/wf_degrade.iqvsg"\n')
        elif streams == "2x2":
            self.socket_send('MVSGALL; WAVE:LOAD "/user/wf_degrade.iqvsg"\n')

        if action == "run":
            if streams == "1x1":
                # VSG1 ;wave:exec off;WLIST:WSEG1:DATA "/user/deg.iqvsg";wlist:wseg1:save;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1

                self.socket_send("VSG1" + chain_sel_scpi_cmd + ";WLIS:COUN 2000\n")
                self.socket_send(
                    "*wai;VSG1" + chain_sel_scpi_cmd + ' ;wave:load "\//user/wf_degrade.iqvsg";wave:exec on\n'
                )
                self.socket_send(
                    "VSG1"
                    + chain_sel_scpi_cmd
                    + ' ;wave:exec off;WLIST:WSEG1:DATA "\//user/wf_degrade.iqvsg";wlist:wseg1:save;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1\n'
                )
            elif streams == "2x2":
                self.socket_send("MVSGALL;WLIS:COUN 2000\n")
                self.socket_send('*wai;MVSGALL ;wave:load "\//user/wf_degrade.iqvsg";wave:exec on\n')
                self.socket_send(
                    'MVSGALL ;wave:exec off;WLIST:WSEG1:DATA "\//user/wf_degrade.iqvsg";wlist:wseg1:save;WLIST:COUNT:ENABLE WSEG1;WAVE:EXEC ON, WSEG1\n'
                )
        elif action == "disable":
            if streams == "1x1":
                self.socket_send("VSG1" + chain_sel_scpi_cmd + "; WAVE:EXEC OFF;WLIST:COUNT:DISABLE WSEG1\n")
            elif streams == "2x2":
                self.socket_send("MVSGALL; WAVE:EXEC OFF;WLIST:COUNT:DISABLE WSEG1\n")

    def init_vsg_funcs(
        self,
        standard="11ac",
        bw="20",
        streams="2x2",
        stbc="STBC_0",
        gi="LGI",
        coding="BCC",
        greenfield_mode="Mixed",
        preamble="LONG",
        payload="1024",
        test="rx",
        chain_sel="1",
    ):
        self.start_vsg()
        self.set_equip_default()
        self.set_rf(streams=streams, test=test, chain_sel=chain_sel)
        self.set_modulation(standard)
        self.set_bandwidth(bw=bw, standard=standard)
        self.set_idleinterval(100)
        if (standard == "11n") or (standard == "11ac"):
            self.set_streams(standard, streams)
            self.set_stbc(stbc)
            self.set_guardinterval(gi)
            self.set_coding(coding)
        if standard == "11n":
            self.set_greenfield(greenfield_mode)
        if standard == "11b":
            self.set_preamble(preamble)
        self.generate_waveform(streams=streams)
        self.rf_on_off(rf_state="on", streams=streams)

    # Modulation Type
    def set_vsa_modulation(self, standard):
        debugPrint("Setting VSA Modulation as " + modulation)
        if standard == "11b":
            modulation = "dsss"
        else:
            modulation = "ofdm"
        # print "\nSetting "+modulation+" in VSA"
        self.socket_send("CHAN1;WIFI;CONF:STAN " + modulation.upper() + "\n")
        if standard == "11b":
            self.socket_send("CHAN1;WIFI;CONF:STAN DSSS\n")

    # Setting Capture Length
    def set_capturelength(self, len, streams):
        # print "\nSetting interval ",len
        debugPrint("\nSetting interval " + str(len))
        if streams == "1x1":
            self.socket_send("VSA1" + chain_sel_scpi_cmd + ";CAPT:TIME " + str(float(len) / 1000) + "\n")
        elif streams == "2x2":
            self.socket_send("MVSAALL;CAPT:TIME " + str(float(len) / 1000) + "\n")

    # Apply to VSA
    def apply_vsa(self, chn="", bw="", streams="2x2", chain_sel_scpi_cmd="1"):
        # print "\nApply settings to VSA",chn
        debugPrint("\nApply settings to VSA" + str(chn))
        if bw == "20":
            self.socket_send("CHAN1;WIFI;CONF:CHAN:IND1 " + str(chn) + "\n")
            self.socket_send("CHAN1;WIFI;CONF:CHAN:CBW 20000000\n")  # 20MHz
        elif bw == "40":
            if str(chn) in prime_20_sec_20_flags_dict[bw].keys():
                self.socket_send("CHAN1;WIFI;CONF:CHAN:IND1 " + str(chn) + "\n")  # For Plus
            else:
                self.socket_send("CHAN1;WIFI;CONF:CHAN:IND1 " + str(int(chn) - 4) + "\n")  # For Minus
            self.socket_send("CHAN1;WIFI;CONF:CHAN:CBW 40000000\n")  # 40MHz
        elif bw == "80":
            if prime_20_sec_20_flags_dict[bw][str(chn)] == "l":
                self.socket_send("CHAN1;WIFI;CONF:CHAN:IND1 " + str(int(chn) - 6) + "\n")  # For Minus
            elif prime_20_sec_20_flags_dict[bw][str(chn)] == "lr":
                self.socket_send("CHAN1;WIFI;CONF:CHAN:IND1 " + str(int(chn) + 2) + "\n")
            elif prime_20_sec_20_flags_dict[bw][str(chn)] == "rl":
                self.socket_send("CHAN1;WIFI;CONF:CHAN:IND1 " + str(int(chn) - 2) + "\n")
            elif prime_20_sec_20_flags_dict[bw][str(chn)] == "r":
                self.socket_send("CHAN1;WIFI;CONF:CHAN:IND1 " + str(int(chn) + 6) + "\n")  # For Plus
            self.socket_send("CHAN1;WIFI;CONF:CHAN:CBW 80000000\n")  # 80MHz
        if int(chn) < 20:
            self.socket_send("CHAN1;WIFI;CONF:BAND 2G4\n")
        else:
            self.socket_send("CHAN1;WIFI;CONF:BAND 5G\n")
        if streams == "1x1":
            self.socket_send("CHAN1;WIFI; HSET:ALL VSA1" + chain_sel_scpi_cmd + "\n")
        elif streams == "2x2":
            self.socket_send("CHAN1;WIFI; HSET:ALL MVSAALL\n")

    # Save Power Values
    def save_power_values(self, dr, txp, ch, standard, streams, cable_loss_1x1, cable_loss_2x2):
        debugPrint("Saving Power Values")
        self.socket_send("WIFI\n")
        if standard == "11b":
            self.socket_send("CALC:POW 0,1\n")
        else:
            self.socket_send("CALC:POW 0,10\n")
        self.socket_send("FETCh:POW:SIGN1:AVER?\n")
        result = str(cntrl_sckt.recv(200))
        debugPrint(result)
        power_1x1 = result.split(",")[-1]
        if streams == "1x1":
            debugPrint(round(float(power_1x1) + float(cable_loss_1x1), 2))
            return round(float(power_1x1) + float(cable_loss_1x1), 2)
        self.socket_send("FETCh:POW:SIGN2:AVER?\n")
        result = str(cntrl_sckt.recv(200))
        debugPrint(result)
        power_2x2 = result.split(",")[-1]
        debugPrint(round(float(power_1x1) + float(cable_loss_1x1), 2))
        debugPrint(round(float(power_2x2) + float(cable_loss_2x2), 2))
        return round(float(power_1x1) + float(cable_loss_1x1), 2), round(float(power_2x2) + float(cable_loss_2x2), 2)

    def save_evm_txquality_stats(self, dr, txp, ch, standard, streams):
        debugPrint("Saving EVM Values")
        self.socket_send("FORM:READ:DATA ASC\n")
        if standard == "11b":
            self.socket_send("FETCh:TXQuality:DSSS:AVER?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            evm_1x1 = result.split(",")[1]
            debugPrint(evm_1x1.encode().decode("unicode_escape").rstrip("'\n"))
            return evm_1x1.encode().decode("unicode_escape").rstrip("'\n")
        else:
            self.socket_send("FETC:OFDM:EVM:DATA:ALL:AVER?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            evm_1x1 = str(result).split(",")[1]
            if streams == "1x1":
                # return round(float(evm_1x1),2)
                debugPrint(evm_1x1.encode().decode("unicode_escape").rstrip("'\n"))
                return evm_1x1.encode().decode("unicode_escape").rstrip("'\n")
            evm_2x2 = str(result).split(",")[2]
        # print round(float(evm_1x1),2),round(float(evm_2x2),2)
        # return round(float(evm_1x1),2),round(float(evm_2x2),2)
        debugPrint(evm_1x1.encode().decode("unicode_escape").rstrip("'\n"))
        debugPrint(evm_2x2.encode().decode("unicode_escape").rstrip("'\n"))
        return evm_1x1.encode().decode("unicode_escape").rstrip("'\n"), evm_2x2.encode().decode(
            "unicode_escape"
        ).rstrip("'\n")

    # Save Freq Err
    def save_freqerr(self, dr, txp, standard, streams):
        debugPrint("Saving SYSCLKERR Values")
        if standard == "11b":
            self.socket_send("FETCh:TXQuality:DSSS:AVER?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            freq_error_1x1 = result.split(",")[4]
            # return round(float(freq_error_1x1),2)
            debugPrint(freq_error_1x1.encode().decode("unicode_escape").rstrip("'\n"))
            return freq_error_1x1.encode().decode("unicode_escape").rstrip("'\n")
        else:
            self.socket_send("FETC:OFDM:FERR:ALL:AVER?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            freq_error_1x1 = result.split(",")[1]
            if streams == "1x1":
                # return round(float(freq_error_1x1),2)
                debugPrint(freq_error_1x1.encode().decode("unicode_escape").rstrip("'\n"))
                return freq_error_1x1.encode().decode("unicode_escape").rstrip("'\n")
            freq_error_2x2 = result.split(",")[2]
        # return round(float(freq_error_1x1),2),round(float(freq_error_2x2)	,2)
        debugPrint(freq_error_1x1.encode().decode("unicode_escape").rstrip("'\n"))
        debugPrint(freq_error_2x2.encode().decode("unicode_escape").rstrip("'\n"))
        return freq_error_1x1.encode().decode("unicode_escape").rstrip("'\n"), freq_error_2x2.encode().decode(
            "unicode_escape"
        ).rstrip("'\n")

    # Save Phase Err
    def save_phaseerr(self, dr, txp, standard, streams):
        debugPrint("Saving SYSCLKERR Values")
        if standard == "11b":
            self.socket_send("FETCh:TXQuality:DSSS:AVER?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            phaseerr_1x1 = result.split(",")[3]
            # return round(float(phaseerr_1x1),2)
            debugPrint(phaseerr_1x1.encode().decode("unicode_escape").rstrip("'\n"))
            return phaseerr_1x1.encode().decode("unicode_escape").rstrip("'\n")
        else:
            self.socket_send("FETC:OFDM:PERR:ALL:AVER?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            phaseerr_1x1 = result.split(",")[1]
            if streams == "1x1":
                # return round(float(phaseerr_1x1),2)
                debugPrint(phaseerr_1x1.encode().decode("unicode_escape").rstrip("'\n"))
                return phaseerr_1x1.encode().decode("unicode_escape").rstrip("'\n")
            phaseerr_2x2 = result.split(",")[2]
        # return round(float(phaseerr_1x1),2),round(float(phaseerr_2x2),2)
        debugPrint(phaseerr_1x1.encode().decode("unicode_escape").rstrip("'\n"))
        debugPrint(phaseerr_2x2.encode().decode("unicode_escape").rstrip("'\n"))
        return phaseerr_1x1.encode().decode("unicode_escape").rstrip("'\n"), phaseerr_2x2.encode().decode(
            "unicode_escape"
        ).rstrip("'\n")

    # Save Gain Imb
    def save_ampimb(self, dr, txp, standard, streams):
        debugPrint("Saving GainImb Values")
        if standard == "11b":
            self.socket_send("FETCh:TXQuality:DSSS:AVER?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            ampimb_1x1 = result.split(",")[8]
            # return round(float(ampimb_1x1),2)
            debugPrint(ampimb_1x1.encode().decode("unicode_escape").rstrip("'\n"))
            return ampimb_1x1.encode().decode("unicode_escape").rstrip("'\n")
        else:
            self.socket_send("FETC:OFDM:AIMB:ALL:AVER?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            ampimb_1x1 = result.split(",")[1]
            if streams == "1x1":
                # return round(float(ampimb_1x1),2)
                debugPrint(ampimb_1x1.encode().decode("unicode_escape").rstrip("'\n"))
                return ampimb_1x1.encode().decode("unicode_escape").rstrip("'\n")
            ampimb_2x2 = result.split(",")[2]
        # return round(float(ampimb_1x1),2),round(float(ampimb_2x2),2)
        debugPrint(ampimb_1x1.encode().decode("unicode_escape").rstrip("'\n"))
        debugPrint(ampimb_2x2.encode().decode("unicode_escape").rstrip("'\n"))
        return ampimb_1x1.encode().decode("unicode_escape").rstrip("'\n"), ampimb_2x2.encode().decode(
            "unicode_escape"
        ).rstrip("'\n")

    # Save Phase Imb
    def save_phaseimb(self, dr, txp, standard, streams):
        debugPrint("Saving PhaseImb Values")
        if standard == "11b":
            self.socket_send("FETCh:TXQuality:DSSS:AVER?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            phaseimb_1x1 = result.split(",")[9]
            # return round(float(phaseimb_1x1),2)
            debugPrint(phaseimb_1x1.encode().decode("unicode_escape").rstrip("'\n"))
            return phaseimb_1x1.encode().decode("unicode_escape").rstrip("'\n")
        else:
            self.socket_send("FETC:OFDM:PIMB:ALL:AVER?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            phaseimb_1x1 = str(result).split(",")[1]
            if streams == "1x1":
                # return round(float(phaseimb_1x1),2)
                debugPrint(phaseimb_1x1.encode().decode("unicode_escape").rstrip("'\n"))
                return phaseimb_1x1.encode().decode("unicode_escape").rstrip("'\n")
            phaseimb_2x2 = result.split(",")[2]
        # return round(float(phaseimb_1x1),2),round(float(phaseimb_2x2),2)
        debugPrint(phaseimb_1x1.encode().decode("unicode_escape").rstrip("'\n"))
        debugPrint(phaseimb_2x2.encode().decode("unicode_escape").rstrip("'\n"))
        return phaseimb_1x1.encode().decode("unicode_escape").rstrip("'\n"), phaseimb_2x2.encode().decode(
            "unicode_escape"
        ).rstrip("'\n")

    # Save TX Quality Stats
    def save_txquality_stats(self, dr, txp, ch, standard, streams):
        # print('Saving EVM Values')
        debugPrint("Saving EVM Values")
        self.socket_send("FORM:READ:DATA ASC\n")
        if standard == "11b":
            self.socket_send("FETCh:TXQuality:DSSS?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            evm_1x1 = result.split(",")[1]
            evm_2x2 = result.split(",")[1]
            phaseerr_1x1 = result.split(",")[3]
            phaseerr_2x2 = result.split(",")[3]
            freq_error_1x1 = result.split(",")[4]
            freq_error_2x2 = result.split(",")[4]
            sysclkerr_1x1 = result.split(",")[6]
            sysclkerr_2x2 = result.split(",")[6]
            lo_leakage_1x1 = result.split(",")[7]
            lo_leakage_2x2 = result.split(",")[7]
            ampimb_1x1 = result.split(",")[8]
            ampimb_2x2 = result.split(",")[8]
            phaseimb_1x1 = result.split(",")[8]
            phaseimb_2x2 = result.split(",")[8]
        else:
            if streams == "1x1":
                phaseimb_1x1 = self.save_phaseimb(dr, txp, standard, streams)
                evm_1x1 = self.save_evm_txquality_stats(dr, txp, ch, standard, streams)
                phaseerr_1x1 = self.save_phaseerr(dr, txp, standard, streams)
                freq_error_1x1 = self.save_freqerr(dr, txp, standard, streams)
                sysclkerr_1x1 = self.save_sysclkerr(dr, txp, standard, streams)
                lo_leakage_1x1 = self.save_lo_leakage(dr, txp, standard, streams)
                ampimb_1x1 = self.save_ampimb(dr, txp, standard, streams)
            elif streams == "2x2":
                phaseimb_1x1, phaseimb_2x2 = self.save_phaseimb(dr, txp, standard, streams)
                evm_1x1, evm_2x2 = self.save_evm_txquality_stats(dr, txp, ch, standard, streams)
                phaseerr_1x1, phaseerr_2x2 = self.save_phaseerr(dr, txp, standard, streams)
                freq_error_1x1, freq_error_2x2 = self.save_freqerr(dr, txp, standard, streams)
                sysclkerr_1x1, sysclkerr_2x2 = self.save_sysclkerr(dr, txp, standard, streams)
                lo_leakage_1x1, lo_leakage_2x2 = self.save_lo_leakage(dr, txp, standard, streams)
                ampimb_1x1, ampimb_2x2 = self.save_ampimb(dr, txp, standard, streams)
        if streams == "1x1":
            return evm_1x1, phaseerr_1x1, freq_error_1x1, sysclkerr_1x1, lo_leakage_1x1, ampimb_1x1, phaseimb_1x1
        return (
            evm_1x1,
            evm_2x2,
            phaseerr_1x1,
            phaseerr_2x2,
            freq_error_1x1,
            freq_error_2x2,
            sysclkerr_1x1,
            sysclkerr_2x2,
            lo_leakage_1x1,
            lo_leakage_2x2,
            ampimb_1x1,
            ampimb_2x2,
            phaseimb_1x1,
            phaseimb_2x2,
        )

    # Save Sys Clk Err
    def save_sysclkerr(self, dr, txp, standard, streams):
        debugPrint("Saving SYSCLKERR Values")
        if standard == "11b":
            self.socket_send("FETC:DSSS:SCER:ALL:AVER?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            sysclkerr_1x1 = result.split(",")[6]
            debugPrint(sysclkerr_1x1.encode().decode("unicode_escape").rstrip("'\n"))
            return sysclkerr_1x1.encode().decode("unicode_escape").rstrip("'\n")
        else:
            self.socket_send("FETC:OFDM:SCER:ALL:AVER?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            sysclkerr_1x1 = result.split(",")[1]
            if streams == "1x1":
                # return round(float(sysclkerr_1x1),2)
                debugPrint(sysclkerr_1x1.encode().decode("unicode_escape").rstrip("'\n"))
                return sysclkerr_1x1.encode().decode("unicode_escape").rstrip("'\n")
            sysclkerr_2x2 = result.split(",")[2]
        # return round(float(sysclkerr_1x1),2),round(float(sysclkerr_2x2),2)
        debugPrint(sysclkerr_1x1.encode().decode("unicode_escape").rstrip("'\n"))
        debugPrint(sysclkerr_2x2.encode().decode("unicode_escape").rstrip("'\n"))
        return sysclkerr_1x1.encode().decode("unicode_escape").rstrip("'\n"), sysclkerr_2x2.encode().decode(
            "unicode_escape"
        ).rstrip("'\n")

    # Save Gain Imb
    def save_gainimb(self, dr, txp, standard, streams):
        if standard == "11b":
            self.socket_send("FETC:DSSS:AIMB:ALL:AVER?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            gainimb_1x1 = result.split(",")[8]
        else:
            self.socket_send("FETC:OFDM:AIMB:ALL:AVER?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            ampimb_1x1 = result.split(",")[1]
            if streams == "2x2":
                gainimb_2x2 = result.split(",")[2]
        return float(gainimb_1x1), float(gainimb_2x2)

    # Save LO Leakage
    def save_lo_leakage(self, dr, txp, standard, streams):
        debugPrint("Saving lo_leakage Values")
        if standard == "11b":
            self.socket_send("FETC:DSSS:LOLeakage:ALL:AVER?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            lo_leakage_1x1 = result.split(",")[6]
            debugPrint(lo_leakage_1x1.encode().decode("unicode_escape").rstrip("'\n"))
            return lo_leakage_1x1.encode().decode("unicode_escape").rstrip("'\n")
        else:
            self.socket_send("FETC:OFDM:LOLeakage:ALL:AVER?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            lo_leakage_1x1 = result.split(",")[1]
            if streams == "1x1":
                # return round(float(lo_leakage_1x1),2)
                debugPrint(lo_leakage_1x1.encode().decode("unicode_escape").rstrip("'\n"))
                return lo_leakage_1x1.encode().decode("unicode_escape").rstrip("'\n")
            lo_leakage_2x2 = result.split(",")[2]
        # return round(float(lo_leakage_1x1),2),round(float(lo_leakage_2x2),2)
        debugPrint(lo_leakage_1x1.encode().decode("unicode_escape").rstrip("'\n"))
        debugPrint(lo_leakage_2x2.encode().decode("unicode_escape").rstrip("'\n"))
        return lo_leakage_1x1.encode().decode("unicode_escape").rstrip("'\n"), lo_leakage_2x2.encode().decode(
            "unicode_escape"
        ).rstrip("'\n")

    # Save OBW
    def save_obw_values(self, standard, streams):
        self.socket_send("CHAN1\n")
        if streams == "2x2":
            self.socket_send("MVSAALL ;init\n")
        else:
            self.socket_send("VSA1" + chain_sel_scpi_cmd + " ;init\n")
        self.socket_send("WIFI\n")
        if standard == "11b":
            self.socket_send("calc:pow 0, 1\n")
            self.socket_send("calc:txq 0, 1\n")
            self.socket_send("calc:ccdf 0, 1\n")
            self.socket_send("calc:spec 0, 1\n")
        else:
            self.socket_send("calc:txq 0, 1\n")

        debugPrint("Saving OBW Values")
        if standard == "11b":
            obw_1x1 = "20000000"
        else:
            self.socket_send("FETCH:TXQuality:OFDM:INFO:CBW?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            obw_1x1 = result.split(",")[1]
        debugPrint(str(int(obw_1x1) / 1000000))
        return str(int(obw_1x1) / 1000000)

    # Save Data Rate Values
    def save_datarate_values(self, standard, streams):
        debugPrint("Saving data rate Values")
        if standard == "11b":
            self.socket_send("FETCH:TXQuality:DSSS:INFO:DRATE?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            dr_1x1 = result.split(",")[1].encode().decode("unicode_escape").rstrip("'\n")
            debugPrint(dr_1x1)
            return dr_1x1
        elif standard == "11g" or standard == "11a":
            self.socket_send("FETCH:TXQuality:OFDM:INFO:DRATE?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            dr_1x1 = result.split(",")[1].encode().decode("unicode_escape").rstrip("'\n")
            debugPrint(dr_1x1)
            return dr_1x1
        else:
            self.socket_send("FETCH:TXQuality:OFDM:INFO:MCS?\n")
            result = str(cntrl_sckt.recv(200))
            debugPrint(result)
            dr_1x1 = result.split(",")[1].encode().decode("unicode_escape").rstrip("'\n")
            dr_1x1 = "MCS" + dr_1x1
            debugPrint(dr_1x1)
            return dr_1x1
            if streams == "2x2":
                dr_2x2 = result.split(",")[2]
                dr_2x2 = "MCS" + dr_2x2
        debugPrint(dr_1x1)
        debugPrint(dr_2x2)
        return dr_1x1, dr_2x2

    def save_spec_margins(self, standard, ch, bw="20"):
        # if (standard == '11b'):
        # time.sleep(2)
        # self.socket_send('VSA1;WIFI;CLE:SPEC\n')
        # set_modulation('OFDM')
        # set_frequency(ch)
        # time.sleep(0.5)
        # self.socket_send('VSA1;INIT\n')
        # self.socket_send('WIFI\n')
        # self.socket_send('CALC:SPEC 0,10\n')
        # time.sleep(0.5)
        self.socket_send("FORM:READ:DATA ASC\n")
        self.socket_send("FETC:SPEC:AVER:MARG:OFR?\n")
        # time.sleep(0.5)
        result = cntrl_sckt.recv(512)
        debugPrint(result)
        # print result
        # print "Avg Spectrum margin offset frequencies in Hz: ",result[2:-1]
        spectrum_result = result.split(",")
        spectral_margins_freq = spectrum_result[1:]

        # for i in spectral_margins_freq:
        # spec_data.append(round(float(i),2))
        self.socket_send("FETC:SPEC:AVER:MARG?\n")
        # time.sleep(0.5)
        result = cntrl_sckt.recv(512)
        debugPrint(result)
        spectrum_result = result.split(",")
        spectrum_status_code = float(spectrum_result[0])
        spectral_margins = spectrum_result[1:]
        # print 'spectrum_status_code',spectrum_status_code
        if spectrum_status_code == 0:
            # print "Avg spectrum margin (Passed) in dB: ",result[2:-1]
            debugPrint("PASS,PASS")
            return "PASS", "PASS"
            # for i in spectral_margins:
            # spec_data.append(round(float(i),2))
        elif spectrum_status_code == 1:
            # print "Avg spectrum margin (Failed) in dB: ",result[2:-1]
            debugPrint("FAIL,FAIL")
            return "FAIL", "FAIL"
            # data.append('FAIL')
            # for i in spectral_margins:
            # spec_data.append(round(float(i),2))
        else:
            debugPrint("NODATA,NODATA")
            return "NODATA", "NODATA"
            # for i in spectral_margins:
            # spec_data.append('NODATA')

        self.socket_send("FETC:SPEC:MAX:MARG:OFR?\n")
        # time.sleep(0.5)
        result = cntrl_sckt.recv(512)
        debugPrint(result)
        # print "Max Spectrum margin offset frequencies in Hz: ",result[2:-1]
        max_spectrum_result = result.split(",")
        max_spectral_margins_freq = max_spectrum_result[1:]
        for i in max_spectral_margins_freq:
            max_spec_data.append(i)

        self.socket_send("FETC:SPEC:MAX:MARG?\n")
        # time.sleep(0.5)
        result = cntrl_sckt.recv(512)
        debugPrint(result)
        max_spectrum_result = result.split(",")
        max_spectrum_status_code = float(max_spectrum_result[0])
        max_spectral_margins = max_spectrum_result[1:]
        if max_spectrum_status_code == 0:
            print("Max spectrum margin (Passed) in dB: ", result[2:-1])
            return "PASS"
            for i in max_spectral_margins:
                max_spec_data.append(i)
        elif max_spectrum_status_code == 1:
            print("Max spectrum margin (Failed) in dB: ", result[2:-1])
            return "FAIL"
            for i in max_spectral_margins:
                max_spec_data.append(i)
        else:
            return "NODATA"
            for i in max_spectral_margins:
                max_spec_data.append("NODATA")
        if (standard == "11b") and (bwcfg != "20C"):
            set_modulation("DSSS")  # Revert to DSSS

    def save_ofdm_spec_flatness(self, standard):
        if standard == "11b":
            return "NODATA", "NODATA"
        else:
            self.socket_send("FETC:TXQ:OFDM:SFL:MARG?\n")
        result = cntrl_sckt.recv(2048)
        sfl_check_result = result.split(",")
        if all(float(sf) == 0 for sf in sfl_check_result[::5]):
            if all(float(s_f) >= 0 for s_f in sfl_check_result):
                # print "OFDM spectral flatness check: PASS"
                return "PASS", "PASS"
                self.socket_send("FETC:TXQ:OFDM:SFL:AVER:MARG?\n")
                result = cntrl_sckt.recv(512)
                if float(result.split(",")[0]) == 0:
                    print("Average OFDM spectral flatness margins in dB:", result[2:-1])
            else:
                # print("OFDM spectral flatness check: FAIL")
                # print("OFDM spectral flatness margins:",result[:-1])
                return "FAIL", "FAIL"
        else:
            # print("OFDM SPECTRAL FLATNESS CHECK: NODATA")
            # print("OFDM spectral flatness check result:",result[:-1])
            return "NODATA", "NODATA"

    def save_psdu_crc(self, standard, d_rate):
        if standard == "11b":
            self.socket_send("FETC:TXQ:DSSS:PSDU:CRC?\n")
        else:
            self.socket_send("FETC:TXQ:OFDM:PSDU:CRC?\n")
        result = cntrl_sckt.recv(512)
        debugPrint(result)
        psdu_crc_result = result.split(",")
        if all(float(pc) == 0 for pc in psdu_crc_result[::2]):
            if all(float(pc) == 1 for pc in psdu_crc_result[1::2]):
                # print "PSDU CRC: PASS"
                return "PASS", "PASS"
            else:
                # print "PSDU CRC result:",result[:-1]
                # print "PSDU CRC: FAIL"
                return "FAIL", "FAIL"
        else:
            # print "PSDU CRC result:",result[:-1]
            # print "PSDU CRC: NODATA"
            return "NODATA", "NODATA"

    # Click AGC Button
    def click_agc(self, standard, streams, ref_level="AUTO", chain_sel_scpi_cmd="1"):
        debugPrint("Click AGC")
        if streams == "2x2":
            self.socket_send("MVSAALL ;RLEVel " + ref_level + "\n")
        else:
            self.socket_send("VSA1" + chain_sel_scpi_cmd + " ;RLEVel:AUTO\n")
            # # self.socket_send('VSA1;RLEV 25\n')
            # self.socket_send('VSA1;RLEV '+ref_level+'\n')
        return
        self.socket_send("CHAN1\n")
        if streams == "2x2":
            self.socket_send("MVSAALL ;init\n")
        else:
            self.socket_send("VSA1" + chain_sel_scpi_cmd + " ;init\n")
        self.socket_send("WIFI\n")
        if standard == "11b":
            self.socket_send("calc:pow 0, 1\n")
            self.socket_send("calc:txq 0, 1\n")
            self.socket_send("calc:ccdf 0, 1\n")
            self.socket_send("calc:spec 0, 1\n")
        else:
            self.socket_send("calc:pow 0, 10\n")
            self.socket_send("calc:txq 0, 10\n")
            self.socket_send("calc:ccdf 0, 10\n")
            self.socket_send("calc:ramp 0, 10\n")
            self.socket_send("calc:spec 0, 10\n")

    # Start Packet Analyses
    def click_analyser(self, standard, streams, chain_sel_scpi_cmd="1"):
        debugPrint("Click Analyser")
        self.socket_send("CHAN1\n")
        if streams == "2x2":
            self.socket_send("MVSAALL ;init\n")
        else:
            self.socket_send("VSA1" + chain_sel_scpi_cmd + " ;init\n")
        self.socket_send("WIFI\n")
        if standard == "11b":
            self.socket_send("calc:pow 0, 1\n")
            self.socket_send("calc:txq 0, 1\n")
            self.socket_send("calc:ccdf 0, 1\n")
            self.socket_send("calc:spec 0, 1\n")
        else:
            self.socket_send("calc:pow 0, 10\n")
            self.socket_send("calc:txq 0, 1\n")
            self.socket_send("calc:ccdf 0, 10\n")
            self.socket_send("calc:spec 0, 10\n")

    # Modulation Type
    def set_vsa_modulation(self, standard):
        debugPrint("Setting VSA standard " + standard)
        if standard == "11b":
            modulation = "dsss"
        else:
            modulation = "ofdm"
        # print "\nSetting "+modulation+" in VSA"
        debugPrint("\nSetting " + modulation + " in VSA")
        self.socket_send("CHAN1;WIFI;CONF:STAN " + modulation.upper() + "\n")
        if standard == "11b":
            self.socket_send("CHAN1;WIFI;CONF:STAN DSSS\n")

    def init_vsa_funcs(
        self,
        standard="11ac",
        bw="20",
        streams="2x2",
        stbc="STBC_0",
        gi="LGI",
        coding="BCC",
        greenfield_mode="Mixed",
        preamble="LONG",
        payload="1024",
        chain_sel="1",
    ):
        self.start_vsg()
        self.set_equip_default()
        self.set_rf(streams=streams, test="tx", chain_sel=chain_sel)
        self.set_vsa_modulation(standard)
        self.set_capturelength(100, streams)

    def config_adj_11a(self):
        return

    # 802.11b Initialization settings
    def config_adj_11b(self):
        return

    # 802.11g Initialization settings
    def config_adj_11g(self):
        return

    # 802.11n Initialization settings
    def config_adj_11n(self):
        return

    # 802.11ac Initialization settings
    def config_adj_11ac(self):
        return

    # Modulation Type
    def set_adj_modulation(self, standard):
        print("\nSetting " + standard + " in VSA")
        return

    # Setting Payload
    def set_adj_payload(self, standard, payload):
        print("\nSetting payload ", payload)
        return

    # Setting MAC Header OFF
    def set_adj_macheader(self):
        print("Set adj MACHeader")
        return

    # Setting Channel
    def apply_adjacent_vsg(self, bw="", chn="", streams="2x2", config="adj"):
        print("apply_adjacent_vsg")
        return

    # Setting Adj Amplitude
    def set_adj_amplitude(self, streams, ampl):
        print("\nSetting adj amplitude ", ampl)
        return

    def set_adj_bandwidth(self, standard="", bw=""):
        print("set_adj_bandwidth")
        return

    # RF ON/OFF
    def rf_on_off_adj(self, rf_state="on", streams="1x1"):
        print("\nSetting RF ", rf_state)
        return

    def set_pop_trigger(self, packet_delay="", packet_cnt="2000"):
        print("Setting packet delay ", packet_delay)
        return
