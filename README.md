# Manchester Hack Jr 2023
### An AJ Bell Futures Foundation inspired project:
<br>

<p align="centre">
    <img src="https://cdn.discordapp.com/attachments/1160991230210084894/1168150967489933382/gitrich.png?ex=6550b85d&is=653e435d&hm=7fdfae07b700bf3cbe78e706b6a230a5630da67a4521bf3d4546377f80f54f36&">
</p>
<br>
<br>

## About the Project
<hr>

In summary, this project is a **financial education website**, where the user can learn about investing in stocks through on-hands practice, utilising **fake**, virtual currency in the **world's existent stock market in real-time**. 
<br>
<br>

### The User
<hr>

Each user registered into our database is given upmost confidentiality, **every user's session token and password is encrypted by the industry standard, cryptographically secure, hashing algorithm known as argon2**.
Additionally, this project utilises virtual, made-up (fake) currency. The user is not at financial risk in any way, shape or form. If the user were to lose any or all finance provided in the project, the user may restart again from the starting balance; however, as a result, any stock owned (unsold) before restarting will also be **discarded**.

<br>
<br>

## The Programming
<hr>

In the backend, we are using [fastapi](https://fastapi.tiangolo.com/) and pydantics to have typed data and well structured api endpoints. The code then interacts with our main `Database` class, which handles all connections with our database and can be found at `src/database.py`. For the database, we are using sqlite3 which does not need a server, as it can store all data locally.

To get the stock data, we use the [Alpaca API](https://alpaca.markets/) and we are interacting with it using `aiohttp` , which means that our code can be asynchronous. The Alpaca API also comes with a benefit of providing the latest news data which we can then display to the user so that they can make more informed decisions.


<br>
<br>

## Usage
<hr>

Our project is designed with the motive to engage the user to gain experience in the stock market **without risk**. Although this project is aimed towards inexperienced individuals who yearn to learn, this can also be used by experienced individuals to try new implementations of strategies and tactics without risk.
<br>
<br>

### Buying

In this project, the user is able to select as many stocks or shares to buy, at any time.
The only factor limiting the user is their **virtual wallet**! As the user learns more and more about stocks and the market, they will be able to earn more out of their investments, and either invest more or remain neutral in order to dominate the **rankings**(see below).
<br>
<br>

### Selling
Moreover, the user is also able sell the bought stock/share, _hopefully_ for a profit. They may choose a quick and easy transaction, quickly selling any stock/share as they rise in value, **or** the user may prefer to hold onto the stock for an even greater return at the cost of additional time.

### News
The _News_  feature allows the user to make more informed decisions based on recent real-world events, as our virtual simulation utilises **current stock prices**. This allows for a greater immersion and **realism**, which makes the project more reliable as a training resource for stock trading and investing.

<br>
<br>

## Leaderboard

<hr>

In order to add more content into the project that the user can engage with, we have added a ranking  system. The users that have signed up can actively compete against eachother for the title of the greatest investor within our project's reality-based simulation (bragging rights are included). **The leaderboard functions by sorting the users in descending order, the largest portfolio value to the lowest**. This creates a ranking from the most prosperous user to the least valued user. We believe this system is necessary for the motivation of the user.

<br>
<br>

***This is a project constructed within the time frame of HacJr Manchester, given inspiration through the challenge given by AJ Bell Futures Foundation- saving for the future.***



