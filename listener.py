
class Listener():
    """ 
    Abstract for making classes that can recieve messages from ChatLogger.
    Supply:
        recieveMessage(self, username, message):
        
    """
    
    # Called by ChatLogger when a new message appears
    def recieveMessage(self, username, message, admin):
        raise NotImplementedError("Listener.recieveMessage() not implemented")

