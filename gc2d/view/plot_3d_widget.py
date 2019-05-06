import pyqtgraph.opengl as gl
from pyqtgraph.opengl import GLViewWidget

from gc2d.controller.listener.plot_3d_listener import Plot3DListener
from gc2d.view.palette.shader import PaletteShader


class Plot3DWidget(GLViewWidget):

    def __init__(self, model_wrapper, parent=None):
        """
        The Plot2DWidget is responsible for rendering the 2D chromatogram data.
        :param model_wrapper: the wrapper of the model.
        :param parent: the parent of this Widget.
        """
        super().__init__(parent=parent)
        self.listener = Plot3DListener(self, model_wrapper)
        self.setCameraPosition(distance=400)

        self.surface = gl.GLSurfacePlotItem(computeNormals=False)
        # This will need to be done dynamically later. TODO
        self.surface.scale(1, 1, 0.00001)
        self.addItem(self.surface)

        self.translation_x, self.translation_y = 0, 0


        if model_wrapper.model is not None: 
            self.notify('model', model_wrapper.model)

        model_wrapper.add_observer(self, self.notify)

    def notify(self, name, value):
        """
        Updates the image rendered to match the model.
        :return: None
        """
        if name == 'model':
            if value is None:
                self.setVisible(False)
            else:
                if not self.isVisible():
                    prev_x, prev_y = self.translation_x, self.translation_y
                    self.translation_x = -len(value.get_2d_chromatogram_data()) / 2
                    self.translation_y = -len(value.get_2d_chromatogram_data()[0]) / 2
                    self.surface.translate(self.translation_x - prev_x, self.translation_y - prev_y, 0)
                    self.surface.setData(z=value.get_2d_chromatogram_data())
                    self.setVisible(True)
                self.surface.setShader(PaletteShader(value.lower_bound, value.upper_bound, value.palette))
        if name == 'model.palette':
            self.surface.setShader(PaletteShader(value.lower_bound, value.upper_bound, value.palette))
