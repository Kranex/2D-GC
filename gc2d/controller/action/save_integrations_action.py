import json

from PyQt5.QtWidgets import QAction, QFileDialog


class SaveIntegrationsAction(QAction):

    def __init__(self, parent, model_wrapper, shortcut=None):
        """
        A SaveIntegrationsAction is a QAction that when triggered, saves the integration areas.
        It will open a file dialog to ask for a path, and save the areas in *gcgc files in json format
        :param parent: The parent widget
        :param model_wrapper: The Model Wrapper
        """
        super().__init__('Save integration areas', parent)
        self.window = parent
        self.model_wrapper = model_wrapper
        if shortcut is not None:
            self.setShortcut(shortcut)
        self.setStatusTip('Save integration areas')
        self.triggered.connect(self.save)

    def save(self):
        """
        Asks for a path via a file dialog, Writes the integration areas in the specified path as json format.
        :param path: the path to write the data to
        :return: None
        """
        path = QFileDialog.getSaveFileName(self.window, 'Save GCxGC integrations',
                                           filter='GCxGC file (*.gcgc);; All files (*.*)')[0]
        if path is not '':
            _model, integrations, _preferences = self.model_wrapper.get_state()
            with open(path, 'w') as save_fd:
                json.dump({"integrations": integrations},
                          save_fd, separators=(',', ':'), sort_keys=True, indent=4)
