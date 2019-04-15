

class Handler():

    def __init__(self, model_wrapper):
        self.model_wrapper = model_wrapper
    
    def clear_value(self, key):
        """
        Removes an integration from the model wrapper
        :return: None
        """
        self.model_wrapper.clear_integration(key)
    
    def change_label(self, key, new_label):
        """
        Takes an edited label and saves this to the appropriate Integration object in the model_wrapper
        :return: None
        """
        self.model_wrapper.update_integration(key, label=new_label)
