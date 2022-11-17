from mesa import Agent


class BoxAgent(Agent):
    """
    Box agent class
    input: unique id, model
    output: box agent
    """

    def __init__(self,unique_id,model):
        """
        Initialize the box agent
        input: unique id, model
        output: box agent
        """
        super().__init__(unique_id, model)
        self.collected = False
    def step(self):
        """
        Step function
        input: none
        output: none
        """
        pass