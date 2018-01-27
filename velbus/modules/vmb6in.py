"""
:author: Thomas Delaet <thomas@delaet.org
"""
import velbus

class VMB6INModule(velbus.Module):
    """
    Velbus input module with 6 channels
    """
    def __init__(self, module_type, module_name, module_address, controller):
        velbus.Module.__init__(self, module_type, module_name, module_address, controller)
        self._is_closed = {}
        self._callbacks = {}

    def is_closed(self, channel):
        if channel in self._is_closed:
            return self._is_closed[channel]
        return False

    def _load(self):
        message = velbus.ModuleStatusRequestMessage(self._address)
        message.channels = list(range(1, self.number_of_channels()+1))
        self._controller.send(message)

    def number_of_channels(self):
        return 7

    def _on_message(self, message):
        if isinstance(message, velbus.PushButtonStatusMessage):
            for channel in message.closed:
                self._is_closed[channel] = True
            for channel in message.opened:
                self._is_closed[channel] = False
            for channel in message.get_channels():
                if channel in self._callbacks:
                    for callback in self._callbacks[channel]:
                        callback(self._is_closed[channel])

    def on_status_update(self, channel, callback):
        """
        Callback to execute on status of update of channel
        """
        if not channel in self._callbacks:
            self._callbacks[channel] = []
        self._callbacks[channel].append(callback)

velbus.register_module('VMB6IN', VMB6INModule)
