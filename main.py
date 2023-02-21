import json


def to_hashrate(hashrate: int) -> str:
    index = 0
    units = ['H/S', 'KH/S', 'MH/S', 'GH/S', 'TH/S', 'PH/S', 'EH/S']
    while hashrate > 1000:
        hashrate /= 1000
        index += 1
    return f'{round(hashrate, 2)} {units[index]}'


class CoinSetting:
    def __init__(self, filename: str):
        self.coin_filename = filename
        self.pool_percent = 0
        self.pool_block = 0
        self.pool_reward_by_day = 0
        self.pool_euros_by_day = 0
        self.pool_hash_rate_expected = 0
        self.fees_reward_by_day = 0
        self.fees_euros_by_day = 0
        with open(self.coin_filename) as fd:
            data = json.load(fd)
            self.coin = data["coin"]
            self.block_reward = data["block_reward"]
            self.block_by_day = data["block_by_day"]
            self.pool_hash_rate = data["pool_hash_rate"]
            self.network_difficulty = data["network_difficulty"]
            self.network_hash_rate = data["network_hash_rate"]
            self.fees_percent = data["fees_percent"]
            self.euros = data["euros"]
            self.fees_euros_expected = data["euros_expected"]

    def __str__(self):
        return f'==========================================\n' \
               f'Coin:                   {self.coin}\n' \
               f'Network Difficulty:     {round(self.network_difficulty, 2)}\n'\
               f'Network HashRate:       {to_hashrate(self.network_hash_rate)}\n'\
               f'Block Reward:           {round(self.block_reward, 2)} {self.coin}\n'\
               f'Block By Day:           {round(self.block_by_day, 2)}\n' \
               f'Pool HashRate:          {to_hashrate(self.pool_hash_rate)}\n' \
               f'Pool Hashrate Expected: {to_hashrate(self.pool_hash_rate_expected)}\n' \
               f'Pool Percent:           {round(self.pool_percent, 4)}%\n' \
               f'Pool Block By Day:      {round(self.pool_block, 2)}\n' \
               f'Pool Reward By Day:     {round(self.pool_reward_by_day, 2)} {self.coin}\n' \
               f'Pool Reward By Month:   {round(self.pool_reward_by_day * 31, 4)} {self.coin}\n' \
               f'Pool Euros By Day:      {round(self.pool_euros_by_day, 2)}€\n' \
               f'Pool Euros By Month:    {round(self.pool_euros_by_day * 31, 2)}€\n' \
               f'Fees Percent:           {round(self.fees_percent, 2)}%\n' \
               f'Fees Reward By Day:     {round(self.fees_reward_by_day, 2)} {self.coin}\n' \
               f'Fees Reweard By Month:  {round(self.fees_reward_by_day * 31, 2)} {self.coin}\n' \
               f'Fess Euros By Day:      {round(self.fees_euros_by_day, 2)}€\n' \
               f'Fees Euros By Month:    {round(self.fees_euros_by_day * 31, 2)}€\n' \
               f'Fees Euros Expected:    {round(self.fees_euros_expected, 2)}€\n'

    def compute(self):
        self.pool_percent = (self.pool_hash_rate * 100) / self.network_hash_rate
        self.pool_block = (self.pool_percent * self.block_by_day) / 100
        self.pool_reward_by_day = self.pool_block * self.block_reward
        self.pool_euros_by_day = self.pool_reward_by_day * self.euros

        self.fees_reward_by_day = (self.pool_reward_by_day * self.fees_percent) / 100
        self.fees_euros_by_day = self.fees_reward_by_day * self.euros

        euros_by_month = self.fees_euros_by_day * 31
        factor_euros = self.fees_euros_expected / euros_by_month
        self.pool_hash_rate_expected = self.pool_hash_rate * factor_euros


def load_projet(files: list):
    for filename in files:
        p = CoinSetting(filename)
        p.compute()
        print(p)


coin_project = [
    'ravencoin.json',
    'ergo.json',
    'flux.json',
    'btc.json'
]
load_projet(coin_project)
