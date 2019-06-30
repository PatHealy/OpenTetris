# AI to play OpenTetris
# Largely adapted from https://medium.com/acing-ai/how-i-build-an-ai-to-play-dino-run-e37f37bdf153
import random
import time
import os
import sys
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense, Activation, Conv2D, Flatten
from keras.optimizers import Adam
from ai_terminal_driver import AITerminalDriver

class TetrisAgent:
	def __init__(self,game):
		self._game = game;
		time.sleep(.5)

	def is_running(self):
		return not self._game.is_failed()

	def is_failed(self):
		return self._game.is_failed()

	def rotate(self):
		self._game.rotate()

	def move_down(self):
		self._game.move('down')

	def move_right(self):
		self._game.move('right')

	def move_left(self):
		self._game.move('left')

	def snap(self):
		self._game.snap()

class GameState:
	def __init__(self, agent, game):
		self._agent = agent
		self._game = game

	def get_state(self, actions):
		score = self._game.get_score()
		reward = 0.1*score/10
		is_over = False #game over

		if actions[0] == 1:
			self._agent.move_down()
			reward = 0.1*score/11
		elif actions[1] == 1:
			self._agent.move_right()
			reward = 0.1*score/11
		elif actions[2] == 1:
			self._agent.move_left()
			reward = 0.1*score/11
		elif actions[3] == 1:
			self._agent.rotate()
			reward = 0.1*score/11
		elif actions[4] == 1:
			self._agent.snap()
			reward = 0.1*score/11

		self._game.erase_board()
		self._game.print_board()
		#time.sleep(0.00005)

		board = self._game.get_board()

		if self._agent.is_failed():
			self._game.new_game()
			if score == 0:
				score = 1
			reward = -11/score
			is_over = True

		return board, reward, is_over #return the Experience tuple

class TetrisTrainer:
	def __init__(self, width=10, height=20, driver='Terminal', observe=False):
		self.ACTIONS = 5
		self.LEARNING_RATE = 1e-4
		self.GAMMA = 0.99
		self.OBSERVATION = 50000
		self.EXPLORE = 100000
		self.FINAL_EPSILON = 0.0001
		self.INITIAL_EPSILON = 0.1
		self.REPLAY_MEMORY = 50000
		self.BATCH = 32
		self.FRAME_PER_ACTION = 1
		self.width = width
		self.height = height
		self.play_game(width=width, height=height, driver=driver, observe=observe)

	def build_model(self):
		model = Sequential()
		model.add(Conv2D(32, (8, 8), padding='same',input_shape=(self.width,self.height+3,1)))
		model.add(Activation('relu'))
		model.add(Flatten())
		model.add(Dense(512))
		model.add(Activation('relu'))
		model.add(Dense(self.ACTIONS))
		adam = Adam(lr=self.LEARNING_RATE)
		model.compile(loss='mse',optimizer=adam)
		return model

	def train_batch(self, minibatch):
		inputs = np.zeros((self.BATCH, self.width, self.height+3, 1))
		targets = np.zeros((inputs.shape[0], self.ACTIONS))
		loss = 0

		for i in range(0, len(minibatch)):
			state_t = minibatch[i][0]
			action_t = minibatch[i][1]
			reward_t = minibatch[i][2]
			state_t1 = minibatch[i][3]
			terminal = minibatch[i][4]
			inputs[i:i + 1] = state_t
			targets[i] = self.model.predict(state_t)
			Q_sa = self.model.predict(state_t1)
			if terminal:
				targets[i, action_t] = reward_t
			else:
				targets[i, action_t] = reward_t + self.GAMMA * np.max(Q_sa)

				loss += self.model.train_on_batch(inputs, targets)

	def train_network(self, model, game_state):
		D = deque()
		do_nothing = np.zeros(self.ACTIONS)
		do_nothing[0] = 1

		x_t, r_0, terminal = game_state.get_state(do_nothing)
		s_t = np.array(x_t)
		s_t = s_t.reshape(-1, self.width, self.height+3, 1)

		OBSERVE = self.OBSERVATION
		epsilon = self.INITIAL_EPSILON
		t = 0
		while (True): #endless running
			loss = 0
			Q_sa = 0
			action_index = 0
			r_t = 0
			a_t = np.zeros([self.ACTIONS])

			if  random.random() <= epsilon:
				action_index = random.randrange(self.ACTIONS)
				a_t[action_index] = 1
			else:
				q = model.predict(s_t)
				max_Q = np.argmax(q)
				action_index = max_Q 
				a_t[action_index] = 1

			if epsilon > self.FINAL_EPSILON and t > OBSERVE:
				epsilon -= (self.INITIAL_EPSILON - self.FINAL_EPSILON) / self.EXPLORE 

			x_t1, r_t, terminal = game_state.get_state(a_t)
			x_t1 = np.array(x_t1)
			last_time = time.time()
			x_t1 = x_t1.reshape(1, x_t1.shape[1], x_t1.shape[0], 1)
			s_t1 = x_t1

			D.append((s_t, action_index, r_t, s_t1, terminal))
			if len(D) > self.REPLAY_MEMORY:
				D.popleft() 

			if t > OBSERVE:
				self.train_batch(random.sample(D, self.BATCH))
			s_t = s_t1 
			t = t + 1
			print("TIMESTEP", t, "/ EPSILON", epsilon, "/ ACTION", action_index, "/ REWARD", r_t,"/ Q_MAX " , np.max(Q_sa), "/ Loss ", loss)

	def play_game(self, width=10, height=20, driver='Terminal', observe=False):
		if driver == 'Terminal':
			game = AITerminalDriver(width=width, height=height)
		player = TetrisAgent(game)
		game_state = GameState(player,game)
		self.model = self.build_model()
		self.train_network(self.model,game_state)

if __name__ == '__main__':
	t = TetrisTrainer()