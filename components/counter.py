from .component import Component
from .ioport import IOPort
from ..signal.signal import Signal

class Counter(Component):
    '''
    A class to represent an incrementing counter that extends Component.

    This class is a functional logic component that counts upwards from a
    custom value.
    '''

    def __init__(self):
        '''Initialize Counter object and extend Component.'''
        out_ports = [IOPort('data', 'any', 'out', 16, False)]
        Component.__init__(self,
                            comp_name='Counter',
                            out_ports=out_ports,
                            cycles=4,
                            config_options='vwst'
                        )
        
        self.width = 16
        self.signed = False

    def _get_width(self) -> int:
        '''Get the bit width of the component.'''
        return super()._get_width()

    def _set_width(self, val:int) -> None:
        '''Set the bit width of the component.'''
        super()._set_width(val)
        self.out_by_id['data'].width = self._width

    width = property(_get_width, _set_width)

    def _get_signed(self) -> bool:
        '''Get the signage of the component.'''
        return super()._get_signed()

    def _set_signed(self, val:bool) -> None:
        '''Set the signage of the component.'''
        super()._set_signed(val)
        self.out_by_id['data'].signed = self._signed

    signed = property(_get_signed, _set_signed)

    def _execute(self) -> None:
        '''
        Execute the counter's functional logic.

        The counter counts upwards from a custom value.
        '''
        self.out_by_id['data'].value = self._value
        self._value, _ = self._value + 1