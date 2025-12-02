from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import csv
import os
import base64
import requests
from requests.auth import HTTPBasicAuth
from configparser import ConfigParser
import json
import time


import base64   
import httpx   
import openai   

app = Flask(__name__)
CORS(app)


# Global variables - will be initialized when needed
configur = None
Gpt4ifxUname = None
Gpt4ifxPassword = None
Gpt4ifxchatUrl = None
Gpt4ifxBearertoken = None
Gpt4ifxUrlBearertoken = None

def init_config():
    global configur, Gpt4ifxUname, Gpt4ifxPassword, Gpt4ifxchatUrl, Gpt4ifxBearertoken, Gpt4ifxUrlBearertoken
    
    if configur is not None:
        return  # Already initialized
    
    # Initialize config with error handling
    configur = ConfigParser()
    config_files = ['config.ini', 'config_template.ini']
    config_loaded = False

    for config_file in config_files:
        if os.path.exists(config_file):
            configur.read(config_file)
            if configur.has_section('gpt4ifxapi'):
                config_loaded = True
                break

    if not config_loaded:
        print("ERROR: No valid config file found")
        print("Available files:", [f for f in os.listdir('.') if f.endswith('.ini')])
        raise Exception("No valid config file found. Please create config.ini from config_template.ini")

    # Get config values with fallbacks - prioritize environment variables
    Gpt4ifxUname = os.getenv('GPT4IFX_USERNAME') or configur.get('gpt4ifxapi', 'username', fallback='')
    Gpt4ifxPassword = os.getenv('GPT4IFX_PASSWORD') or configur.get('gpt4ifxapi', 'password', fallback='')
    Gpt4ifxchatUrl = configur.get('gpt4ifxapi', 'chaturl', fallback='https://gpt4ifx.icp.infineon.com')
    Gpt4ifxBearertoken = configur.get('gpt4ifxapi', 'bearertoken', fallback='')
    Gpt4ifxUrlBearertoken = configur.get('gpt4ifxapi', 'url_bearertoken', fallback='https://gpt4ifx.icp.infineon.com/auth/token')

    print(f"Config loaded - Username: '{Gpt4ifxUname[:3]}***' (length: {len(Gpt4ifxUname)})")
    print(f"Password configured: {'Yes' if Gpt4ifxPassword else 'No'} (length: {len(Gpt4ifxPassword) if Gpt4ifxPassword else 0})")
    print(f"Token URL: {Gpt4ifxUrlBearertoken}")
    print(f"Environment GPT4IFX_USERNAME: {os.getenv('GPT4IFX_USERNAME', 'Not set')}")
    print(f"Environment GPT4IFX_PASSWORD: {'Set' if os.getenv('GPT4IFX_PASSWORD') else 'Not set'}")

