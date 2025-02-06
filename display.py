import sys
import time
import random
import numpy as np
from multiprocessing import shared_memory
import os
import socket
import pygame
import threading

# Type de message : "L,E,W" Lights, direction 1 et direction 2 Verte
# "V,P,E,W" VÃ©hicule, Prioritaire East West
# "V,N,E,W" Normal
# "V,W,E,W" Waiting

def handle_client_connection(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        message = data.decode()
        print(f"Server received: {message}")

        global object_status
        object_status.append(message)

    conn.close()

def start_server():
    HOST = "localhost"
    PORT = 65431
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print("Server is listening...")
    
    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        client_thread = threading.Thread(target=handle_client_connection, args=(conn,))
        client_thread.start()

def interface():
    """
    Allows the operator to observe the simulation in real-time.
    """
    # Initialize pygame
    pygame.init()

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)
    YELLOW = (255, 204, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    # Default window size
    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)  # Start in windowed mode
    pygame.display.set_caption("Crossroad Simulation")

    # Define road dimensions
    ROAD_WIDTH = min(WINDOW_WIDTH, WINDOW_HEIGHT) // 2
    LANE_WIDTH = ROAD_WIDTH // 2
    MARKING_WIDTH = 5
    MARKING_LENGTH = 30

    # clock = pygame.time.Clock() # Track time
    fullscreen = False
    running = True
    while running:
        # Handle events (quit or toggle fullscreen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f: 
                    fullscreen = not fullscreen
                    if fullscreen:
                        # Switch to fullscreen mode
                        SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    else:
                        # Switch to windowed mode
                        SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
                        
        # Fill screen with background color
        SCREEN.fill(WHITE)
        # Get screen size (update after toggle)
        screen_width, screen_height = SCREEN.get_size()
        center_x, center_y = screen_width // 2, screen_height // 2

        # Draw vertical road
        pygame.draw.rect(SCREEN, GRAY, [(center_x - ROAD_WIDTH//2, 0), (ROAD_WIDTH, screen_height)])
        
        # Draw horizontal road
        pygame.draw.rect(SCREEN, GRAY, [(0, center_y - ROAD_WIDTH//2), (screen_width, ROAD_WIDTH)])
        
        # Draw lane markings (Vertical)
        for y in range(0, screen_height, 2 * MARKING_LENGTH):
            pygame.draw.rect(SCREEN, YELLOW, [(center_x - MARKING_WIDTH//2, y), (MARKING_WIDTH, MARKING_LENGTH)])
        
        # Draw lane markings (Horizontal)
        for x in range(0, screen_width, 2 * MARKING_LENGTH):
            pygame.draw.rect(SCREEN, YELLOW, [(x, center_y - MARKING_WIDTH//2), (MARKING_LENGTH, MARKING_WIDTH)])
        
        # Update display
        pygame.display.flip()
        
        # # Limit FPS
        # clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    object_status = []  # List of object statuses
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    interface()