
class Listener:
    """ 
    Abstract for making classes that can receive messages from ChatLogger.
    Supply:
        receive_message(self, username, message, adminm, player):
        
    """
    
    # Called by ChatLogger when a new message appears
    def receive_message(self, username, message, admin, player):
        raise NotImplementedError("Listener.receive_message() not implemented")

