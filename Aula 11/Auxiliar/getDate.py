from datetime import datetime

def _getdate():
    
    now = datetime.now()
    
    date = now.strftime('%d/%m/%y')
    
    return date