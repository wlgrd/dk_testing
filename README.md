
# 0 Porting to Python 3.10

Main changes done: 
* Replaces prints
* Removed a lot of imports
* A lot of formatting
* Installed:
  * matplotlib
  * termcolor
  * pyserial
* Changed all occurrences of `wifi_radio_test` to `nrf_wifi_prod`
* encode strings for all cntrl_sckt.sendall calls
* 

NOTE: fixed for minimal requirements, just do `python -m pip install -r requirements.txt` instead of the list under 3#. 
# 1.	Hardware Required

1. PC: Any Linux/Windows PC
2. DK
3. Litepoint 
4. Co-axial Cables/LAN Cables

# 2.	Test Setup

![test setup](test_setup.png)

# 3.	Installations
1.	Python27 and the following modules
```
wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
python2 get-pip.py
vim input_conf.py
python -m pip install xlsxwriter
python -m pip install numpy
python -m pip install matplotlib
python -m pip install paramiko
python -m pip install serial
python -m pip install pyserial
python -m pip install openpyxl
python -m pip install docx
python -m pip install python_docx
```

# 4.	Script Execution

1.	Open `input_conf.py`
2.	Edit the following parameters
```
tester_hostname =
com_port =
board_num =
```

3.	Run the following command `python test_dk.py`

# 5.	Output
1.	Text file be created in the same directory xo_val_board_14.txt, assuming 14 as the board number configured in input_conf.py
2.	This XO will be used for all TX and RX tests
3.	Sample output of execution is as below:

```
Trying to find optimal XO for the board
Found Optimal XO : 30
=========== Starting TX Tests ===========

Channel :       1
Standard        :       11b
Data Rate       :       1
Measured EVM    :       -25.55
EVM Stauts      :       PASS
Spectral Mask Status    :       PASS

Channel :       1
Standard        :       11b
Data Rate       :       11
Measured EVM    :       -24.66
EVM Stauts      :       PASS
Spectral Mask Status    :       PASS

Channel :       36
Standard        :       11n
Data Rate       :       MCS0
Measured EVM    :       -32.22
EVM Stauts      :       PASS
Spectral Mask Status    :       PASS

Channel :       36
Standard        :       11n
Data Rate       :       MCS7
Measured EVM    :       -31.83
EVM Stauts      :       PASS
Spectral Mask Status    :       PASS

Channel :       149
Standard        :       11n
Data Rate       :       MCS0
Measured EVM    :       -32.37
EVM Stauts      :       PASS
Spectral Mask Status    :       PASS

Channel :       149
Standard        :       11n
Data Rate       :       MCS7
Measured EVM    :       -33.46
EVM Stauts      :       PASS
Spectral Mask Status    :       PASS
=========== Starting RX Tests ===========

Channel :       1
Standard        :       11b
Data Rate       :       1
Measured PER%   :       0.0
PER Stauts      :       PASS

Channel :       1
Standard        :       11b
Data Rate       :       11
Measured PER%   :       0.0
PER Stauts      :       PASS

Channel :       36
Standard        :       11n
Data Rate       :       MCS0
Measured PER%   :       0.0
PER Stauts      :       PASS

Channel :       36
Standard        :       11n
Data Rate       :       MCS7
Measured PER%   :       0.0
PER Stauts      :       PASS

Channel :       149
Standard        :       11n
Data Rate       :       MCS0
Measured PER%   :       0.0
PER Stauts      :       PASS

Channel :       149
Standard        :       11n
Data Rate       :       MCS7
Measured PER%   :       0.0
PER Stauts      :       PASS
```