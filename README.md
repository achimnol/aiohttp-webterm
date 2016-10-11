# aiohttp-based Web Terminal

This is a very primitive prototype combining [terminal.js](https://github.com/Gottox/terminal.js),
[SockJS](http://sockjs.org/) with [its Python-side counterpart](https://github.com/aio-libs/sockjs), and [Python
aiohttp](https://github.com/KeepSafe/aiohttp) to implement a web-based terminal emulator.

**NOTE:** This has no security protection at all. DO NOT USE for any production or on public networks as all keystrokes and terminal content are exposed as plain text.

## How to try out

You need Python 3.5 or higher, NodeJS 4 or higher, and an OS with pseudo-tty capability.

```sh
npm install  # install terminal.js and its dependencies
webpack      # bundle them into a single js file usable in browsers
python -m venv ./venv-test-pty       # prepare a virtual-env
source ./venv-test-pty/bin/activate  # activate it
pip install -r requirements.txt      # install server-side dependencies
python webterm.py   # run!
```

Then open `http://localhost:5000` on your web browser.
