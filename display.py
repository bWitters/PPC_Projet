import sys
import time
import random
import numpy as np
from multiprocessing import shared_memory
import os
import socket
import pygame
import threading

# Global variables
object_list = []
object_list_lock = threading.Lock()  # Lock for synchronizing access to object_list

def handle_client_connection(conn): # 
    global object_list, object_list_lock
    while True:
        data = conn.recv(1024)
        if not data:
            break
        message = data.decode()
        print(f"Server received: {message}")

        messages = message.split("_")
        for message in messages:
            parts = message.split(",")
            if parts[0] == "V" and parts[1] != "W":
                if parts[1] == "P":
                    color = (255, 0, 0)  # Red for priority vehicles
                else:
                    color = (255, 255, 255)  # White for normal vehicles

                # Define initial position based on direction
                WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
                ROAD_WIDTH = min(WINDOW_WIDTH, WINDOW_HEIGHT) // 2
                LANE_WIDTH = ROAD_WIDTH // 2
                center_x, center_y = WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
                if parts[2] == "E":
                    # Right side of the road
                    x = WINDOW_WIDTH - 50  # Adjust to be within the screen
                    y = center_y - LANE_WIDTH // 2
                elif parts[2] == "W":
                    # Left side of the road
                    x = 10  # Adjust to be within the screen
                    y = center_y - LANE_WIDTH // 2
                elif parts[2] == "N":
                    # Top side of the road
                    x = center_x - LANE_WIDTH // 2
                    y = 10  # Adjust to be within the screen
                elif parts[2] == "S":
                    # Bottom side of the road
                    x = center_x + LANE_WIDTH // 2
                    y = WINDOW_HEIGHT - 50  # Adjust to be within the screen

                # Create vehicle object
                vehicle = {
                    "color": color,
                    "direction1": parts[2],
                    "direction2": parts[3],
                    "x": x,
                    "y": y,
                    "is_passing": False
                }

                # Add vehicle to the list (with lock)
                with object_list_lock:
                    object_list.append(vehicle)

    conn.close()

def start_server():
    HOST = "localhost"
    PORT = 65430
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

    # Size of the squares and circles for traffic lights
    SQUARE_SIZE = 50  # Size of the square
    CIRCLE_RADIUS = 20  # Radius of the circle

    # clock = pygame.time.Clock() # Track time
    fullscreen = False
    running = True
    clock = pygame.time.Clock()
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
        
        # Draw 4 squares at the corners of the crossroads
        # Top-left square
        pygame.draw.rect(SCREEN, BLACK, (center_x - ROAD_WIDTH//2 - SQUARE_SIZE, center_y - ROAD_WIDTH//2 - SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        # Top-right square
        pygame.draw.rect(SCREEN, BLACK, (center_x + ROAD_WIDTH//2, center_y - ROAD_WIDTH//2 - SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        # Bottom-left square
        pygame.draw.rect(SCREEN, BLACK, (center_x - ROAD_WIDTH//2 - SQUARE_SIZE, center_y + ROAD_WIDTH//2, SQUARE_SIZE, SQUARE_SIZE))
        # Bottom-right square
        pygame.draw.rect(SCREEN, BLACK, (center_x + ROAD_WIDTH//2, center_y + ROAD_WIDTH//2, SQUARE_SIZE, SQUARE_SIZE))

        # Draw 4 circles (traffic lights) inside the squares
        # Top-left circle
        pygame.draw.circle(SCREEN, RED, (center_x - ROAD_WIDTH//2 - SQUARE_SIZE//2, center_y - ROAD_WIDTH//2 - SQUARE_SIZE//2), CIRCLE_RADIUS)
        # Top-right circle
        pygame.draw.circle(SCREEN, RED, (center_x + ROAD_WIDTH//2 + SQUARE_SIZE//2, center_y - ROAD_WIDTH//2 - SQUARE_SIZE//2), CIRCLE_RADIUS)
        # Bottom-left circle
        pygame.draw.circle(SCREEN, RED, (center_x - ROAD_WIDTH//2 - SQUARE_SIZE//2, center_y + ROAD_WIDTH//2 + SQUARE_SIZE//2), CIRCLE_RADIUS)
        # Bottom-right circle
        pygame.draw.circle(SCREEN, RED, (center_x + ROAD_WIDTH//2 + SQUARE_SIZE//2, center_y + ROAD_WIDTH//2 + SQUARE_SIZE//2), CIRCLE_RADIUS)

        # Draw vehicles
        global object_list, object_list_lock
        with object_list_lock:
            for vehicle in object_list:
                color = vehicle["color"]
                x = vehicle["x"]
                y = vehicle["y"]
                pygame.draw.rect(SCREEN, color, [(x, y), (40, 40)])

                # Update vehicle position
                if not vehicle["is_passing"]:
                    if vehicle["direction1"] == "E":
                        vehicle["x"] -= 1
                    elif vehicle["direction1"] == "W":
                        vehicle["x"] += 1
                    elif vehicle["direction1"] == "N":
                        vehicle["y"] += 1
                    elif vehicle["direction1"] == "S":
                        vehicle["y"] -= 1

                    # Check if the vehicle has passed the intersection
                    if (vehicle["direction1"] == "E" and vehicle["x"] < center_x - LANE_WIDTH//2) or \
                       (vehicle["direction1"] == "W" and vehicle["x"] > center_x + LANE_WIDTH//2) or \
                       (vehicle["direction1"] == "N" and vehicle["y"] > center_y + LANE_WIDTH//2) or \
                       (vehicle["direction1"] == "S" and vehicle["y"] < center_y - LANE_WIDTH//2):
                        vehicle["is_passing"] = True
                else:
                    if vehicle["direction2"] == "E":
                        vehicle["x"] += 1
                    elif vehicle["direction2"] == "W":
                        vehicle["x"] -= 1
                    elif vehicle["direction2"] == "N":
                        vehicle["y"] -= 1
                    elif vehicle["direction2"] == "S":
                        vehicle["y"] += 1

        # Update display
        pygame.display.update()
        
        # Delay between frames
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    interface()