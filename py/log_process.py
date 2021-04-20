def logtext(path,text):
    from datetime import datetime
    log = open(path,'a')
    log.write(text +' '+ str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')) +'\n')
    log.close()