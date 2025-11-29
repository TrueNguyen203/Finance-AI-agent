# Finance AI Agents

## Table of Contents
- [Description](#description)
- [Tech](#tech)
- [How to run the code](#how-to-run-the-code)
- [Author](#author)

## Description
This is my personal project. My aim is to create an AI agents that can retrive vietnamese stock data and perform some calculation on it like SMA, RSI and MACD. Other than the demo image, you guy can check longer demo in the `auto_question_test_results.txt` file.

![](demo_image.png)

## Tech:
- I am using the vnstock api to retrieve vietnamese stock data in real time. You guy can read the documentation of the api at [https://vnstocks.com/docs](https://vnstocks.com/docs). </br>
- The tools for the agent are cusomize base on the API that I have mentioned above. </br>
- The model I use is `gpt-oss:120b-cloud` using through Ollama. </br>


## How to run the code:
1. Clone the repository </br> 
   `git clone https://github.com/TrueNguyen203/Finance-AI-agent.git` </br>
   
2. Set up the model </br>
   - Download Ollama at [https://ollama.com/](https://ollama.com/) and open it in your computer </br>
   - Login in to your account </br>
   - You may need to ask it 1 question with the model `gpt-oss:120b-cloud` or else you can run ollama pull `gpt-oss:120b-cloud` </br>
   
3. Setup the virtual environment </br>
`python -m venv venv_name` </br>
`venv_name\Scripts\activate` </br>
`pip install -r requirements.txt` </br>

4. Run the app </br>
`python src/index.py`

##  Author
- Chu Cao Nguyen - nguyenmilan203@gmail.com
  
