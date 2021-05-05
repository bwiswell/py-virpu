from .component import Component
from .ioport import IOPort

class Constant(Component):
    '''
    A class to represent a custom constant value that extends Component.
    
    This class is a functional logic component that coninuously outputs a
    custom value.
    '''

    def __init__(self):
        '''Initialize the Constant object and extend Component.'''
        out_ports = [IOPort('data', 'any', 'out')]
        Component.__init__(self, 
                            comp_name='Constant', 
                            out_ports=out_ports,
                            config_options='vws'
                            )

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
        Execute the constant's functional logic.

        The constant continuously outputs a custom value.
        '''
        self.out_by_id['data'].value = self._value