import numpy as np
from scipy import ndimage

from gc2d.model.preferences import Preferences, PreferenceEnum
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
        self.preferences = Preferences()

    def get_palette(self):
        """
        :return: The palette of the model, or none if there is no model.
        """
        if self.model is not None:
            return self.model.palette

        return None

    def set_palette(self, palette):
        """
        :param palette: the color palette to set.
        :return: None
        """
        if self.model is not None:
            self.model.palette = palette
            self.notify('model.palette', self.model)

    def set_upper_bound(self, upper_bound):
        """
        :param upper_bound: The upper bound of the palette
        :return: The lower bound of the palette
        """
        if self.model is not None:
            self.model.upper_bound = upper_bound
            self.notify('model.upper_bound', self.model)

    def set_lower_bound(self, lower_bound):
        """
        :param lower_bound: The lower bound of the palette
        :return: The lower bound of the palette
        """
        if self.model is not None:
            self.model.lower_bound = lower_bound
            self.notify('model.lower_bound', self.model)

    def get_state(self):
        """ returns an array with the model data and the integration data for storage """
        return (
            self.model.get_2d_chromatogram_data(), 
            [integration.get_state() for integration in self.integrations.values()],
            self.preferences.get_state()
        )

    def set_model(self, arr):
        """
        Overwrites the model data and notifies listeners
        :param arr: numpy array with the data to be set as the new model
        :return: None
        """
        self.close_model()
        self.model = Model(arr, len(arr[0]))
        self.notify('model', self.model)  # Notify all observers.

    def import_model(self, file_name):
        """
        Loads the chromatogram data from a text file into a new model, omits last column (trailing commas).
        :param file_name: The name of the chromatogram file to open.
        :return: None
        """
        arr = np.genfromtxt(file_name, delimiter=',', dtype=np.float64)
        self.set_model(arr[:,:-1])
        
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
            

    def filter_gaussian(self, sigma):
        """
        Applies a Gaussian filter to the model and puts it in the convolution data.
        :param sigma: The standard deviation of the Gaussian filter.
        :return: None
        """

        self.model.set_convolved_data(ndimage.gaussian_filter(self.model.get_raw_data(), sigma, mode='constant'))
        self.notify('model', self.model)

    def toggle_convolved(self, convolved):
        """
        Toggle whether to show convolved data.
        :param convolved: A boolean signifying whether to show convolved data or not.
        :return: None
        """
        self.model.toggle_convolved(convolved)
        self.notify('model', self.model)

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
        :param label: an updated label
        :return: None
        """
        self.integrations[key].update(mask, label)
        self.notify('integrationUpdate', self.integrations[key])
    
    def toggle_show(self, key):
        """ 
        Toggle whether an integration is highlighted/showing in the 3D visualization
        :param key: the key of the toggled integration
        :return: None
        """
        self.integrations[key].toggle_show()
        self.notify('showIntegration', self.integrations[key])

    def clear_integration(self, key):
        """
        Removes an integration and notifies view that this has happened
        :param key: identifier of the integration to be removed
        :return: None
        """
        self.notify('removeIntegration', self.integrations[key])
        del self.integrations[key]

    def get_preference(self, which):
        """
        Gets a preference value, specified by which
        :param which: a PreferenceEnum object specifying which preference should be retrieved
        :return: the called preference value 
        """
        return self.preferences.get(which)
    
    def set_preference(self, which, value):
        """
        Sets a preference value, specified by which
        :param which: a PreferenceEnum object specifying which preference should be overwritten
        :return: None
        """
        self.preferences.set(which, value)
        
