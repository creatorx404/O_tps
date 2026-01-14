from O_tps.core import *
from O_tps.localuseragent import *
async def pakwheels(phone, client, out):
    name = "pakwheels"
    domain = "pakwheels.com"
    frequent_rate_limit = False
    
    # Remove country code, keep last 10 digits
    clean_phone = phone.replace('+92', '').replace('+91', '').replace(' ', '')[-10:]
    
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.pakwheels.com',
        'Referer': 'https://www.pakwheels.com/',
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    data = {
        'mobile_number': clean_phone,
        'country_code': '+92',
        'is_popup_request': 'true'
    }
    
    try:
        response = await client.post(
            'https://www.pakwheels.com/login-with-mobile',
            headers=headers,
            data=data,
        )
        
        try:
            response_data = response.json()
        except:
            response_data = {}
        
        response_text = response.text.lower()
        
        # Success: response contains pin_id
        if response_data.get('pin_id') or 'pin_id' in response_text:
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
                "sent": True,
                "error": False
            })
            return None
        
        elif 'rate' in response_text or 'limit' in response_text or 'too many' in response_text:
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": True,
                "sent": False,
                "error": False
            })
            return None
        
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
