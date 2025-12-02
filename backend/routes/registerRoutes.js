const express = require('express');
const router = express.Router();
const https = require('https');
const axios = require('axios');

// Register map data
const registerMap = {
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
  }
};

// Token management
let cachedToken = null;
let tokenExpiry = null;

async function getGPT4IFXToken() {
  const username = process.env.GPT4IFX_USERNAME;
  const password = process.env.GPT4IFX_PASSWORD;
  
  if (!username || !password) {
    throw new Error('GPT4IFX credentials not configured');
  }

  if (cachedToken && tokenExpiry && Date.now() < tokenExpiry) {
    return cachedToken;
  }

  try {
    const auth = Buffer.from(`${username}:${password}`).toString('base64');
    
    const response = await axios.get('https://gpt4ifx.icp.infineon.com/auth/token', {
      headers: {
        'Authorization': `Basic ${auth}`,
        'User-Agent': 'IFX-MSD-GenAI-Tool/1.0',
        'Accept': 'application/json'
      },
      httpsAgent: new https.Agent({ rejectUnauthorized: false }),
      timeout: 30000
    });

    cachedToken = response.data.trim();
    tokenExpiry = Date.now() + (3600 * 1000); // 1 hour
    return cachedToken;
  } catch (error) {
    throw new Error(`Failed to get GPT4IFX token: ${error.message}`);
  }
}

async function callGPT4IFX(prompt) {
  const token = await getGPT4IFXToken();
  
  try {
    const response = await axios.post('https://gpt4ifx.icp.infineon.com/v1/chat/completions', {
      model: "gpt-4",
      messages: [
        { role: "system", content: "You are a very logical AI" },
        { role: "user", content: prompt }
      ],
      max_tokens: 2000,
      temperature: 0.7
    }, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      httpsAgent: new https.Agent({ rejectUnauthorized: false }),
      timeout: 60000
    });

    return response.data.choices[0].message.content;
  } catch (error) {
    throw new Error(`GPT4IFX API error: ${error.message}`);
  }
}

// Process registers endpoint
router.post('/process-registers', async (req, res) => {
  try {
    const { inputText, registerName = 'MAIN' } = req.body;
    
    if (!inputText) {
      return res.status(400).json({ success: false, error: 'Input text required' });
    }

    const step1Prompt = `Split the data into three columns and also create a new column converting the hexadecimal values in the third column to binary 

${inputText}

Also, provide the output in the .csv format
Reply with only the data in csv and nothing else`;

    const step1Result = await callGPT4IFX(step1Prompt);
    
    let step2Prompt = `Your Job is to map the binary value given to the symbols based on the index.
The given bit indexes start from 0 and ends at 31.
Start mapping values from index 0, LSB side to index 31 on the MSB

Now its your turn, do the same for the below register taking the binary value from the fourth column.

${registerName}
`;

    const regMap = registerMap[registerName] || {};
    for (const [key, value] of Object.entries(regMap)) {
      step2Prompt += `${key}: ${value}\n`;
    }

    step2Prompt += '\nOutput the binary value for this register and also, don\'t give me explanation.';
    
    const finalPrompt = step1Result + '\n\n' + step2Prompt;
    const finalResult = await callGPT4IFX(finalPrompt);

    res.json({
      success: true,
      data: finalResult,
      register: registerName
    });

  } catch (error) {
    console.error('Register processing error:', error);
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

module.exports = router;