class DFA:

    def __call__(self, input_data):
        output = self.current_state(input_data)
        self.current_state = self.get_next_state(self.current_state, input_data)
        return output

    def get_next_state(self, current_state, input_data):
        return current_state

    def __init__(self):
        self.current_state = lambda x: x

if __name__ == '__main__':
    m = DFA()
    print(m(1))
    print(m(1))

