#!/usr/bin/env python3
"""
Bluey's Adventure Game
Help Bluey collect toys while avoiding obstacles!
Use arrow keys to move Bluey around.
"""

import tkinter as tk
from tkinter import messagebox
import random

class BlueyGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Bluey's Adventure")
        self.root.resizable(False, False)
        
        # Game settings
        self.canvas_width = 600
        self.canvas_height = 500
        self.player_size = 40
        self.item_size = 30
        self.obstacle_size = 35
        self.speed = 15
        
        # Game state
        self.player_x = self.canvas_width // 2
        self.player_y = self.canvas_height - 80
        self.player_dx = 0
        self.player_dy = 0
        
        self.items = []
        self.obstacles = []
        self.score = 0
        self.level = 1
        self.lives = 5  # Increased from 3 for easier gameplay
        self.game_running = False
        self.game_over = False
        
        # Difficulty settings
        self.items_per_level = 3  # Reduced from 5
        self.obstacles_per_level = 1  # Reduced from 3
        
        # Create UI
        self.create_widgets()
        
        # Bind keys
        self.root.bind('<Left>', lambda e: self.set_direction(-self.speed, 0))
        self.root.bind('<Right>', lambda e: self.set_direction(self.speed, 0))
        self.root.bind('<Up>', lambda e: self.set_direction(0, -self.speed))
        self.root.bind('<Down>', lambda e: self.set_direction(0, self.speed))
        self.root.bind('<KeyRelease>', self.stop_movement)
        
    def create_widgets(self):
        # Title frame
        title_frame = tk.Frame(self.root, bg='#87CEEB')
        title_frame.pack(fill='x')
        
        title = tk.Label(title_frame, text="🐕 BLUEY'S ADVENTURE 🐕", 
                        font=('Comic Sans MS', 24, 'bold'), 
                        bg='#87CEEB', fg='#1E3A8A')
        title.pack(pady=10)
        
        # Score and lives frame
        info_frame = tk.Frame(self.root, bg='#FEE2C5')
        info_frame.pack(fill='x')
        
        self.score_label = tk.Label(info_frame, 
                                    text=f"Score: {self.score}", 
                                    font=('Comic Sans MS', 14, 'bold'),
                                    bg='#FEE2C5', fg='#D2691E')
        self.score_label.pack(side='left', padx=20, pady=5)
        
        self.level_label = tk.Label(info_frame, 
                                    text=f"Level: {self.level}", 
                                    font=('Comic Sans MS', 14, 'bold'),
                                    bg='#FEE2C5', fg='#D2691E')
        self.level_label.pack(side='left', padx=20, pady=5)
        
        self.lives_label = tk.Label(info_frame, 
                                    text=f"Lives: {'❤️' * self.lives}", 
                                    font=('Comic Sans MS', 14, 'bold'),
                                    bg='#FEE2C5', fg='#DC143C')
        self.lives_label.pack(side='right', padx=20, pady=5)
        
        # Game canvas
        self.canvas = tk.Canvas(self.root, 
                               width=self.canvas_width, 
                               height=self.canvas_height,
                               bg='#90EE90',
                               highlightthickness=2,
                               highlightbackground='#228B22')
        self.canvas.pack(padx=10, pady=10)
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg='#FFF8DC')
        control_frame.pack(fill='x', pady=10)
        
        self.start_btn = tk.Button(control_frame, text='Start Game', 
                                   font=('Comic Sans MS', 12, 'bold'),
                                   bg='#4169E1', fg='white',
                                   padx=20, pady=10,
                                   command=self.start_game)
        self.start_btn.pack(side='left', padx=20)
        
        reset_btn = tk.Button(control_frame, text='Reset', 
                             font=('Comic Sans MS', 12, 'bold'),
                             bg='#FF6347', fg='white',
                             padx=20, pady=10,
                             command=self.reset_game)
        reset_btn.pack(side='left', padx=20)
        
        # Instructions
        instructions = tk.Label(self.root, 
                               text="Use Arrow Keys to help Bluey collect toys! 🎾 Avoid obstacles! 🚧", 
                               font=('Comic Sans MS', 11),
                               bg='#FFF8DC', fg='#8B4513')
        instructions.pack(pady=5)
        
        # Draw initial state
        self.draw_welcome_screen()
        
    def draw_welcome_screen(self):
        """Draw welcome screen."""
        self.canvas.delete('all')
        
        # Draw grass texture
        for i in range(0, self.canvas_height, 20):
            for j in range(0, self.canvas_width, 20):
                if (i + j) % 40 == 0:
                    self.canvas.create_oval(j, i, j+5, i+5, 
                                          fill='#7CFC00', outline='#7CFC00')
        
        # Welcome text
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 - 50,
                               text="Welcome to Bluey's Adventure!",
                               font=('Comic Sans MS', 20, 'bold'),
                               fill='#1E3A8A')
        
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
                               text="Collect all the toys to win!",
                               font=('Comic Sans MS', 14),
                               fill='#4169E1')
        
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + 40,
                               text="Click 'Start Game' to begin!",
                               font=('Comic Sans MS', 14, 'italic'),
                               fill='#DC143C')
    
    def set_direction(self, dx, dy):
        """Set player movement direction."""
        if self.game_running and not self.game_over:
            self.player_dx = dx
            self.player_dy = dy
    
    def stop_movement(self, event):
        """Stop player movement when key is released."""
        if event.keysym in ['Left', 'Right']:
            self.player_dx = 0
        if event.keysym in ['Up', 'Down']:
            self.player_dy = 0
    
    def spawn_items(self):
        """Spawn collectible items."""
        self.items = []
        for _ in range(self.items_per_level + self.level - 1):
            x = random.randint(50, self.canvas_width - 50)
            y = random.randint(50, self.canvas_height - 100)
            item_type = random.choice(['ball', 'bone', 'toy'])
            self.items.append({'x': x, 'y': y, 'type': item_type})
    
    def spawn_obstacles(self):
        """Spawn obstacles."""
        self.obstacles = []
        # Only add obstacles after level 2
        if self.level > 2:
            for _ in range(self.obstacles_per_level + max(0, self.level - 3)):
                x = random.randint(50, self.canvas_width - 50)
                y = random.randint(50, self.canvas_height - 150)
                # Make sure obstacle isn't too close to player start
                if abs(y - self.player_y) > 100:
                    # Much slower movement
                    dx = random.choice([-0.5, 0.5])
                    dy = random.choice([-0.5, 0.5])
                    self.obstacles.append({'x': x, 'y': y, 'dx': dx, 'dy': dy})
    
    def start_game(self):
        """Start the game."""
        if not self.game_running:
            self.game_running = True
            self.game_over = False
            self.spawn_items()
            self.spawn_obstacles()
            self.start_btn.config(state='disabled')
            self.game_loop()
    
    def game_loop(self):
        """Main game loop."""
        if not self.game_running or self.game_over:
            return
        
        # Move player
        self.player_x += self.player_dx
        self.player_y += self.player_dy
        
        # Keep player in bounds
        self.player_x = max(self.player_size // 2, 
                           min(self.player_x, self.canvas_width - self.player_size // 2))
        self.player_y = max(self.player_size // 2, 
                           min(self.player_y, self.canvas_height - self.player_size // 2))
        
        # Move obstacles
        for obs in self.obstacles:
            obs['x'] += obs['dx']
            obs['y'] += obs['dy']
            
            # Bounce off walls
            if obs['x'] <= 0 or obs['x'] >= self.canvas_width:
                obs['dx'] = -obs['dx']
            if obs['y'] <= 0 or obs['y'] >= self.canvas_height:
                obs['dy'] = -obs['dy']
        
        # Check item collection
        collected = False
        for item in self.items[:]:
            if self.check_collision(self.player_x, self.player_y, 
                                   item['x'], item['y'], 
                                   self.player_size, self.item_size):
                self.items.remove(item)
                self.score += 10
                collected = True
                self.update_display()
                
                # Show encouraging message
                msg_x = item['x']
                msg_y = item['y'] - 20
                encouragements = ["Great job!", "Awesome!", "You're doing great!", 
                                "Well done!", "Amazing!", "Fantastic!", "Yay!"]
                msg = random.choice(encouragements)
                msg_id = self.canvas.create_text(msg_x, msg_y,
                                                text=msg,
                                                font=('Comic Sans MS', 12, 'bold'),
                                                fill='#FFD700',
                                                tags='encourage')
                # Remove message after 500ms
                self.root.after(500, lambda: self.canvas.delete(msg_id))
        
        # Check obstacle collision
        for obs in self.obstacles:
            if self.check_collision(self.player_x, self.player_y, 
                                   obs['x'], obs['y'], 
                                   self.player_size, self.obstacle_size):
                self.hit_obstacle()
                break
        
        # Check level complete
        if len(self.items) == 0 and not self.game_over:
            self.level_complete()
            return
        
        # Draw everything
        self.draw_game()
        
        # Continue loop
        self.root.after(50, self.game_loop)
    
    def check_collision(self, x1, y1, x2, y2, size1, size2):
        """Check if two objects collide."""
        distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        return distance < (size1 + size2) // 2
    
    def hit_obstacle(self):
        """Handle obstacle collision."""
        self.lives -= 1
        self.update_display()
        
        if self.lives <= 0:
            self.game_over = True
            self.game_running = False
            self.show_game_over()
        else:
            # Reset player position
            self.player_x = self.canvas_width // 2
            self.player_y = self.canvas_height - 80
            self.player_dx = 0
            self.player_dy = 0
    
    def level_complete(self):
        """Handle level completion."""
        self.level += 1
        self.score += 50  # Bonus for completing level
        self.update_display()
        
        # Show level complete message
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
                               text=f"Level {self.level - 1} Complete!",
                               font=('Comic Sans MS', 24, 'bold'),
                               fill='#FFD700',
                               tags='level_msg')
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2 + 40,
                               text=f"Bonus: +50 points!",
                               font=('Comic Sans MS', 16, 'bold'),
                               fill='#32CD32',
                               tags='level_msg')
        
        # Continue to next level after delay
        self.root.after(2000, self.next_level)
    
    def next_level(self):
        """Start next level."""
        self.canvas.delete('level_msg')
        self.spawn_items()
        self.spawn_obstacles()
        self.game_loop()
    
    def draw_game(self):
        """Draw the game state."""
        self.canvas.delete('all')
        
        # Draw grass background
        for i in range(0, self.canvas_height, 20):
            for j in range(0, self.canvas_width, 20):
                if (i + j) % 40 == 0:
                    self.canvas.create_oval(j, i, j+5, i+5, 
                                          fill='#7CFC00', outline='#7CFC00')
        
        # Draw items
        for item in self.items:
            if item['type'] == 'ball':
                # Tennis ball
                self.canvas.create_oval(
                    item['x'] - self.item_size // 2, item['y'] - self.item_size // 2,
                    item['x'] + self.item_size // 2, item['y'] + self.item_size // 2,
                    fill='#FFFF00', outline='#FFD700', width=2
                )
                # Ball details
                self.canvas.create_arc(
                    item['x'] - self.item_size // 2, item['y'] - self.item_size // 2,
                    item['x'] + self.item_size // 2, item['y'] + self.item_size // 2,
                    start=0, extent=180, outline='white', width=2, style='arc'
                )
            elif item['type'] == 'bone':
                # Dog bone
                self.canvas.create_rectangle(
                    item['x'] - 15, item['y'] - 5,
                    item['x'] + 15, item['y'] + 5,
                    fill='#F5DEB3', outline='#D2691E', width=2
                )
                self.canvas.create_oval(
                    item['x'] - 18, item['y'] - 8,
                    item['x'] - 10, item['y'] + 8,
                    fill='#F5DEB3', outline='#D2691E', width=2
                )
                self.canvas.create_oval(
                    item['x'] + 10, item['y'] - 8,
                    item['x'] + 18, item['y'] + 8,
                    fill='#F5DEB3', outline='#D2691E', width=2
                )
            else:  # toy
                # Toy block
                self.canvas.create_rectangle(
                    item['x'] - self.item_size // 2, item['y'] - self.item_size // 2,
                    item['x'] + self.item_size // 2, item['y'] + self.item_size // 2,
                    fill='#FF69B4', outline='#FF1493', width=2
                )
        
        # Draw obstacles (rocks/cones)
        for obs in self.obstacles:
            # Orange cone
            points = [
                obs['x'], obs['y'] - self.obstacle_size // 2,
                obs['x'] - self.obstacle_size // 2, obs['y'] + self.obstacle_size // 2,
                obs['x'] + self.obstacle_size // 2, obs['y'] + self.obstacle_size // 2
            ]
            self.canvas.create_polygon(points, fill='#FF8C00', outline='#FF4500', width=2)
            # White stripe
            self.canvas.create_rectangle(
                obs['x'] - 10, obs['y'],
                obs['x'] + 10, obs['y'] + 5,
                fill='white', outline='white'
            )
        
        # Draw player (Bluey)
        # Body
        self.canvas.create_oval(
            self.player_x - self.player_size // 2, self.player_y - self.player_size // 2,
            self.player_x + self.player_size // 2, self.player_y + self.player_size // 2,
            fill='#5B9BD5', outline='#1E3A8A', width=2
        )
        
        # Ears
        self.canvas.create_oval(
            self.player_x - 18, self.player_y - 25,
            self.player_x - 8, self.player_y - 10,
            fill='#5B9BD5', outline='#1E3A8A', width=2
        )
        self.canvas.create_oval(
            self.player_x + 8, self.player_y - 25,
            self.player_x + 18, self.player_y - 10,
            fill='#5B9BD5', outline='#1E3A8A', width=2
        )
        
        # Eyes
        self.canvas.create_oval(
            self.player_x - 10, self.player_y - 5,
            self.player_x - 4, self.player_y + 1,
            fill='black'
        )
        self.canvas.create_oval(
            self.player_x + 4, self.player_y - 5,
            self.player_x + 10, self.player_y + 1,
            fill='black'
        )
        
        # Nose
        self.canvas.create_oval(
            self.player_x - 3, self.player_y + 3,
            self.player_x + 3, self.player_y + 9,
            fill='black'
        )
        
        # Tail
        self.canvas.create_oval(
            self.player_x - self.player_size // 2 - 8, self.player_y + 5,
            self.player_x - self.player_size // 2 + 2, self.player_y + 15,
            fill='#5B9BD5', outline='#1E3A8A', width=2
        )
    
    def update_display(self):
        """Update score, level, and lives display."""
        self.score_label.config(text=f"Score: {self.score}")
        self.level_label.config(text=f"Level: {self.level}")
        self.lives_label.config(text=f"Lives: {'❤️' * self.lives}")
    
    def reset_game(self):
        """Reset the game."""
        self.player_x = self.canvas_width // 2
        self.player_y = self.canvas_height - 80
        self.player_dx = 0
        self.player_dy = 0
        self.items = []
        self.obstacles = []
        self.score = 0
        self.level = 1
        self.lives = 5  # Increased from 3
        self.game_running = False
        self.game_over = False
        
        self.start_btn.config(state='normal')
        self.update_display()
        self.draw_welcome_screen()
    
    def show_game_over(self):
        """Show game over screen."""
        self.draw_game()
        
        # Draw game over overlay
        self.canvas.create_rectangle(
            100, 150, 500, 350,
            fill='#FFE4B5', outline='#FF6347', width=3
        )
        
        self.canvas.create_text(
            self.canvas_width // 2, 200,
            text="GAME OVER!", 
            font=('Comic Sans MS', 32, 'bold'),
            fill='#DC143C'
        )
        
        self.canvas.create_text(
            self.canvas_width // 2, 260,
            text=f"Final Score: {self.score}", 
            font=('Comic Sans MS', 20, 'bold'),
            fill='#1E3A8A'
        )
        
        self.canvas.create_text(
            self.canvas_width // 2, 300,
            text=f"Level Reached: {self.level}", 
            font=('Comic Sans MS', 16),
            fill='#4169E1'
        )
        
        self.start_btn.config(state='normal')
        
        messagebox.showinfo("Game Over", 
                          f"Good try! You reached level {self.level}\nFinal Score: {self.score}")

def main():
    root = tk.Tk()
    
    # Center the window
    window_width = 620
    window_height = 750
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2 
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    game = BlueyGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()