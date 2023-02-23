# Amex Offers

Program that connects to an American Express account and adds all eligible offers.

## Requirements

* Python 3.11 or later
* An American Express account
* Google Chrome installation

## Overview

Every month, Amex releases offers that cardholders are eligible to add to their card and use to save money. Once added to a card, these offers are applied automatically. However, the offers must be manually added to the card, which requires the tedious process of clicking a button to add each offer, often around 100 offers each month. This program takes credentials for an Amex account and programmatically adds all eligible offers to the card. By sparing the user from the monotony of a repetitive task, the Amex Offers program saves the user time and ensures the user can take full advantage of the benefits of their card.

## Setup

To connect the Amex Offers program with an account, clone this repository and run

```
pip install -r requirements.txt
```

Create a file called `config.ini` with the following format:

```
[CHROME]
chrome = <chrome_executable_path>
port = <port>
profile = <chrome_user_data_dir>

[AMEX]
username = <amex_username>
password = <amex_password>
```

To run the program and add all eligible offers to the Amex account, run

```
python main.py
```

A log file named `amex-offers.log` will be saved to the root directory of the project and contain details of the program's execution.
