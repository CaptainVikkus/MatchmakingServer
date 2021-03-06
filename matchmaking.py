import random
import socket
import requests
import time
from _thread import *
import threading
from datetime import datetime
import json

clients_lock = threading.Lock()

def getUserELO(userID):
    print("Getting ELO for " + userID)
    url = "https://k1zg78a86f.execute-api.us-east-2.amazonaws.com/default/returnELOfromID/?USERID=" + userID
    response = requests.get(url)
    #print(response.content)
    return int(json.loads(response.content))


def connectionLoop(sock):
   while True:
      #message
      gameData = { "GameID" : random.
                  randint(0, 1000), "Players" : []}
      #wait for data
      data, addr = sock.recvfrom(1024)
      jdata = json.loads(data)
      print("Match Start:")
      print(jdata["Users"])

      #matchmake
      targetELO = getUserELO(jdata["Users"][0])
      print(targetELO)
      numPlayers = 0
      for user in jdata["Users"]:
          player = {}
          player['UserID'] = user
          elo = getUserELO(user)
          player['ELO'] = elo
          print(elo)

          if (elo < targetELO + 500 and elo > targetELO - 500 ): #only elo valid players
              gameData["Players"].append(player)
              numPlayers += 1
              print("Added " + player['UserID'] + " to match")
          if (numPlayers == 3): #full match check
              break
      print(len(gameData["Players"]))
      if (len(gameData["Players"]) < 2): #invalid match
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
