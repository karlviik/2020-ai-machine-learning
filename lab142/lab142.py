import gym
import random
import math
import matplotlib.pyplot as plt

env = gym.make('CartPole-v0')
Q = {(0, 0): [0, 0]}
ITER_COUNT = 200
gamma = 1

# speeds = set()
# poss = set()
data = []

for i_episode in range(ITER_COUNT):
    observation = env.reset()
    old_state = (0, 0)

    prob = max(0.1, min(1.0, 1.0 - math.log10((i_episode + 1) / 25.0)))
    alpha = prob

    for t in range(200):
        # env.render()

        if Q[old_state][0] == Q[old_state][1] or random.random() < prob:
            action = round(random.random())
        else:
            action = 0 if Q[old_state][0] == max(Q[old_state]) else 1

        next_observation, reward, done, info = env.step(action)
        if done:
            reward = -reward   # simulatsioon lõppes enne 200 sammu, negatiivne tasu

        _, _, angle, speed = next_observation

        angle = round(angle * 10 * 2.5)
        speed = round(speed * 2.5)
        # poss.add(angle)
        # speeds.add(speed)

        new_state = (angle, speed)

        if new_state not in Q.keys():
            Q[new_state] = [0, 0]

        Q[old_state][action] += alpha * (reward + gamma * max(Q[new_state]) - Q[old_state][action])

        observation = next_observation
        old_state = new_state

        if done:
            # print("Episode {} finished after {} timesteps".format(i_episode, t+1))
            data.append(t + 1)
            break
# print(speeds)
# print(poss)
env.close()
plt.plot(range(len(data)), data)
plt.show()
