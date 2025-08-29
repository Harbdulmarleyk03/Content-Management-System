import re 

BANNED_WORDS = ['buy now', 'click here', 'viagra', 'scam', 'xxx']
URL_PATTERN = r"http[s]?://"

def is_spam_content(text):
    text_lower = text.lower()

    for word in BANNED_WORDS:
        if word in text_lower:
            return True 
        
    if re.search(URL_PATTERN, text_lower):
        return True 
    
    if re.search(r'(.)\1{5,}', text_lower):
        return True 
    return False