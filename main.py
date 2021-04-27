from lib.linepy import *
from lib.akad import *
from akad.ttypes import OpType, Message, TalkException
from thrift.Thrift import *
from thrift.unverting import *
from thrift.TMultiplexedProcessor import *
from thrift.TSerialization import *
from thrift.TRecursive import *
from thrift import transport, protocol, server
from thrift.protocol import TCompactProtocol, TMultiplexedProtocol, TProtocol
from thrift.transport import TTransport, TSocket, THttpClient, TZlibTransport
from threading import Thread
import os, livejson, traceback, time, sys
from data import commands
OT = OpType

fileName = os.path.splitext(os.path.basename(__file__))[0]
db = livejson.File("token/%s.json" %fileName)

if ":" in db['token']:
    app = "ANDROIDLITE\t2.11.1\tAndroid OS\t5.1.1"
else:
    app = "DESKTOPWIN\t6.0.3\tWindows\t10"
try:
    client = LINE(idOrAuthToken=db["token"], appName=app)
except:
    e = traceback.format_exc()
    if "code=20" in e: print("FREEZING"); time.sleep(3600); python3 = sys.executable; os.execl(python3, python3, *sys.argv)
    elif "code=8" in e or "code=7" in e: client = LINE(db["mail"], db["pass"], certificate='{}.crt'.format(db["mail"]), appName=app); db['token'] = client.authToken
    else: traceback.print_exc()
uid = client.profile.mid
poll = OEPoll(client)
good = commands(fileName, client, app, uid)
print("LOGIN SUCCESS")
def main_loop(op):
    if op.type == OT.RECEIVE_MESSAGE: good.receive_message(op)
    elif op.type == OT.INVITE_INTO_GROUP or op.type == 121: good.notif_invite(op)
    elif op.type == OT.CANCEL_INVITATION_GROUP or op.type == 125: good.notif_cancel(op)
    elif op.type == OT.KICKOUT_FROM_GROUP or op.type == 132: good.notif_kick(op)
    elif op.type == OT.NOTIFIED_KICKOUT_FROM_GROUP or op.type == 133: good.notif_kick_from_group(op)
    elif op.type == OT.NOTIFIED_INVITE_INTO_GROUP or op.type == 124: good.notif_invite_into_group(op)
    elif op.type == OT.NOTIFIED_ACCEPT_GROUP_INVITATION or op.type == 130: good.notif_accept_group_invite(op)

while 1:
    try:
        ops = client.poll.fetchOperations(client.revision, 50)
        for op in ops:
            client.revision = max(client.revision, op.revision)
            t1 = Thread(target=main_loop(op,))
            t1.start()
            t1.join()
    except Exception as e:
        e = traceback.format_exc()
        if "EOFError" in e: pass
        elif "ShouldSyncException" in e or "LOG_OUT" in e: python3 = sys.executable; os.execl(python3, python3, *sys.argv)
        else: traceback.print_exc()
