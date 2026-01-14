from O_tps.core import *
from O_tps.localuseragent import *
import json

async def jazztv(phone, client, out):
    name = "jazztv"
    domain = "jazztv.pk"
    frequent_rate_limit = False
    
    # Format phone: need full number with 92 prefix, no +
    clean_phone = phone.replace('+', '').replace(' ', '')
    if not clean_phone.startswith('92'):
        # Remove leading 0 if present and add 92
        clean_phone = clean_phone.lstrip('0')
        clean_phone = '92' + clean_phone
    
    # Detect telco/operator
    def detect_telco(phone_num):
        # Get the prefix after 92
        if phone_num.startswith('92'):
            prefix = phone_num[2:5]  # Get first 3 digits after 92
        else:
            prefix = phone_num[1:4]
        
        jazz_prefixes = ['300', '301', '302', '303', '304', '305', '310', '320', '321', '322', '323', '324', '342']
        telenor_prefixes = ['340', '341', '343', '344', '345', '346', '347']
        zong_prefixes = ['311', '312', '313', '314', '315', '316', '317', '318']
        ufone_prefixes = ['330', '335', '336','331', '332', '333', '334']
        
        if prefix in jazz_prefixes:
            return 'jazz'
        elif prefix in telenor_prefixes:
            return 'telenor'
        elif prefix in zong_prefixes:
            return 'zong'
        elif prefix in ufone_prefixes:
            return 'ufone'
        else:
            return 'other'
    
    telco = detect_telco(clean_phone)
    
    # Guest token - this might need to be refreshed periodically
    # For now using a static guest token
    guest_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJZR2M2c0FXT2t1YlpfOTAzV0syZHZOMEc2enhnUFZUX25HUnZ3TjNzdDNvIn0.eyJleHAiOjE3NjkxNzY0MDMsImlhdCI6MTc2ODMxMjQwMywianRpIjoiMzEzODM2ZDQtNzZmNi00ZDI2LTk0NmEtNzhiYjc4NGNhZmQ3IiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay5qYXp6dHYucGs6ODQ0My9yZWFsbXMvVGFtYXNoYSIsImF1ZCI6WyJvdC10b2tlbi1jbGllbnQiLCJhY2NvdW50Il0sInN1YiI6IjE5YzM4OTJmLTJmNjctNDdiNy1hZjIyLWI2ODAwNzdhMjFmMiIsInR5cCI6IkJlYXJlciIsImF6cCI6IlRhbWFzaGFBcHAiLCJzaWQiOiJiYTEwY2I5MC00MzVkLTQzNjMtODFhOC0xNmU3MjVjNDRkZGEiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIi8qIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJvZmZsaW5lX2FjY2VzcyIsImRlZmF1bHQtcm9sZXMtdGFtYXNoYSIsImd1ZXN0IiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6InByb2ZpbGUgZW1haWwiLCJjb3VudHJ5IjoiUEsiLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsIm5hbWUiOiJTaG9haWIgR3Vlc3QiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJzaG9haWIuYWhzYW5AY29udmV4aW50ZXJhY3RpdmVlLmNvbSIsInJlZ2lvbiI6IkRFRkFVTFQiLCJnaXZlbl9uYW1lIjoiU2hvYWliIiwiZmFtaWx5X25hbWUiOiJHdWVzdCIsImVtYWlsIjoic2hvYWliLmFoc2FuQGNvbnZleGludGVyYWN0aXZlZS5jb20ifQ.kzhzfJ7lW0qNOTvmshHwewqFwGiV0jOOwkCa-XTcyZOJVZcWsy40fq3ya4Y6Jf_w1UYeicq4G-T_eTntt3hU2Hbi8xRwodYg2flxQZPfBNn19hQWJ2b-BkKamHxy9j1QH4-1lWjOvbB8D3nBcCodZ9RgMaNw0mDBfrVK0SQGjkwtHRPoVpWiIm4bbeZPZ6nTo-6b5vFQDVL0j5s8laJw5t_R4o-B3V0Ky4sVT5hcEfurDs2qfBJbBABUOINOwojaeDH112yR-ge6nX6IHecPZUkuAoSUcZjZ9ddSaWagEZzjh5Hk9s-Y0P9MJY9gbDZMv74TmpmAlIt042tAMNRLtg"
    
    headers = {
        'User-Agent': random.choice(ua["browsers"]["chrome"]),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Authorization': f'Bearer {guest_token}',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://tamashaweb.com',
        'Referer': 'https://tamashaweb.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
    }
    
    payload = {
        "from_screen": "signUp",
        "device": "Google Chrome",
        "telco": telco if telco != 'other' else 'other',
        "device_id": "web",
        "is_header_enrichment": "no",
        "other_telco": telco if telco == 'other' else telco,
        "mobile": clean_phone,
        "phone_details": "web"
    }
    
    try:
        response = await client.post(
            'https://web.jazztv.pk/alpha/api_gateway/index.php/v5/users-dbss/sign-up-wc',
            headers=headers,
            json=payload,
        )
        
        try:
            response_data = response.json()
        except:
            response_data = {}
        
        response_text = response.text.lower()
        
        # Check for success - API returns encrypted data with code 200
        if (response_data.get('code') == 200 or 
            response_data.get('eData') or
            'adata' in response_data or
            response.status_code == 200 and len(response_text) > 50):
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
        
        # Check for errors
        elif (response_data.get('code') != 200 or
              'error' in response_text or
              'fail' in response_text):
            out.append({
                "name": name,
                "domain": domain,
                "frequent_rate_limit": frequent_rate_limit,
                "rateLimit": False,
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
