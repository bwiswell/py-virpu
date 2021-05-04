from .component import Component
from .ioport import IOPort
from ..signal.signal import Signal

class Delayer(Component):
    '''
    A class to represent a signal delayer that extends Component.

    This class is a functional component that delays a signal for a custom
    number of ticks.
    '''

    def __init__(self):
        '''Initialize the Delayer object and extend Component.'''
        in_ports = [IOPort('data', 'any', 'in')]
        out_ports = [IOPort('data', 'any', 'out')]

        Component.__init__(self,
                            comp_name='Delayer',
                            in_ports=in_ports,
                            out_ports=out_ports,
                            cycles=4,
                            config_options='wsct'
                        )

    def _get_width(self) -> int:
        '''Get the bit width of the component.'''
        return super()._get_width()

    def _set_width(self, val:int) -> None:
        '''Set the bit width of the component.'''
        super()._set_width(val)
        self.in_by_id['data'].width = self._width
        self.out_by_id['data'].width = self._width

    width = property(_get_width, _set_width)

    def _get_signed(self) -> bool:
        '''Get the signage of the component.'''
        return super()._get_signed()

    def _set_signed(self, val:bool) -> None:
        '''Set the signage of the component.'''
        super()._set_signed(val)
        self.in_by_id['data'].signed = self._signed
        self.out_by_id['data'].signed = self._signed

    signed = property(_get_signed, _set_signed)

    def execute(self) -> None:
        '''
        Execute the delayer's functional logic.

        The delayer delays a signal for a custom number of ticks.
        '''
        self.out_by_id['data'].value = self.in_by_id['data'].value