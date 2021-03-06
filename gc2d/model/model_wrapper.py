import numpy as np

from gc2d.model.integration import Integration
from gc2d.model.model import Model
from gc2d.model.preferences import PreferenceEnum, Preferences
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

    def set_palette(self, palette):
        """
        :param palette: the color palette to set.
        :return: None
        """
        if self.model is not None:
            self.set_preference(PreferenceEnum.PALETTE, palette)
            self.model.palette = palette
            self.notify('model.palette', self.model)

    def set_upper_bound(self, upper_bound):
        """
        :param upper_bound: The upper bound of the palette
        :return: The lower bound of the palette
        """
        if self.model is not None:
            self.set_preference(PreferenceEnum.UPPER_BOUND, upper_bound)
            self.model.upper_bound = upper_bound
            self.notify('model.upper_bound', self.model)

    def set_lower_bound(self, lower_bound):
        """
        :param lower_bound: The lower bound of the palette
        :return: The lower bound of the palette
        """
        if self.model is not None:
            self.set_preference(PreferenceEnum.LOWER_BOUND, lower_bound)
            self.model.lower_bound = lower_bound
            self.notify('model.lower_bound', self.model)

    def get_state(self):
        """ returns an array with the model data and the integration data for storage """
        return (
            self.model.get_raw_data(),
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
        self.set_lower_bound(self.model.lower_bound)
        self.set_upper_bound(self.model.upper_bound)
        self.notify('model', self.model)  # Notify all observers.

    def import_model(self, file_name):
        """
        Loads the chromatogram data from a text file into a new model, omits last column (trailing commas).
        :param file_name: The name of the chromatogram file to open.
        :return: None
        """
        arr = np.genfromtxt(file_name, delimiter=',', dtype=np.float64)
        self.set_model(arr[:, :-1])

    def close_model(self):
        """
        Sets the model to None, effectively closing the chromatogram without closing the program.
        :return: None
        """
        if self.model is not None:
            self.model = None
            self.notify('model', self.model)  # Notify all observers
            keys = [key for key in self.integrations]
            for key in keys:
                self.clear_integration(key)
            self.integrate_id = 0

    def set_transform(self, transform):
        """
        Applies a transform to the model and puts it in the convolution data.
        :param transform: a Transform object (that has a transform method that takes and returns a 2d numpy array)
        :return: None
        """
        self.model.set_convolved_data(transform.transform(self.model.get_raw_data()))
        self.set_preference(PreferenceEnum.TRANSFORM, transform)
        self.notify('model', self.model)
        self.recompute_integrations()

    def toggle_convolved(self, convolved):
        """
        Toggle whether to show convolved data.
        :param convolved: A boolean signifying whether to show convolved data or not.
        :return: None
        """
        self.model.toggle_convolved(convolved)
        self.notify('model.viewTransformed', self.model)
        self.recompute_integrations()

    def add_integration(self, selector, key):
        """
        Appends a new integration data object to the self.integrations, with generated label
        Notifies the view that integration values have changed
        :param selector: Selector object, drawing a region of interest in a plot2d
        :param key: TODO What is this?
        :return index: the index of this integration, to be used as identifier
        """
        self.integrations[key] = Integration(key, selector)
        self.notify('newIntegration', self.integrations[key])
        self.set_current(key)

    def set_current(self, key):
        """
        If a single integration area is being edited, all are faded except the current, which is highlighted in view
        :param key: the key of the current ROI
        :return: None
        """
        for curr_key in self.integrations:
            self.set_show(curr_key, curr_key == key)

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

    def recompute_integrations(self):
        for integration in self.integrations.values():
            integration.recompute()

    def set_show(self, key, mode):
        """ 
        Toggle whether an integration is highlighted/showing in the 3D visualization
        Only updates view if a the show has actually toggled
        :param key: the key of the toggled integration
        :param mode: the bool value to set show to
        :return: None
        """
        changed = self.integrations[key].set_show(mode)
        if changed:
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
        self.notify(which.name, value)
