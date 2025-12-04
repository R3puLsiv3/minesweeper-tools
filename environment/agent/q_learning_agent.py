import random

import gymnasium as gym
import numpy as np


class QLearningAgent:

    def __init__(self, env_name, episodes, eps_decay, alpha, alpha_decay, gamma):
        self.env_name = env_name
        self.episodes = episodes
        self.eps = 1
        self.eps_decay = eps_decay
        self.alpha = alpha
        self.alpha_decay = alpha_decay
        self.gamma = gamma

        self.q_table = {}

    def train(self):
        env = gym.make(self.env_name)
        for episode in range(self.episodes):
            state, _ = env.reset()
            state, reward, terminated, _, info = env.step(0)
            while not terminated:

                if random.random() < self.eps:
                    action = env.action_space.sample(mask=info["mask"])
                elif state in self.q_table:
                    action = np.argmax(self.q_table[state][info["mask"]])
                else:
                    self.q_table[state] = np.zeros(16)
                    action = env.action_space.sample(mask=info["mask"])

                next_state, reward, terminated, _, info = env.step(action)

                self.q_table[state][action] += self.alpha * (
                        reward + self.gamma * max(self.q_table[next_state]) - self.q_table[state][action])

                self.eps *= self.eps_decay
                self.alpha *= self.alpha_decay
