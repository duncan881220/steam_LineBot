from transitions.extensions import GraphMachine

class BotStateMachine(GraphMachine):
    current_game_id = 0
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
    def is_show_price_imformation(self, event):
        return event == "價格資訊"###string版本
    def is_show_game_imformation(self, event):
        return event == "遊戲資訊"
    def game_finded_correctly(self, user_input, title_list):
        return user_input in title_list
def CreateLineBotMachine():
    machine = BotStateMachine(
    states=["init", "game_selected", "price_info", "game_info"],
    transitions=[
        {
            "trigger": "advance",
            "source": "init",
            "dest": "game_selected",
            "conditions": "game_finded_correctly",
        },
        {
            "trigger": "info",
            "source": "price_info",
            "dest": "game_info",
            "conditions": "is_show_game_imformation",
        },
        {
            "trigger": "info",
            "source": "game_selected",
            "dest": "game_info",
            "conditions": "is_show_game_imformation",
        },
        {
            "trigger": "info",
            "source": "game_selected",
            "dest": "price_info",
            "conditions": "is_show_price_imformation",
        },
        {
            "trigger": "info",
            "source": "game_info",
            "dest": "price_info",
            "conditions": "is_show_price_imformation",
        },
        {"trigger": "go_back", "source": ["init" ,"game_selected", "price_info", "game_info"], "dest": "init"},
    ],
    initial="init",
    auto_transitions=False,
    show_conditions=True,
    )
    return machine
def show_fsm(machine):
    machine.get_graph().draw("fsm.png", prog="dot", format="png")

if __name__ == "__main__":
    machine = CreateLineBotMachine()
    show_fsm(machine)
    