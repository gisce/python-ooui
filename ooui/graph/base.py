

class Graph(object):
    def __init__(self, element):
        """

        :param element: lxml.etree._Element
        """
        self._string = element.get('string')
        self._timerange = element.get('timerange', None)
        self._x_range = element.get('x_range', 'default')
        self._y_range = element.get('y_range', "default")
        self._y_zoom = element.get('y_zoom', 'none')
        self._y_zoom_explicit = element.get('y_zoom') is not None

        interval = element.get('interval', None)
        self._interval = int(interval) if interval is not None else 1

        self._type = None

    @property
    def string(self):
        return self._string

    @property
    def timerange(self):
        return self._timerange

    @property
    def interval(self):
        return self._interval

    @property
    def y_range(self):
        return self._y_range

    @property
    def y_zoom(self):
        return self._y_zoom

    @property
    def y_zoom_explicit(self):
        return self._y_zoom_explicit

    @property
    def x_range(self):
        return self._x_range

    @property
    def type(self):
        return self._type

    @property
    def fields(self):
        return []

    def process(self, values, fields, options=None):
        raise NotImplementedError
