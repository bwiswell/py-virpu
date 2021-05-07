from .component import Component
from .ioport import IOPort

class Incrementer(Component):
    '''
    A class to represent a value incrementer that extends Component.
    
    This class is a functional logic component that adds 1 to an incoming
    value.
    '''
    
    def __init__(self):
        '''Initialize the Incrementer object and extend Component.'''
        in_ports = [IOPort('data', 'any', 'in', 16, False)]
        out_ports = [IOPort('data', 'any', 'out', 16, False)]
        Component.__init__(self,
                            comp_name='Incrementer',
                            in_ports=in_ports,
                            out_ports=out_ports,
                            config_options='ws'
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

    def _execute(self) -> None:
        '''
        Execute the incrementer's function logic.

        The incrementer adds 1 to an incoming value.
        '''
        value = self.in_by_id['data'].value
        value, _ = value + 1
        self.out_by_id['data'].value = value