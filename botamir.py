# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 11:21:56 2022

@author: Amir
"""
import sys
import configuracionestwitter
#configuracionestwitter.reload(consumer, consumerSecret, beared,access,accessSecret,clientID,clientIDSecret)
from configuracionestwitter import consumer, consumerSecret, beared,access,accessSecret,clientID,clientIDSecret

#from logging import exception
#from pydoc import cli
import socket
import threading
import time
import tweepy
#from tweepy import OAuthHandler
import pandas as pd
#from pandastable import Table, TableModel
#import clienteBot.py


# Configuracion de acceso con las credenciales

client = tweepy.Client(bearer_token=beared,consumer_key=consumer,consumer_secret=consumerSecret,access_token=access,access_token_secret=accessSecret)

id = 1512087571882409997

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65405  # Port to listen on (non-privileged ports are > 1023)
query = 'from:hambai832'





def menubot():
    print ("*********************************************")
    print ("Este es mi bot de Twitter, lista de Menués:")
    print ("\n")
    print ("1. Convertir el nombre de Usuario de alguien en ID de Twitter")
    print ("2. Listar los Twetts de un ID de Usuario Especifico")
    print ("3. Bot Activo en stream")
    print ("4. Crawler de Hashtags")
    print ("5. Exit")
    
def scriptstream():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            
            idnueva=idantigua = client.get_users_tweets(id=id).meta.get("newest_id")
            
            
            while True:    
                idnueva=idantigua = client.get_users_tweets(id=id).meta.get("newest_id")
                print("Esperando conexxion con el Bot")
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print(f"conectado a {addr} Esperando a un nuevo tweet")
                    
                    
                    while(idnueva==idantigua):
                        
                        time.sleep(10)
                        idnueva = client.get_users_tweets(id=id).meta.get("newest_id")
                    
                    
                    print("Tweet nuevo reconocido, con id: ",idnueva," Trasmitiendo ....")
                    conn.sendall(bytes(str(idnueva), 'utf8'))
                    time.sleep(10)
                    s.close()
    except KeyboardInterrupt :
        print()
    finally:
        s.close()



def cliente():
  
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
            s2.connect((HOST, PORT))
            data = s2.recv(2000)
            d = str(data)[2:(len(str(data))-1)]
            print("Se ha recibido la id del Tweet procediendo con la respuesta, like y retweet: ... ")
            client.like(tweet_id=d)
            client.retweet(tweet_id=d)
            client.create_tweet(text="Que prueba tan chula",in_reply_to_tweet_id=d)
            print("like, Retweet y comentario realizado")
            s2.close()
            time.sleep(13)

    
    
    
loop = True

while loop:
    menubot()
    opcionbot = int(input("Ingrese el numero de opcion que desee realizar: "))
    if opcionbot == 1:
        username = input("Ingrese el nick del Usuario: ")
        print ("\n")
        try:
            user_id = client.get_user(username=username)
            print (f"El ID de Twitter del usuario {user_id.data.name} es {user_id.data.id}.")
            print ("\n")
            #1client.get_users_tweets(id=id).meta
        except :
            print("Error: El Usuario no existe")
            print ("\n")
    if opcionbot == 2:
        try:
            auth = tweepy.OAuthHandler(consumer, consumerSecret)
            auth.set_access_token(access, accessSecret)
            api = tweepy.API(auth)
            userID = input("Ingrese el nick del Usuario: ")
            h = int(input("Ingrese la cantidad de Tweets que desee listar (el limite es 200): "))
            api = tweepy.API(auth)
            tweets = api.user_timeline(screen_name=userID, 
                           # count equivale a la cantidad máxima de tweets
                           count=200,
                           include_rts = False,
                           # extended permite que se atrape todo el tweet 
                           # si se quitara esta opción solo se extraerian 140 palabras
                           tweet_mode = 'extended'
                           )
        
            for info in tweets[:h]:
                print("ID: {}".format(info.id))
                print(info.created_at)
                print(info.full_text)
                print("\n")
                
        except :
             print("Error: El Usuario no existe")
             print ("\n")
             
    if opcionbot == 3:
        t1 = threading.Thread(target=scriptstream).start()
        t2 = threading.Thread(target=cliente).start()
                
        
    if opcionbot == 4:
        auth = tweepy.OAuthHandler(consumer, consumerSecret)
        auth.set_access_token(access, accessSecret)
        api = tweepy.API(auth)
        df = pd.DataFrame(columns=['text', 'source', 'url'])
        columns = ['Fecha','Usuario','Tweet']
        msg =[]
        q = input("Ingrese el Hashtag que desee buscar:")
        for tweet in api.search_tweets( q, lang="es"):
            msg.append([tweet.created_at, tweet.user.screen_name, tweet.text]) 
            #msg = tuple(msg)                    
            #msgs.append(msg)

        df = pd.DataFrame(msg, columns=columns)
        print(df)
        
        #except :
         #    print("Error: El Usuario no existe")
          #   print ("\n")