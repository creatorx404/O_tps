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
    
    # Detect operator from phone prefix
    def get_operator(phone_num):
        prefix = phone_num[1:4]  # Get first 3 digits after 0
        
        # Jazz prefixes: 300-305, 310, 320-324, 342
        jazz_prefixes = ['300', '301', '302', '303', '304', '305', '310', '320', '321', '322', '323', '324', '342']
        # Telenor prefixes: 340-347, 345
        telenor_prefixes = ['340', '341', '343', '344', '345', '346', '347']
        # Zong prefixes: 310-318, 331-334
        zong_prefixes = ['311', '312', '313', '314', '315', '316', '317', '318', '331', '332', '333', '334']
        # Ufone prefixes: 330, 331, 333, 336
        ufone_prefixes = ['330', '335', '336']
        
        if prefix in jazz_prefixes:
            return '1'  # Jazz
        elif prefix in telenor_prefixes:
            return '2'  # Telenor
        elif prefix in zong_prefixes:
            return '3'  # Zong
        elif prefix in ufone_prefixes:
            return '4'  # Ufone
        else:
            return '5'  # Default/Unknown
    
    # Try detected operator first, then all others
    detected_operator = get_operator(clean_phone)
    operators_to_try = [detected_operator]
    
    # Add all other operators
    all_operators = ['1', '2', '3', '4', '5']
    for op in all_operators:
        if op not in operators_to_try:
            operators_to_try.append(op)
    
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
    
    data = {
        'uuid': clean_phone,
    }
    
    # Try each operator
    for operator in operators_to_try:
        try:
            params = {
                'siteid': '',
                'selOperator': operator,
            }
            
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
                (response_data.get('respCode') == '00' and 'otpsent' in str(response_data).lower())):
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
            
            # If this operator failed but not rate limited, try next operator
            # Small delay between attempts
            if operator != operators_to_try[-1]:  # Not the last one
                await asyncio.sleep(0.5)
                continue
        
        except Exception as e:
            # If error on this operator, try next one
            if operator != operators_to_try[-1]:  # Not the last one
                await asyncio.sleep(0.5)
                continue
            else:
                # Last operator also failed
                out.append({
                    "name": name,
                    "domain": domain,
                    "frequent_rate_limit": frequent_rate_limit,
                    "rateLimit": False,
                    "sent": False,
                    "error": True
                })
                return None
    
    # All operators tried, none succeeded
    out.append({
        "name": name,
        "domain": domain,
        "frequent_rate_limit": frequent_rate_limit,
        "rateLimit": False,
        "sent": False,
        "error": False
    })
    return None
