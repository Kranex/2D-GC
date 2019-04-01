from PyQt5.Qt import QObject
from pyqtgraph import PolyLineROI 

class Selector(QObject):

    def __init__(self, parent, model_wrapper):
        """ 
        Selector draws a Region of Interest, and sends + updates the selected region as mask to the model.
        :param parent: The parent widget
        :param model_wrapper: The Model Wrapper
        """
        super().__init__(parent.window)
        self.window = parent
        self.model_wrapper = model_wrapper
        self.draw()
        
    def draw(self):
        """
        Draw region of interest (ROI)
        the ROI is connected to save(self) which is called every time the ROI has been edited
        :return: None
        """
        self.roi = PolyLineROI([[80, 60], [90, 30], [60, 40]], pen=(6,9), closed=True) 
        self.window.plot_2d.widget.addItem(self.roi)
        self.roi.sigRegionChangeFinished.connect(self.update_mask)
        self.id = self.model_wrapper.add_integration(self.get_region(), self)

    def update_mask(self):
        """
        Updates region mask in model 
        :return: None
        """
        self.model_wrapper.update_integration(self.id, mask=self.get_region())

    def update_label(self, string):
        self.model_wrapper.update_integration(self.currentRow(), label=string)

    def clearValue(self, row):
        self.window.plot_2d.removeItem(self.roi)
        self.model_wrapper.clear_integration(row)

    def get_region(self):
        """
        generates a mask for ROI region of the current chromatogram
        :return: The generated mask of the chromatogram 
        """
        return self.roi.getArrayRegion(self.model_wrapper.model.get_2d_chromatogram_data(), self.window.plot_2d.img)

    def destroy(self):
        fixed = self.roi.getSceneHandlePositions()
        return fixed