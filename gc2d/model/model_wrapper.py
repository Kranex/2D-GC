import numpy as np

from gc2d.model.integration import Integration
from gc2d.model.model import Model
from gc2d.observable import Observable


class ModelWrapper(Observable):

    def __init__(self):
        """
        The model wrapper is responsible for facilitating complex interaction with the model.
        """
        super().__init__()
        self.model = None
        """The model containing all information relating to the chromatogram"""
        self.integrations = {}
        self.integrate_id = 0

    def set_palette(self, palette):
        """
        :param palette:
        :return:
        """
        self.model.palette = palette
        self.notify('model.palette', self.model)

    def save_model(self, location):
        """
        Later in development we may wish to save the settings of the program to file.
        :param location: The location to save to.
        :return: None
        """

        # Insert some hook to the save/load module.
        print("ModelWrapper.save_model() not yet implemented.")

    def load_model(self, file_name):
        """
        Loads the chromatogram data into a new model.
        Later in development this may be responsible for loading more than just the chromatogram data.
        :param file_name: The name of the chromatogram file to open.
        :return: None
        """
        self.close_model()
        data = []
        with open(file_name) as sourcefile:
            for line in sourcefile:
                row = [float(val.strip()) for val in line.split(",") if val.strip()]
                data.append(row)
        arr = np.array(data, dtype=np.float64)

        self.model = Model(arr, len(data[0]))

        self.notify('model', self.model)  # Notify all observers.

    def close_model(self):
        """
        Sets the model to None, effectively closing the chromatogram without closing the program.
        :return: None
        """
        if (self.model is not None):
            self.model = None
            self.notify('model', self.model)  # Notify all observers
            keys = [key for key in self.integrations]
            for key in keys:
                self.clear_integration(key)
            self.integrate_id = 0
            

    def add_integration(self, selector, key):
        """
        Appends a new integration data object to the self.integrations, with generated label
        Notifies the view that integration values have changed
        :param mask: a selection mask of the chromatogram
        :param selector: Selector object, drawing a region of interest in a plot2d
        :return index: the index of this integration, to be used as identifier
        """
        self.integrations[key] = Integration(key, selector)
        self.notify('newIntegration', self.integrations[key])
    
    def get_new_key(self):
        """
        Generates a new identifier for an integration value
        :return: a unique identifier 
        """
        self.integrate_id += 1
        return self.integrate_id - 1

    def update_integration(self, key, mask=None, label=None):
        """
        Update an integration mask, and notifies the view that integration values have been changed
        :param key: the key of the altered integration
        :param mask: an updated mask
        :parame label: an updated label
        :return: None
        """
        self.integrations[key].update(mask, label)
        self.notify('integrationUpdate', self.integrations[key])
    
    def toggle_show(self, key):
        #still in progress, should show integration in view
        self.notify('toggleIntegration', self.integrations[key])

    def clear_integration(self, key):
        """
        Removes an integration and notifies view that this has happened
        :param key: identifier of the integration to be removed
        :return: None
        """
        self.notify('removeIntegration', self.integrations[key])
        del self.integrations[key]
