from gridworlds.environments.coin_collection import CoinCollectionEnvironment
from gridworlds.agents.q_agent import QAgent


def play_coin_collection(agent, trials=500, debug_flag=False):
    reward_per_episode = []
    environment = agent.environment

    for episode in range(trials):
        trace = []
        action_spaces = []

        while environment._episode_timesteps:
            current_state = environment._agent_coordinates
            action = agent.next_action(environment.action_space())
            action_spaces.append(environment.action_space())
            trace.append(action)
            reward = environment.step(action)
            new_state = environment._agent_coordinates

            agent.learn(current_state, reward, new_state, action)

            if environment.game_over:
                break

        reward_per_episode.append(environment._episode_reward)

        if debug_flag and episode == trials - 1:
            print('Episode trace')
            print(trace)
            print('Action spaces at each timestep')
            print(action_spaces)
            environment.print_environment()
            print(f"Final episode reward: {environment._episode_reward}")

        environment.reset()

    return reward_per_episode


if __name__ == '__main__':
    env = CoinCollectionEnvironment()
    env.print_environment()
    print(f"Episode timesteps: {env._episode_timesteps}")
    agent = QAgent(env, epsilon=0.15, alpha=0.2, gamma=0.9)
    reward_per_episode = play_coin_collection(agent, trials=50000)
    print("Successfully ran")
    print(reward_per_episode[-100:])
