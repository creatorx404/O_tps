from O_tps.core import *
from O_tps.localuseragent import *

async def bajao(phone, client, out):
    name = "bajao"
    domain = "bajao.pk"
    frequent_rate_limit = False
    
    # Remove country code, keep last 10 digits
    clean_phone = phone.replace('+92', '').replace('+91', '').replace(' ', '')[-10:]
    # Add leading 0 if not present
    if not clean_phone.startswith('0'):
        clean_phone = '0' + clean_phone
    
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://bajao.pk',
        'Referer': 'https://bajao.pk/create',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    
    # selOperator=5 might be for different carriers
    # You can try different values: 1=Jazz, 2=Telenor, 3=Zong, 4=Ufone, 5=?
    params = {
        'siteid': '',
        'selOperator': '5',
    }
    
    data = {
        'uuid': clean_phone,
    }
    
    try:
        response = await client.post(
            'https://bajao.pk/api/v2/login/generatePinV2',
            params=params,
            headers=headers,
            data=data,
        )
        
        try:
            response_data = response.json()
        except:
            response_data = {}
        
        response_text = response.text.lower()
        
        # Check for success
        if (response_data.get('isSuccess') == True or 
            'pin has been sent' in response_text or
            'otp has been sent' in response_text or
            'sms' in response_text and 'sent' in response_text or
            response_data.get('respCode') == '00'):
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": True,
                "error": False
            })
            return None
        
        # Check for rate limit
        elif ('rate' in response_text or 
              'limit' in response_text or 
              'too many' in response_text or 
              'wait' in response_text):
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": True,
                "sent": False,
                "error": False
            })
            return None
        
        # Unknown response
        else:
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": False,
                "error": False
            })
            return None
            
    except Exception as e:
        out.append({
            "name": name,
            "domain": domain,
            "frequent_rate_limit": frequent_rate_limit,
            "rateLimit": False,
            "sent": False,
            "error": True
        })
        return None
