import json
import time
import random
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

from easytello import Tello

class Simulator():
    def __init__(self):
        self.takeoff_alt = 81
        self.field_limit = 200
        self.num_treasures = 5
        self.vision_range = 70  # visão do drone em cm
        self._init_state()
        self.driver_instance = None
        self.command()
        self.generate_field()
        self._init_plot()

    def _init_state(self):
        self.takeoff_state = False
        self.altitude = 0
        self.cur_loc = (0,0)
        self.bearing = 0
        self.altitude_data = []
        self.path_coors = [(0,0)]
        self.flip_coors = []
        self.command_log = []
        self.treasures = []
        self.visited_treasures = []

    def _init_plot(self):
        self.fig, self.ax = plt.subplots()
        self.plot_field()
        plt.show(block=False)

    # ---------------- Commands ----------------
    def serialize_command(self, command: dict):
        serialized = command['command']
        command_args = command.get('arguments', ())
        if len(command_args) > 0:
            serialized = '{} {}'.format(serialized, ' '.join([str(arg) for arg in command_args]))
        return serialized

    def send_command(self, command: str, *args):
        command_json = {'command': command, 'arguments': args}
        self.command_log.append(command_json)
        print('I am running your "{}" command.'.format(self.serialize_command(command_json)))
        time.sleep(0.5)  # simula tempo do comando

    def command(self):
        print("Hi! My name is TelloSim and I am your training drone.")
        print("I help you try out your flight plan before sending it to a real Tello.")
        print("I am now ready to take off. 🚁")
        self.send_command('command')

    def check_takeoff(self):
        if not self.takeoff_state:
            raise Exception("I can't do that unless I take off first!")

    # ---------------- Altitude ----------------
    def takeoff(self):
        if not self.takeoff_state:
            print("Get ready for takeoff!")
            self.takeoff_state = True
            self.altitude = self.takeoff_alt
            self.altitude_data.append(self.takeoff_alt)
            self.send_command('takeoff')
            print(f"My estimated takeoff altitude is {self.altitude} centimeters")
        else:
            print(f"My current altitude is {self.altitude} centimeters, can't takeoff again!")

    def land(self):
        self.check_takeoff()
        print("Landing...")
        self.takeoff_state = False
        self.altitude = 0
        self.send_command('land')
        print("Flight finished. Keep the window open to view final state.")
        plt.show(block=True)  # mantém a janela aberta

    def up(self, dist):
        self.check_takeoff()
        self.altitude += dist
        self.altitude_data.append(self.altitude)
        self.send_command('up', dist)

    def down(self, dist):
        self.check_takeoff()
        self.altitude -= dist
        self.altitude_data.append(self.altitude)
        self.send_command('down', dist)

    # ---------------- Horizontal Movements ----------------
    def dist_bearing(self, orig, bearing, dist):
        rads = np.deg2rad(bearing)
        dx = np.sin(rads) * dist
        dy = np.cos(rads) * dist
        return orig[0]+dx, orig[1]+dy

    def forward(self, dist):
        self._move_along_path(dist, self.bearing, 'forward')

    def back(self, dist):
        self._move_along_path(dist, self.bearing+180, 'back')

    def left(self, dist):
        self._move_along_path(dist, self.bearing-90, 'left')

    def right(self, dist):
        self._move_along_path(dist, self.bearing+90, 'right')

    def _move_along_path(self, dist, bearing, command_name):
        self.check_takeoff()
        prev_loc = self.cur_loc
        self.cur_loc = self.dist_bearing(self.cur_loc, bearing, dist)
        self.path_coors.append(self.cur_loc)
        self.send_command(command_name, dist)
        self.collect_treasure_along_path(prev_loc, self.cur_loc)
        self.plot_field()

    def cw(self, deg):
        self.check_takeoff()
        self.bearing = (self.bearing + deg) % 360
        self.send_command('cw', deg)
        print(f"New bearing: {self.bearing}")

    def ccw(self, deg):
        self.check_takeoff()
        self.bearing = (self.bearing - deg) % 360
        self.send_command('ccw', deg)
        print(f"New bearing: {self.bearing}")

    # ---------------- Tesouros ----------------
    def generate_field(self):
        self.treasures = []
        self.visited_treasures = []
        while len(self.treasures) < self.num_treasures:
            tx = random.randint(-self.field_limit, self.field_limit)
            ty = random.randint(-self.field_limit, self.field_limit)
            safe = True
            for t in self.treasures:
                if np.hypot(tx-t[0], ty-t[1]) < 20:  # distância mínima entre tesouros
                    safe = False
                    break
            if safe:
                self.treasures.append((tx, ty))

    def collect_treasure_along_path(self, prev_loc, new_loc):
        steps = int(np.ceil(np.hypot(new_loc[0]-prev_loc[0], new_loc[1]-prev_loc[1])))
        if steps == 0:
            steps = 1
        xs = np.linspace(prev_loc[0], new_loc[0], steps)
        ys = np.linspace(prev_loc[1], new_loc[1], steps)
        for x, y in zip(xs, ys):
            for i, (tx, ty) in enumerate(self.treasures):
                if i in self.visited_treasures:
                    continue
                if abs(x - tx) <= self.vision_range/2 and abs(y - ty) <= self.vision_range/2:
                    print(f"Tesouro coletado em ({tx},{ty})!")
                    self.visited_treasures.append(i)

    # ---------------- Plotting ----------------
    def plot_field(self):
      self.ax.cla()
      self.ax.set_xlim([-self.field_limit-40, self.field_limit+40])
      self.ax.set_ylim([-self.field_limit-40, self.field_limit+40])
      self.ax.grid()
      self.ax.set_xlabel('X Distance from Start')
      self.ax.set_ylabel('Y Distance from Start')
      self.ax.set_title('Tello Flight Path')

      # Tesouros
      for i, (tx, ty) in enumerate(self.treasures):
          if i in self.visited_treasures:
              self.ax.plot(tx, ty, 'gx', markersize=15, label="Collected Treasure" 
                         if 'Collected Treasure' not in self.ax.get_legend_handles_labels()[1] else "")
          else:
              self.ax.plot(tx, ty, 'g*', markersize=15, label="Treasure" 
                         if 'Treasure' not in self.ax.get_legend_handles_labels()[1] else "")

      # Trajetória drone
      if len(self.path_coors) > 0:
          x_vals = [p[0] for p in self.path_coors]
          y_vals = [p[1] for p in self.path_coors]
          self.ax.plot(x_vals, y_vals, 'bo', linestyle='dashed', linewidth=2, markersize=8, label="Drone Moves")
          self.ax.plot(x_vals, y_vals, linewidth=2, alpha=.3)

      # ---------------- Área de visão ----------------
      self.ax.set_aspect('equal')
      vision_half = self.vision_range / 2
      rect = plt.Rectangle(
          (self.cur_loc[0]-vision_half, self.cur_loc[1]-vision_half),
          self.vision_range, self.vision_range,
          linewidth=1, edgecolor='blue', facecolor='blue', alpha=0.2
      )
      self.ax.add_patch(rect)

      self.ax.legend()
      plt.pause(0.01)


    # ---------------- Deploy para drone real ----------------
    def deploy(self):
        print("Deploying commands to real drone!")
        if self.driver_instance is None:
            self.driver_instance = Tello()
        for command in self.command_log:
            self.driver_instance.send_command(self.serialize_command(command))

    # ---------------- Reset ----------------
    def reset(self):
        print("Resetting simulator state...")
        self._init_state()
        self.command()
        self.generate_field()
        self._init_plot()

