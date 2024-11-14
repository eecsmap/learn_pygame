import pygame
import logging
import sys
from collections import deque

logger = logging.getLogger(__name__)

class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 18)

    def tprint(self, screen, text):
        text_bitmap = self.font.render(text, True, (0, 0, 0))
        screen.blit(text_bitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

class JoyStickDashboard:

    # show joystick activities on screen
    def __init__(self, joystick_manager, width=800, height=900):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.my_font = pygame.font.SysFont('Microsoft Yahei.ttf', 64)
        self.clock = pygame.time.Clock()
        self.text_print = TextPrint()
        self.joystick_manager = joystick_manager
        self.axis4_values = deque([0] * 300)

    def show(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            self.joystick_manager.handle(event)

        # self.screen.fill('black')
        # x = y = 0
        # if joystick_manager.joysticks:
        #     x = int(joystick_manager.joysticks[0].get_axis(0) * 250)
        #     y = int(joystick_manager.joysticks[0].get_axis(1) * 250)
        # else:
        #     self.screen.blit(self.my_font.render('insert joystick ...', True, 'red'), (0, 0))


        # Drawing step
        # First, clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
        self.screen.fill((255, 255, 255))
        self.text_print.reset()

        # Get count of joysticks.
        joystick_count = pygame.joystick.get_count()

        self.text_print.tprint(self.screen, f"Number of joysticks: {joystick_count}")
        self.text_print.indent()

        # For each joystick:
        for joystick in self.joystick_manager.joysticks.values():
            jid = joystick.get_instance_id()

            self.text_print.tprint(self.screen, f"Joystick {jid}")
            self.text_print.indent()

            # Get the name from the OS for the controller/joystick.
            name = joystick.get_name()
            self.text_print.tprint(self.screen, f"Joystick name: {name}")

            guid = joystick.get_guid()
            self.text_print.tprint(self.screen, f"GUID: {guid}")

            power_level = joystick.get_power_level()
            self.text_print.tprint(self.screen, f"Joystick's power level: {power_level}")

            # Usually axis run in pairs, up/down for one, and left/right for
            # the other. Triggers count as axes.
            axes = joystick.get_numaxes()
            self.text_print.tprint(self.screen, f"Number of axes: {axes}")
            self.text_print.indent()

            for i in range(axes):
                axis = joystick.get_axis(i)
                self.text_print.tprint(self.screen, f"Axis {i} value: {axis:>6.3f}")
            self.text_print.unindent()

            buttons = joystick.get_numbuttons()
            self.text_print.tprint(self.screen, f"Number of buttons: {buttons}")
            self.text_print.indent()

            for i in range(buttons):
                button = joystick.get_button(i)
                self.text_print.tprint(self.screen, f"Button {i:>2} value: {button}")
            self.text_print.unindent()

            hats = joystick.get_numhats()
            self.text_print.tprint(self.screen, f"Number of hats: {hats}")
            self.text_print.indent()

            # Hat position. All or nothing for direction, not a float like
            # get_axis(). Position is a tuple of int values (x, y).
            for i in range(hats):
                hat = joystick.get_hat(i)
                self.text_print.tprint(self.screen, f"Hat {i} value: {str(hat)}")
            self.text_print.unindent()

            self.text_print.unindent()

            # Draw the chart for the value of axis[4] over time
            self.text_print.tprint(self.screen, "Axis 4 values over time:")
            self.text_print.indent()
            self.axis4_values.append(joystick.get_axis(4))
            if len(self.axis4_values) > 300:
                self.axis4_values.popleft()
            for i in range(len(self.axis4_values)):
                x = 10 + i
                y = 100 + self.axis4_values[i] * 100
                pygame.draw.line(self.screen, (0, 0, 0), (x, 100), (x, y))
            self.text_print.unindent()


        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Limit to 30 frames per second.
        self.clock.tick(30)

        # pygame.draw.line(self.screen, 'red', (self.width / 2, self.height / 2), ((self.width + x) / 2, (self.height + y) / 2), 10)

        # pygame.display.update()
        # self.clock.tick(50)


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
            #assert instance_id not in self.joysticks
            self.joysticks[instance_id] = joystick
            if self.notify_add:
                self.notify_add(joystick)

        elif event.type == pygame.JOYDEVICEREMOVED:
            #assert event.instance_id in self.joysticks
            if self.notify_remove:
                self.notify_remove(self.joysticks[event.instance_id])
            #self.joysticks[event.instance_id].quit()
            del self.joysticks[event.instance_id]
        
        # handle buttons
        if event.type in (pygame.JOYAXISMOTION, pygame.JOYBALLMOTION, pygame.JOYHATMOTION, pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED):
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


def main():
    pygame.init()
    joystick_manager = JoystickManager()
    dashboard = JoyStickDashboard(joystick_manager)
    while True:
        dashboard.show()

if __name__ == '__main__':
    main()