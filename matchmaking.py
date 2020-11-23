import random
import socket
import time
from _thread import *
import threading
from datetime import datetime
import json

clients_lock = threading.Lock()

def getUserELO(userID):
    url = "https://k1zg78a86f.execute-api.us-east-2.amazonaws.com/default/returnELOfromID/?" + userID
    response = requests.getURL(url)
    return json.loads(response.content)


def connectionLoop(sock):
   while True:
      #message
      gameData = { "GameID" : random.
                  randint(0, 1000), "Players" : []}
      #wait for data
      data, addr = sock.recvfrom(1024)
      print(str(data))
      jdata = json.loads(data)
      print(jdata["Users"])

      #matchmake
      targetELO = getUserELO(jdata["Users"][0])
      numPlayers = 0
      for user in jdata["Users"]:
          player = {}
          player['UserID'] = user
          elo = getUserELO(user)
          player['ELO'] = elo

          if (elo < targetELO + 500 & elo > targetELO - 500 ): #only elo valid players
              gameData["Players"].append(player)
              numPlayers += 1
          if (numPlayers == 3): #full match check
              break
      if (gameData["Players"].count < 2): #invalid match
          gameData["GameID"] = -1
      #send data
      s = json.dumps(gameData)
      sock.sendto(bytes(s,'utf8'), (addr[0],addr[1]))


def main():
   port = 12345
   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
   s.bind(('', port))
   start_new_thread(connectionLoop,(s,))
   while True:
      time.sleep(1)

if __name__ == '__main__':
   main()
