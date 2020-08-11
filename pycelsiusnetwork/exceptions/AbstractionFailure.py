class AbstractionFailure(Exception):
    def __init__(self, json: dict):
        self.json = json
        super().__init__(f'Abstraction Layer got a response in an '
                         f'unexpected format. '
                         f'Try using raw=True instead.')
