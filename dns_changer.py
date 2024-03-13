import subprocess
import json

# import pyfiglet

DNS_ADDR_JSON_PATH = "./address.json"
TITLE = "DNS-changer"


class Address:
    def __init__(self, name: str, addr1: str):
        self.name = name
        self.addr1 = addr1

    def __repr__(self):
        return {"name": self.name, "addr1": self.addr1}

    def get_dict(self):
        return self.__repr__()


def connect(ip_address=None, disable=False):
    command = (
        f"wmic nicconfig where (IPEnabled=TRUE) call SetDNSServerSearchOrder ({ip_address})"
        if disable == False
        else "wmic nicconfig where (IPEnabled=TRUE) call SetDNSServerSearchOrder ()"
    )
    res = subprocess.run(command, capture_output=True)
    print(res)
    return True if res.returncode == 0 else False


def get_addr_data(path: str):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {"address": []}


def add_addr_data(path: str, prev_data: dict, new_address: Address):
    prev_data["address"].append(new_address.get_dict())

    with open(path, "w") as f:
        json.dump(prev_data, f)


# def delete_addr_data(path: str, prev_data: dict, index: int):
#     prev_data["address"].remove(prev_data[index])

#     with open(path, "w") as f:
#         json.dump(prev_data, f)


def print_data(data: dict):
    for i, addr in enumerate(data["address"], start=1):
        print(f"{i} - {addr['name']}({addr['addr1']})")


def handle_connection(data):
    print_data(data)
    run = True
    while run:
        index = input("choose one: ").lower()

        if index.isdigit():
            try:
                server = data["address"][int(index) - 1]
            except IndexError:
                print("choose a server from list above")
                continue

            name = server["name"]
            ip_address = server["addr1"]

            success = connect(ip_address)
            if success:
                print(f"Successfully connected to: {name}({ip_address})")
                input("press enter to exit: ")
                return
            else:
                print("Failed to connect!; Try to run the program as Administrator.")
                input("press enter to exit: ")
                return
        else:
            print("please enter a the number associated with servers above.")
            continue


def main():
    data = get_addr_data(DNS_ADDR_JSON_PATH)
    print(f"..::{TITLE}::..")
    print(
        """
type:
    connect -> to connect to a server.
    add -> to add a DNS server.
    disable -> to disable DNS.
    quit -> to quit the program.
"""
    )
    while True:
        answer = input("(connect, add, disable, quit): ").lower().strip()
        if answer == "connect":
            if not data["address"]:
                print("no servers found! please add some and try again.")
                continue
            handle_connection(data)

        elif answer == "add":
            addr1 = input("Enter the server ip address: ").strip()
            name = input("enter a name to save it: ").strip()
            add_addr_data(DNS_ADDR_JSON_PATH, data, Address(name, addr1))
            print("Server successfully added!; connect?")
            if input("(yes/no)").lower() == "yes":
                success = connect(addr1)
                if success:
                    print(f"Successfully connected to: {name}({addr1})")
                    input("press enter to exit: ")
                else:
                    print(
                        "Failed to connect!; Try to run the program as Administrator or your ip address is wrong."
                    )
                    input("press enter to exit: ")

        elif answer == "disable":
            success = connect(disable=True)
            if success:
                print(f"DNS Successfully disabled.")
                input("press enter to exit: ")
            else:
                print("Failed!; Try to run the program as Administrator.")
                input("press enter to exit: ")

        elif answer == "quit":
            quit()

        else:
            print("Invalid input; please choose an option from above.")


main()
