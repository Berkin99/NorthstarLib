
import serial
import time
import pygame
from pygame.locals import *

# Örnek bir hash fonksiyonu ile stringe bir ID atama
def hash_string(string):
    hash_value = 0
    for char in string:
        hash_value = (hash_value * 31 + ord(char)) % 256
    return hash_value

# Uzun bir string
my_long_string = "Bu bir örnek uzun setring0"

# Stringin hash değerini hesaplayarak bir ID oluşturuyoruz
string_id = hash_string(my_long_string)

print("Uzun String:", my_long_string)
print("String ID'si:", string_id)
