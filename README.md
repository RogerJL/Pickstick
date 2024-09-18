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

## How to run without installs
1. download zip via `<>Code` button and unzip
2. extract files to local folder
3. open https://colab.research.google.com/ in modern browser (Chrome...)
4. Upload by selecting the extracted file `Pickstick.ipynb`
5. Colab needs the python files `*.py` too
>Files folder (folder icon to the left), then upload file (document with up arrow)
select all .py files.
>
>_Note_: it is also possible to have these on a google drive

6. Klick on play button of the first section - should run without failure
7. Klick on play button of second section - game starts in window