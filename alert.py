import requests, json, time, os

## Client: configure alert types
path = 'https://alert-api.coinscious.org/alerts'
url  = path+'/configurations'



def authenticate():

    with open('./authen.json', 'r') as f:
        authen_info = json.load(f)
    
    # client: get/refresh token
    credential_dict = {"handle":authen_info['username'], "password":authen_info['password']}

    response_ = requests.post('https://auth-api.coinscious.org/auth/access-token', headers={"Content-Type": "application/json"}, data=json.dumps(credential_dict))
    return response_


def get_alert_list():
    
    ## Add Alert Signals
    body =[
            {
                "alertType": "price",
                "key": "priceDump",
                "exchange": "binance",
                "pair": "btc_usdt"
            },
            {
                "alertType": "price",
                "key": "priceDump",
                "exchange": "binance",
                "pair": "xrp_usdt"
            },
            {
                "alertType": "price",
                "key": "pricePump",
                "exchange": "binance",
                "pair": "btc_usdt"
            },
            {
                "alertType": "price",
                "key": "pricePump",
                "exchange": "binance",
                "pair": "xrp_usdt"
            },
            {
                "alertType": "rsi",
                "key": "overbought",
                "exchange": "binance",
                "pair": "btc_usdt"
            }
    ]
    return body

if __name__ == '__main__':

    response_ = authenticate()
    alert_list = get_alert_list()


    headers = {"Content-Type": "application/json", "Authorization" : "Bearer %s" % response_.json()['token']}
    response = requests.post(url, headers=headers, data=json.dumps(alert_list))
   
    ## Making sure there is no error
    assert(response.status_code==200)
    
    response_track = None 
    while True:
        
        time.sleep(10)
        
        # client: get latest alerts every 15m
    
        url = path+'/latest'
    
        response_alerts = requests.get(url, headers=headers)
        response_alert_json = response_alerts.json()
    
        if response_alerts.status_code != 200:
            print(response_alert_json)
            break
        else:
            if response_alert_json!=response_track:
                print(response_alert_json)
                response_track=response_alert_json
            else:
                print('no new alert within this 10s')
        
        
