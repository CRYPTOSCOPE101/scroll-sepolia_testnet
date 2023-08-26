from func_sepolia_testnet import *
import logging
import threading
import random

RETRY = 20


if __name__ == '__main__':
    with open("private_key.txt", "r") as f:
        keys_list = [row.strip() for row in f if row.strip()]

    def main():
        log = logging.getLogger(threading.current_thread().name)
        console_out = logging.StreamHandler()
        basic_format1 = logging.Formatter('%(asctime)s : [%(name)s] : %(message)s')
        basic_format = logging.Formatter('%(asctime)s : %(message)s')
        console_out.setFormatter(basic_format1)
        file_handler = logging.FileHandler(f"logs/{threading.current_thread().name}.txt", 'w', 'utf-8')
        file_handler.setFormatter(basic_format)
        log.setLevel(logging.DEBUG)
        log.addHandler(console_out)
        log.addHandler(file_handler)

        while keys_list:
            private_key = keys_list.pop(0)
            bsc_w3 = ARBITRUM_CHAIN['web3']
            acc = bsc_w3.eth.account.from_key(private_key)
            log.info('----------------------------------------------------------------------------')
            log.info(f'|   Сейчас работает аккаунт - {acc.address}   |')
            log.info('----------------------------------------------------------------------------\n\n')

            if auto_chain is True:
                start_chain = get_start_chain(private_key, log)
            else:
                if chain_bridge == 1:
                    start_chain = ARBITRUM_CHAIN
                else:
                    start_chain = OPTIMISM_CHAIN

            value_bridge = round(random.uniform(sepolia_eth_min, sepolia_eth_max), sepolia_eth_decimal)
            log.info(f'Bridge from {start_chain["name"]} to Sepolia - {value_bridge} ETH')

            for _ in range(RETRY):
                res_ = get_gas_sepolia(private_key, start_chain, value_bridge, log)
                if res_ == 1:
                    break
            if res_ == 0 or res_ == 'error':
                log.info(f'Bridge from {start_chain["name"]} to Sepolia - Критическая ошибка')
                continue

            time.sleep(random.uniform(time_delay_min, time_delay_max))

            for _ in range(RETRY):
                res_ = bridge_from_sepolia_to_scroll(private_key, log)
                if res_ == 1:
                    break
            if res_ == 0 or res_ == 'error':
                log.info(f'Bridge from Sepolia to Scroll - Критическая ошибка')
                continue

            time.sleep(random.uniform(time_delay_min, time_delay_max))

            log.info('Uniswap\n')

            for i in range(number_of_repetitions):
                log.info(f'Круг - {i+1}\n')

                value = round(random.uniform(value_swap_min, value_swap_max), value_swap_decimal)
                for _ in range(RETRY):
                    res_ = swap_eth_for_token(private_key, value, log)
                    if res_ == 1 or res_ == 'balance':
                        break
                if res_ == 'balance':
                    continue

                time.sleep(random.uniform(time_delay_min, time_delay_max))

                for _ in range(RETRY):
                    res_ = swap_token_for_eth(private_key, log)
                    if res_ == 1 or res_ == 'balance':
                        break
                if res_ == 'balance':
                    continue

                time.sleep(random.uniform(time_delay_min, time_delay_max))

            log.info('Buy GHO Uniswap\n')
            value = round(random.uniform(value_liquid_min, value_liquid_max), value_liquid_decimal)
            for _ in range(RETRY):
                res_ = swap_eth_for_token(private_key, value, log)
                if res_ == 1 or res_ == 'balance':
                    break
            if res_ == 'balance':
                continue

            time.sleep(random.uniform(time_delay_min, time_delay_max))

            log.info('Add liquidity Uniswap\n')
            for _ in range(RETRY):
                res_ = add_liquidity(private_key, log)
                if res_ == 1 or res_ == 'balance':
                    break
            if res_ == 'balance':
                continue

            time.sleep(random.uniform(time_delay_min, time_delay_max))


    for _ in range(number_of_thread):
        threading.Thread(target=main).start()
        time.sleep(20)