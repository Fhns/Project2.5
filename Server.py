# networked multiplayer game
from typing import Dict
import Player
import socket
import datetime

SERVER_PORT = 25001
server_ip = '127.0.0.1'
# randomly choose which player
all_players: Dict[str, Player.Player] = {}


def find_ip_address():
    connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        connection.connect(('10.255.255.255', 1))
        server_address = connection.getsockname()[0]
    except IOError:
        server_address = '127.0.0.1'
    finally:
        connection.close()
    return server_address


def main():
    game_state = Player.GameState(all_players)
    server_address = find_ip_address()
    udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_server_socket.bind((server_address, SERVER_PORT))
    while True:
        data_packet = udp_server_socket.recvfrom(1024)
        client_address = data_packet[1]
        if not client_address[0] in all_players:
            offset = len(all_players) + 1
            new_player: Player.Player = Player.Player(200 * offset, 200 * offset, 0, datetime.datetime.now())
            all_players[client_address[0]] = new_player
        response = game_state.to_json()
        udp_server_socket.sendto(str.encode(response), client_address)


if __name__ == '__main__':
    main()
