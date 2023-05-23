CREATE TABLE coin (
    coin_id INT,
    coin_name VARCHAR(255),
    coin_symbol VARCHAR(10),
    coin_price DECIMAL(18, 10)
);
INSERT INTO coin (coin_id, coin_name, coin_symbol, coin_price)
VALUES  (1, 'Bitcoin', 'BTC', 26934.081784061054),
    (2, 'Ethereum', 'ETH', 1823.1506809035877),
    (3, 'Binance Coin', 'BNB', 643.71),
    (4, 'Cardano', 'ADA', 0.36792227256404747),
    (5, 'XRP', 'XRP', 0.4622456266747739),
    (6, 'Dogecoin', 'DOGE', 0.07310624014277925),
    (7, 'Polkadot', 'DOT', 5.3224943873072315),
    (8, 'Solana', 'SOL', 19.58680196539812),
    (9, 'USD Coin', 'USDC', 0.9999358753635372),
    (10, 'Terra', 'LUNA', 49.26);