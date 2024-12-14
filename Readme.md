## This guide will help you set up and run the AntiRateLimit bot, which manages rate-limited requests in a Discord bot using Python's `asyncio`. The bot controls the rate of requests, retries on failure, and provides efficient task management with concurrency control.

## Prerequisites

- Python 3.7 or higher
- A Discord bot account (You will need a bot token)
- `discord.py` library (for interacting with Discord API)

## Step 1: Clone the Repository

First, clone this repository to your local machine using the following command:

```bash
git clone https://github.com/NovaLeg/antiratelimit.git
cd antiratelimit
```
## Step 2: Install Dependencies

Before running the bot, install the necessary dependencies. The bot requires the discord.py library for interacting with Discord:

```bash
pip install discord.py
```
asyncio and heapq are built-in Python modules, so you don't need to install them separately.

## Step 3: Configure Rate Limiting Settings

In the `main.py` file, you can modify the rate-limiting settings for your bot. The `antiratelimit` class allows you to configure the following parameters:

- **`max_req`**: Maximum number of requests allowed within the defined time window.
- **`time`**: The time window in milliseconds (e.g., 2000ms = 2 seconds).
- **`slots`**: Number of concurrent tasks allowed to be processed at once.
- **`retry`**: The number of retries allowed if a task fails.
- 
## Example Rate Limiting Configuration:

Open the `main.py` file, and look for the following code:

```python
rate_limiter = antiratelimit(max_req=10, time=2000, slots=3, retry=2)
```

