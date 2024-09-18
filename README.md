# Pickstick

This project implements several AIs for a simple Nim game often named 21 sticks.

## Rules:

* Two players. 
* There are 21 sticks in one heap.
* Players alternate taking one to three sticks, but of cause not more than remainings.
* Player that takes last stick looses.

## Implementations:

| Program                          | Details                                                                        |
|----------------------------------|--------------------------------------------------------------------------------|
| `human_player.py`                | Anna vs Bertil                                                                 |
| `random_playing.py`              | randomly selects                                                               |
| `analytical_playing.py`          | optimal selections                                                             |
| `learn_by_playing.py`            | will get better for each game                                                  |
| `learn_by_self_play.py`          | like previous but plays ten games against another similar implementation first |
| `learn_by_reinforced_reward.py`  | overkill but still...                                                          |

### Implementation detail
Common code in `picker.py` but `human_player.py` is used as default opponent.

## How to run
`python` required

### Clone the Repository or download and unzip
`git` optional

Clone the GitHub repository to your local machine using the following command:

`git clone https://github.com/RogerJL/Pickstick`

or download zip via `<>Code` button and unzip



### Run Your Python Code:
If your Python code is in a single script, navigate to the repository folder and run the script:

`cd your-repo`

`python your_script.py`
