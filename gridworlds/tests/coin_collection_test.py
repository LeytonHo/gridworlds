from gridworlds.environments.coin_collection import CoinCollectionEnvironment

# TODO: Clean up

if __name__ == '__main__':
    env = CoinCollectionEnvironment()
    env.print_environment()
    print(env.agent_coordinates)
    print(env.episode_timesteps)
