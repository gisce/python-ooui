

class Graph(object):
    def __init__(self, element):
        """

        :param element: lxml.etree._Element
        """
        self._string = element.get('string')
        self._timerange = element.get('timerange', None)

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
    def type(self):
        return self._type
