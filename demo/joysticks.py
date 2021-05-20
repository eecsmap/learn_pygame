import pygame
import logging
logger = logging.getLogger(__name__)

class JoystickManager:

    def __init__(self, notify_add=None, notify_remove=None):
        self.joysticks = {}
        self.notify_add = notify_add
        self.notify_remove = notify_remove

    def handle(self, event):
        '''
        handle pygame event, watching joystick add/remove events
        '''
        if event.type == pygame.JOYDEVICEADDED:
            # when device is added, the event comes with a device index
            # it looks like the deprecated id in Joystick.get_id()
            # which seems not unique among devices, so we only need it to create a joystick instance
            joystick = pygame.joystick.Joystick(event.device_index)
            joystick.init()
            instance_id = joystick.get_instance_id()
            assert instance_id not in self.joysticks
            self.joysticks[instance_id] = joystick
            if self.notify_add:
                self.notify_add(joystick)

        elif event.type == pygame.JOYDEVICEREMOVED:
            assert event.instance_id in self.joysticks
            if self.notify_remove:
                self.notify_remove(self.joysticks[event.instance_id])
            #self.joysticks[event.instance_id].quit()
            del self.joysticks[event.instance_id]
        
        # handle buttons
        if event.type in (pygame.JOYAXISMOTION, pygame.JOYBALLMOTION, pygame.JOYHATMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP):
            print(f'*** {event}')

def test():
    pygame.init()
    def add(joystick):
        print(f'add joystick[{joystick.get_instance_id()}]: {joystick}')
    def remove(joystick):
        print(f'remove joystick[{joystick.get_instance_id()}]: {joystick}')
        joystick.quit()

    joystick_manager = JoystickManager(add, remove)

    while True:
        for event in pygame.event.get():
            joystick_manager.handle(event)


if __name__ == '__main__':
    test()