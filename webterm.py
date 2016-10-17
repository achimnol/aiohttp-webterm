import os, signal, pty
import asyncio
from pathlib import Path

import aiohttp
from aiohttp import web
import uvloop
import sockjs


here = Path(__file__).parent
pid = None
fd  = None


def terminal_handler(msg, session):
    global pid, fd
    loop = asyncio.get_event_loop()
    if msg.tp == sockjs.MSG_OPEN:
        pid, fd = pty.fork()
        if pid == 0:
            # child
            os.execv('/bin/bash', ('/bin/bash',))
        else:
            print('terminal-start', pid, fd)
            loop.add_reader(fd, terminal_out, session, fd)
    elif msg.tp == sockjs.MSG_MESSAGE:
        try:
            os.write(fd, msg.data.encode('utf8'))
        except IOError:
            # the child may have exited.
            print('IOError: subproc may be dead')
    elif msg.tp == sockjs.MSG_CLOSE:
        print('sockjs close')
        os.kill(pid, signal.SIGHUP)
        os.kill(pid, signal.SIGCONT)
        ret = os.waitpid(pid)
        print('  subproc died', ret)

def terminal_out(session, fd):
    data = os.read(fd, 1024)
    session.send(data.decode('utf8'))

async def index(request):
    content = (here / 'templates' / 'index.html').read_text()
    return web.Response(text=content, content_type='text/html')


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    app = web.Application()
    app.router.add_get('/', index)
    app.router.add_static('/static', str(here / 'static'))
    sockjs.add_endpoint(app, terminal_handler, prefix='/pty')
    try:
        web.run_app(app, port=5000)
    except (KeyboardInterrupt, SystemExit):
        loop.stop()
    finally:
        loop.close()
