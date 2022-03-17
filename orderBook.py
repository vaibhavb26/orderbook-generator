from copy import deepcopy

def Factory(action):
    actions = {
        "N": NewLevel,
        "U": UpdateLevel,
        "D": DeleteLevel
    }

    return actions[action]()


class orderBook:

    def __init__(self):
        self.empty_order = [(-1, -1)]
        self.bid_log = self.empty_order * 10
        self.ask_log = self.empty_order * 10

    def validate_bid_log(self, bid_log):
        is_correct =  True
        bidside_max = 1e9

        for i in range(0, 10):
            if bid_log[i][0] != -1:
                if bid_log[i][0] >= bidside_max:
                    is_correct = False
                    break
                
                else:
                    bidside_max = bid_log[i][0]

        return is_correct


    def validate_ask_log(self, ask_log):
        is_correct =  True
        askside_min = 0

        for i in range(0, 10):
            if ask_log[i][0] != -1:
                if ask_log[i][0] <= askside_min:
                    is_correct = False
                    break

                else:
                    askside_min = ask_log[i][0]
        
        return is_correct

    # def validate_orderbook(self, bid_log, ask_log):
        
    #     is_correct =  True
    #     bidside_max = 1e9
    #     askside_min = 0

    #     for i in range(0, 10):
    #         if bid_log[i][0] != -1:
    #             if bid_log[i][0] >= bidside_max:
    #                 is_correct = False
    #                 break
                
    #             else:
    #                 bidside_max = bid_log[i][0]

    #         if ask_log[i][0] != -1:
    #             if ask_log[i][0] <= askside_min:
    #                 is_correct = False
    #                 break

    #             else:
    #                 askside_min = ask_log[i][0]
        
    #     return is_correct

    def completeness_check(self):

        is_complete = True

        for i in range(0, 10):
            if self.bid_log[i][0] == -1 or self.ask_log[i][0] == -1:
                is_complete = False
                break

        return is_complete

    def print_orderbook(self, seq_no):
        print(seq_no, self.bid_log, self.ask_log)

    def update_orderbook(self, packet):
        
        if packet[3] == 'B':
            updated_bid_log = Factory(packet[1]).applyMethod(packet, self.bid_log)
            if self.validate_bid_log(updated_bid_log):
                self.bid_log = updated_bid_log

        else:
            updated_ask_log = Factory(packet[1]).applyMethod(packet, self.ask_log)
            if self.validate_ask_log(updated_ask_log):
                self.ask_log = updated_ask_log


class NewLevel:
    # ask if no entry existed is there a need to shift all levels down again?
    def applyMethod(packet, log):
        updated_log = deepcopy(log)
        level = packet[2]
        price = packet[4]
        size = packet[5]
        
        for i in range(9, level, -1):
            updated_log[i] = updated_log[i - 1]

        updated_log[level] = (price, size)

        return updated_log
        

class UpdateLevel:
    
    def applyMethod(packet, log):
        updated_log = deepcopy(log)
        level = packet[2]
        price = packet[4]
        size = packet[5]
        updated_log[level] = (price, size)

        return updated_log

class DeleteLevel:
    # ask what if no entry existed at that position in first place
    def applyMethod(packet, log):
        updated_log = deepcopy(log)
        level = packet[2]
        for i in range(level, 9):
            updated_log[i] = updated_log[i + 1]

        updated_log[9] = (-1, -1)

        return updated_log



if __name__ == "__main__":
    file = open("SampleOrders.txt", "r")
    lines = file.readlines()

    prev_seq_no = -1

    custom_orderBook = orderBook()
    for line in lines:
        input = line.split(",")
        input[0] = int(input[0])
        input[2] = int(input[2])
        input[4] = float(input[4])
        input[5] = float(input[5])
        seq_no = input[0]

        custom_orderBook.update_orderbook(input)

        if prev_seq_no != seq_no:
            if custom_orderBook.completeness_check():
                custom_orderBook.print_orderbook(seq_no)

            prev_seq_no = seq_no


    file.close()