def Gpt4ifx_get_Bearertoken():
    init_config()  # Initialize config if not done
    
    if not Gpt4ifxUname or not Gpt4ifxPassword:
        raise Exception("Username and password must be configured in config.ini or environment variables")
    
    print(f"Attempting to get token for user: {Gpt4ifxUname}")
    print(f"Using URL: {Gpt4ifxUrlBearertoken}")
    
    try:
        basic = HTTPBasicAuth(Gpt4ifxUname.strip(), Gpt4ifxPassword.strip())
        
        # Add headers that might be required
        headers = {
            'User-Agent': 'IFX-MSD-GenAI-Tool/1.0',
            'Accept': 'application/json'
        }
        
        response = requests.get(Gpt4ifxUrlBearertoken, auth=basic, headers=headers, verify=False, timeout=30)
        
        print(f"Token request status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            token = response.text.strip()
            print(f"Token obtained successfully (length: {len(token)})")
            # Update config if possible
            if os.path.exists('config.ini'):
                configur.set('gpt4ifxapi','bearertoken', token)
                with open('config.ini', 'w') as f:
                    configur.write(f)
            return token
        elif response.status_code == 401:
            print(f"Auth failed - Username: '{Gpt4ifxUname}', Password length: {len(Gpt4ifxPassword)}")
            raise Exception(f"Authentication failed. Check credentials in HICP environment variables. Response: {response.text}")
        else:
            raise Exception(f"Failed to get bearer token. Status: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error getting token: {str(e)}")

#cert_path = 'C:\Users\pandevaibhav\Documents\Projects\deepa-regmap-ui\diff-checker\ca-bundle.crt'
cert_path = 'C:/Users/pandevaibhav/Documents/Projects/deepa-regmap-ui/diff-checker/ca-bundle.crt'
basic_auth = False      
token = Gpt4ifx_get_Bearertoken()
headers = {     
        'Authorization': f"Bearer {token}",      
        "accept": "application/json",
        "Content-Type": "application/json"}      
   
client = openai.OpenAI(     
            api_key=Gpt4ifx_get_Bearertoken(),     
            base_url='https://gpt4ifx.icp.infineon.com',      
            default_headers=headers,     
            http_client = httpx.Client(verify=cert_path)   
            ) 






my_promt = "You are a very logical AI"

#user input1
user_input_1 = """MAIN    0x0000    0x001e8270
ADC0    0x0001    0x000a0210
PACR1    0x0004    0x00e967fd
PACR2    0x0005    0x000805b4
SFCTL    0x0006    0x001027ff
SADC_CTRL    0x0007    0x00010d00
CSP_I_0    0x0008    0x00000000
CSP_I_1    0x0009    0x00000000
CSP_I_2    0x000a    0x00000000
CSCI    0x000b    0x00000be0"""

step_1_prompt1 = f"""Split the data into three columns and also create a new column converting the hexadecimal values in the third column to binary 

{user_input_1}

Also, provide the output in the .csv format
Reply with only the data in csv and nothing else
"""

register_name="MAIN"

register_map = {
    "MAIN": {
        "FRAME_START": "0",
        "SW_RESET": "1",
        "FSM_RESET": "2",
        "FIFO_RESET": "3",
        "SPI_BC_MODE": "4",
        "PU_IRQ_EN": "5",
        "PU_CSN_EN": "6",
        "PU_CLK_EN": "7",
        "PU_DI_EN": "8",
        "PU_DO_EN": "9",
        "RSVD": "10, 15:12, 18:17",
        "PU_RST_EN": "11",
        "CW_MODE": "16",
        "MADC_BG_CLK_DIV": "20:19",
        "LOAD_STRENGTH": "22:21",
        "LDO_MODE": "23"
    },
    "ADC0": {
        "ADC_Overs_CFG": "1:0",
        "BG_CHOP_EN": "5",
        "BG_TCTRIM": "4:2",
        "STC": "7:6",
        "DSCAL": "8",
        "TRACK_CFG": "10:9",
        "MSB_CTRL": "11",
        "TRIG_MADC": "12",
        "RSVD": "13",
        "ADC_DIV": "23:14"
    },
    "PACR1": {
        "ANAPON": "0",
        "VANAREG": "2:1",
        "DIGPON": "3",
        "VDIGREG": "5:4",
        "BGAPEN": "6",
        "U2IEN": "7",
        "VREFSEL": "9:8",
        "RFILTSEL": "10",
        "RLFSEL": "11",
        "RSVD": "12",
        "LOCKSEL": "15:13",
        "LOCKFORC": "16",
        "ICPSEL": "19:17",
        "BIASFORC": "20",
        "CPEN": "21",
        "LFEN": "22",
        "OSCCLKEN": "23"
    },
    "PACR2": {
        "DIVSET": "4:0",
        "DIVEN": "5",
        "FSTDNEN": "7:6",
        "FSDNTMR": "16:8",
        "TRIVREG": "17",
        "DTSEL": "19:18",
        "RSVD": "20",
        "TR_DIVEN": "23:21"
    },
    "SFCTL": {
        "FIFO_CREF": "12:0",
        "RSVD": "13, 23:20",
        "FIFO_PD_MODE": "15:14",
        "MISO_HS_READ": "16",
        "LFSR_EN": "17",
        "PREFIX_EN": "18",
        "PAD_MODE": "19"
    },
    "CSP_I_0": {
        "TX1_EN": "0",
        "PD1_EN": "1",
        "RSVD": "3:2, 9:7, 19:14, 23:21",
        "VCO_EN": "4",
        "TEMP_MEAS_EN": "5",
        "FDIV_EN": "6",
        "LO_DIST2_EN": "10",
        "LO_DIST1_EN": "11",
        "RX1LOBUF_EN": "12",
        "RX1MIX_EN": "13",
        "ABB1_AAF_CTRL": "20"
    },
    "CSP_I_1": {
        "TX1_DAC": "4:0",
        "RSVD": "9:5, 13:11, 23:21",
        "HP1_GAIN": "10",
        "BB_RSTCNT": "19:14",
        "MADC_BBCH1_EN": "20"
    },
    "CSP_I_2": {
        "HPF_SEL1": "2:0",
        "VGA_GAIN1": "5:3",
        "RSVD": "23:6"
    },
    "CSCI": {
        "RSVD": "4:0, 9",
        "ABB_ISOPD": "5",
        "RF_ISOPD": "6",
        "MADC_BG_EN": "7",
        "MADC_ISOPD": "8",
        "BG_TMRF_EN": "10",
        "PLL_ISOPD": "11",
        "TR_PLL_ISOPD": "17:12",
        "TR_MADCEN": "20:18",
        "TR_BGEN": "23:21"
    },
    "CSP_D_0": {
        "TX1_EN": "0",
        "PD1_EN": "1",
        "RSVD": "3:2, 9:7, 19:14, 23:21",
        "VCO_EN": "4",
        "TEMP_MEAS_EN": "5",
        "FDIV_EN": "6",
        "LO_DIST2_EN": "10",
        "LO_DIST1_EN": "11",
        "RX1LOBUF_EN": "12",
        "RX1MIX_EN": "13",
        "ABB1_AAF_CTRL": "20"
    },
    "CSP_D_1": {
        "TX1_DAC": "4:0",
        "RSVD": "9:5, 13:11, 23:21",
        "HP1_GAIN": "10",
        "BB_RSTCNT": "19:14",
        "MADC_BBCH1_EN": "20"
    },
    "CSP_D_2": {
        "HPF_SEL1": "2:0",
        "VGA_GAIN1": "5:3",
        "RSVD": "23:6"
    },
    "CSCDS": {
        "RSVD": "4:0, 9, 23:12",
        "ABB_ISOPD": "5",
        "RF_ISOPD": "6",
        "MADC_BG_EN": "7",
        "MADC_ISOPD": "8",
        "BG_TMRF_EN": "10",
        "PLL_ISOPD": "11"
    },
    "CS1_U_0": {
        "TX1_EN": "0",
        "PD1_EN": "1",
        "RSVD": "3:2, 9:7, 19:14, 23:21",
        "VCO_EN": "4",
        "TEMP_MEAS_EN": "5",
        "FDIV_EN": "6",
        "LO_DIST2_EN": "10",
        "LO_DIST1_EN": "11",
        "RX1LOBUF_EN": "12",
        "RX1MIX_EN": "13",
        "ABB1_AAF_CTRL": "20"
    },
    "CS1_U_1": {
        "TX1_DAC": "4:0",
        "RSVD": "9:5, 13:11, 23:21",
        "HP1_GAIN": "10",
        "BB_RSTCNT": "19:14",
        "MADC_BBCH1_EN": "20"
    },
    "CS1_U_2": {
        "HPF_SEL1": "2:0",
        "VGA_GAIN1": "5:3",
        "RSVD": "23:6"
    },
    "CS1": {
        "REPCS": "3:0",
        "CS_EN": "4",
        "ABB_ISOPD": "5",
        "RF_ISOPD": "6",
        "MADC_BG_EN": "7",
        "MADC_ISOPD": "8",
        "RSVD": "9, 23:12",
        "BG_TMRF_EN": "10",
        "PLL_ISOPD": "11"
    },
    "CS2": {
        "REPCS": "3:0",
        "CS_EN": "4",
        "ABB_ISOPD": "5",
        "RF_ISOPD": "6",
        "MADC_BG_EN": "7",
        "MADC_ISOPD": "8",
        "RSVD": "9, 23:12",
        "BG_TMRF_EN": "10",
        "PLL_ISOPD": "11"
    },
    "CS3": {
        "REPCS": "3:0",
        "CS_EN": "4",
        "ABB_ISOPD": "5",
        "RF_ISOPD": "6",
        "MADC_BG_EN": "7",
        "MADC_ISOPD": "8",
        "RSVD": "9, 23:12",
        "BG_TMRF_EN": "10",
        "PLL_ISOPD": "11"
    },
    "CS4": {
        "REPCS": "3:0",
        "CS_EN": "4",
        "ABB_ISOPD": "5",
        "RF_ISOPD": "6",
        "MADC_BG_EN": "7",
        "MADC_ISOPD": "8",
        "RSVD": "9, 23:12",
        "BG_TMRF_EN": "10",
        "PLL_ISOPD": "11"
    },
    "CCR0": {
        "TR_END": "8:0",
        "CONT_MODE": "9",
        "REPT": "13:10",
        "TR_INIT1": "21:14",
        "TR_INIT1_MUL": "23:22"
    },
    "CCR1": {
        "TR_START": "8:0",
        "PD_MODE": "10:9",
        "TR_FED": "18:11",
        "TR_FED_MUL": "23:19"
    },
    "CCR2": {
        "MAX_FRAME_CNT": "11:0",
        "FRAME_LEN": "23:12"
    },
    "CCR3": {
        "TR_PAEN": "8:0",
        "TR_SSTART": "14:9",
        "TR_INIT0": "21:15",
        "TR_INIT0_MUL": "23:22"
    },
    "PLL1_0": {
        "FSU": "23:0"
    },
    "PLL1_1": {
        "RSU": "23:0"
    },
    "PLL1_2": {
        "RTU": "13:0",
        "RSVD": "15:14",
        "TR_EDU": "23:16"
    },
    "PLL1_3": {
        "APU": "11:0",
        "APD": "23:12"
    },
    "PLL1_4": {
        "FSD": "23:0"
    },
    "PLL1_5": {
        "RSD": "23:0"
    },
    "PLL1_6": {
        "RTD": "13:0",
        "RSVD": "15:14",
        "TR_EDD": "23:16"
    },
    "PLL1_7": {
        "REPS": "3:0",
        "SH_EN": "4",
        "RSVD": "7:5",
        "CONT_MODE": "8",
        "PD_MODE": "10:9",
        "TR_SED": "18:11",
        "TR_SED_MUL": "23:19"
    },
    "PLL2_7": {
        "REPS": "3:0",
        "SH_EN": "4",
        "RSVD": "7:5",
        "CONT_MODE": "8",
        "PD_MODE": "10:9",
        "TR_SED": "18:11",
        "TR_SED_MUL": "23:19"
    },
    "PLL3_7": {
        "REPS": "3:0",
        "SH_EN": "4",
        "RSVD": "7:5",
        "CONT_MODE": "8",
        "PD_MODE": "10:9",
        "TR_SED": "18:11",
        "TR_SED_MUL": "23:19"
    },
    "PLL4_7": {
        "REPS": "3:0",
        "SH_EN": "4",
        "RSVD": "7:5",
        "CONT_MODE": "8",
        "PD_MODE": "10:9",
        "TR_SED": "18:11",
        "TR_SED_MUL": "23:19"
    },
    "ADC1": {
        "RSVD": "15:0",
        "TR_PSSTART": "21:16",
        "SENSOR_SEL": "23:22"
    },
    "FD": {
        "CLK_SEL": "1:0",
        "DC_IN_ADJ": "6:2",
        "DC_OUT_ADJ": "10:7",
        "IRQ_FD_SEL": "11",
        "RSVD": "23:12"
    },
    "WU": {
        "TR_TWKUP": "7:0",
        "TR_TWKUP_MUL": "11:8",
        "RSVD": "23:12"
    }
}

prompt_2 = f'''Your Job is to map the binary value given to the symbols based on the index.
The given bit indexes start from 0 and ends at 31.
Start mapping values from index 0 , LSB side to index 31 on the MSB


Here is a example
### Input 

Value in binary is  0001 1100 0000 1110 0010 0000  (this should be taken from the fourth column on the above)

And the register map for MAIN register is:
LDO_MODE: Bit position 23
LOAD_STRENGTH: Bit positions 22-21
BG_CLK_DIV: Bit positions 20-19
SADC_CLKDIV: Bit positions 18-17
CW_MODE: Bit position 16
TR_WKUP_MUL: Bit positions 15-12
TR_WKUP: Bit positions 11-4
FIFO_RESET: Bit position 3
FSM_RESET: Bit position 2
SW_RESET: Bit position 1
FRAME_START: Bit position 0


### Output

LDO_MODE : 0x0
LOAD_STRENGTH : 0x0
BG_CLK_DIV : 0x3
SADC_CLKDIV : 0x2
CW_MODE : 0x0
TR_WKUP_MUL : 0x0
TR_WKUP : 0xE2
FIFO_RESET : 0x0
FSM_RESET : 0x0
SW_RESET : 0x0
FRAME_START : 0x0

Now its your turn, do the same for the below register taking the binary value from the fourth column. 

{register_name} 
'''

for key, value in register_map.get(register_name, {}).items():
    prompt_2 += f"{key}: {value}\n"

prompt_2 += f'''

Output the binary value for this register and also, the rest of the outputs on the .csv format.
'''


#test_chat_completion_api(step_1_prompt1,prompt_2)


def test_chat_completion_api(user_message, bot_message):     
    model='o3-mini'     
    completion = client.chat.completions.create(     
                    model=model,     
                    messages=[{"role": "user", "content": user_message},     
                              {"role":"assistant", "content": bot_message}],     
                    # max_tokens=256,     
                    stream=False,     
                    # temperature=0.7,       
                )   
    return completion.choices[0].message.content

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({"message": "Backend is running!", "status": "ok"})

@app.route('/api/process-registers', methods=['POST'])
def process_registers():
    print("API endpoint hit!")
    
    data = request.get_json()
    print(f"Received data: {data}")
    input_text = data.get('inputText', '')
    register_name = data.get('registerName', 'MAIN')
    print(f"Input text length: {len(input_text)}, Register: {register_name}")

    step_1_prompt1 = f"""Split the data into three columns and also create a new column converting the hexadecimal values in the third column to binary 

                        {input_text}

                        Also, provide the output in the .csv format
                        Reply with only the data in csv and nothing else
                    """
    #result = test_chat_completion_api("hi", step_1_prompt1)
    #print(f"AI API result: {result[:100] if result else 'None'}...")
    #return jsonify({"success": True, "data": result, "register": register_name})

    prompt_2 = f'''Your Job is to map the binary value given to the symbols based on the index.
            The given bit indexes start from 0 and ends at 31.
            Start mapping values from index 0 , LSB side to index 31 on the MSB
            
            Now its your turn, do the same for the below register taking the binary value from the fourth column. 
            {register_name} 
            '''
        
    for key, value in register_map.get(register_name, {}).items():
        prompt_2 += f"{key}: {value}\n"
        
    prompt_2 += f'''

    Output the binary value for this register and also, don't give me explanation.
    '''
    
    result = test_chat_completion_api("Hi",step_1_prompt1)
    prompt_2 = result + prompt_2
    print(prompt_2)
    final_result = test_chat_completion_api("Hi",prompt_2)
    print(f"AI API result: {final_result[:100] if final_result else 'None'}...")
    return jsonify({"success": True, "data": final_result, "register": register_name})

@app.route('/api/process-register', methods=['POST'])
def process_register():
    print("API endpoint hit!")
    try:
        data = request.get_json()
        print(f"Received data: {data}")
        input_text = data.get('inputText', '')
        register_name = data.get('registerName', 'MAIN')
        print(f"Input text length: {len(input_text)}, Register: {register_name}")

        step_1_prompt1 = f"""Split the data into three columns and also create a new column converting the hexadecimal values in the third column to binary 

{user_input_1}

Also, provide the output in the .csv format
Reply with only the data in csv and nothing else
"""
        result = test_chat_completion_api("hi", step_1_prompt1)
        print(result)
        
        # Update the prompt with the received register name
        prompt_2 = f'''Your Job is to map the binary value given to the symbols based on the index.
The given bit indexes start from 0 and ends at 31.
Start mapping values from index 0 , LSB side to index 31 on the MSB


Here is a example
### Input 

Value in binary is  0001 1100 0000 1110 0010 0000  (this should be taken from the fourth column on the above)

And the register map for MAIN register is:
LDO_MODE: Bit position 23
LOAD_STRENGTH: Bit positions 22-21
BG_CLK_DIV: Bit positions 20-19
SADC_CLKDIV: Bit positions 18-17
CW_MODE: Bit position 16
TR_WKUP_MUL: Bit positions 15-12
TR_WKUP: Bit positions 11-4
FIFO_RESET: Bit position 3
FSM_RESET: Bit position 2
SW_RESET: Bit position 1
FRAME_START: Bit position 0


### Output

LDO_MODE : 0x0
LOAD_STRENGTH : 0x0
BG_CLK_DIV : 0x3
SADC_CLKDIV : 0x2
CW_MODE : 0x0
TR_WKUP_MUL : 0x0
TR_WKUP : 0xE2
FIFO_RESET : 0x0
FSM_RESET : 0x0
SW_RESET : 0x0
FRAME_START : 0x0

Now its your turn, do the same for the below register taking the binary value from the fourth column. 

{register_name} 
'''
        
        for key, value in register_map.get(register_name, {}).items():
            prompt_2 += f"{key}: {value}\n"
        
        prompt_2 += f'''

Output the binary value for this register and also, the rest of the outputs on the .csv format.
'''
        
        # Create step_1_prompt with actual input text
        step_1_prompt = f"""Split the data into three columns and also create a new column converting the hexadecimal values in the third column to binary 

{input_text}

Also, provide the output in the .csv format
Reply with only the data in csv and nothing else
"""
        
        print("Calling AI API...")
        #result = test_chat_completion_api("Hi", "HEllo")
        print(f"AI API result: {result[:100] if result else 'None'}...")
        return jsonify({"success": True, "data": result, "register": register_name})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)