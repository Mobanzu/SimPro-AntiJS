import livejson, requests, os, time, json, string, re, random, threading, traceback, sys
from lib.akad import *
from lib.akad.ttypes import TalkException

class commands(threading.Thread):
    def __init__(self, fileName, client, app, uid):
        super(commands, self).__init__()
        self.fileName = fileName
        self.client = client
        self.app = app
        self.uid = uid
        self.db = livejson.File("database/%s.json" %fileName, True, True, 4)
        self.master = ["YOUR_MID"]
        self.count = {"countKick": 0, "countInvite": 0, "countCancel": 0}
        self.settings = {
            "strictmode": True,
            "rname": fileName,
            "sname": "default",
            "restartpoint": None,
            "pictprofile": False
        }
        if not "settings" in self.db:
            self.db['settings'] = self.settings
            self.settings = self.db["settings"]
            for oup in self.master:
                client.sendMessage(oup, "Activated.\nMID: %s" %uid)
        else:
            self.settings = self.db["settings"]
        self.stats = {
            "owners": {
                "add": False,
                "del": False,
                "list": []
            },
            "admins": {
                "add": False,
                "del": False,
                "list": []
            },
            "staffs": {
                "add": False,
                "del": False,
                "list": []
            },
            "bots": {
                "add": False,
                "del": False,
                "list": []
            },
            "antijs": {
                "add": False,
                "del": False,
                "list": []
            },
            "banned": {
                "add": False,
                "del": False,
                "list": []
            }
        }
        if not "stats" in self.db:
            self.db['stats'] = self.stats
            self.stats = self.db["stats"]
        else:
            self.stats = self.db["stats"]
        if self.settings["restartpoint"] != None:
            self.client.sendMessage(self.settings["restartpoint"], "Activated")
            self.settings["restartpoint"] = None

    def banned(self, user):
        if user in self.stats["banned"]["list"]: pass
        else: self.stats["banned"]["list"].append(user)
        return 1

    def mycmd(self, text, rname, sname):
        cmd = ""
        pesan = text
        if pesan.startswith(rname):
            pesan = pesan.replace(rname, "", 1)
            if " & " in text:
                cmd = pesan.split(" & ")
            else:
                cmd = [pesan]
        if pesan.startswith(sname):
            pesan = pesan.replace(sname, "", 1)
            if " & " in text:
                cmd = pesan.split(" & ")
            else:
                cmd = [pesan]
        return cmd

    def access(self, good):
        u = self.master
        if good in u:
            return 0
        u = self.stats['owners']['list']
        if good in u:
            return 1
        u = self.stats['admins']['list']
        if good in u:
            return 2
        u = self.stats['staffs']['list']
        if good in u:
            return 3
        u = self.stats['bots']['list']
        if good in u:
            return 4
        u = self.stats['antijs']['list']
        if good in u:
            return 5
        return 1000

    def notif_kick_from_group(self, op):
        kickgroup = op.param1
        kicker = op.param2
        kicked = op.param3
        if not kicked in self.uid:
            if self.settings["strictmode"] and self.access(kicker) > 5:
                self.client.acceptGroupInvitation(kickgroup)
                self.client.kickoutFromGroup(kickgroup, [kicker])
                try:
                    good = []
                    good.append(kicked)
                    for _mid in self.stats['bots']['list']:
                        good.append(_mid)
                    for _mid in self.stats['owners']['list']:
                        good.append(_mid)
                    self.client.inviteIntoGroup(kickgroup, good)
                except TalkException as merror:
                    if merror.code == 10:
                        print("BOT NOT IN ROOM {}".format(self.client.getGroup(kickgroup).name))
                    elif merror.code == 35:
                        print("LIMITED")
                        gc = self.client.getCompactGroup(kickgroup)
                        if gc.preventedJoinByTicket == True:
                            gc.preventedJoinByTicket = False
                            if links == True:
                                gc.preventedJoinByTicket = False
                                self.client.updateGroup(gc)
                            link = self.client.reissueGroupTicket(kickgroup)
                            for sprt in self.stats['bots']['list']:
                                self.client.sendMessage(sprt, "%s %s" %(kickgroup, link))
                            for own in self.stats['owners']['list']:
                                self.client.sendMessage(own, "Room Target:\nline.me/R/ti/g/" + link)
                self.banned(kicker)
            elif self.access(kicked) < 6 and self.access(kicker) > 5:
                self.client.acceptGroupInvitation(kickgroup)
                self.client.kickoutFromGroup(kickgroup, [kicker])
                try:
                    good = []
                    good.append(kicked)
                    for _mid in self.stats['bots']['list']:
                        good.append(_mid)
                    for _mid in self.stats['owners']['list']:
                        good.append(_mid)
                    self.client.inviteIntoGroup(kickgroup, good)
                except TalkException as merror:
                    if merror.code == 10:
                        print("BOT NOT IN ROOM {}".format(self.client.getGroup(kickgroup).name))
                    elif merror.code == 35:
                        print("LIMITED")
                        gc = self.client.getCompactGroup(kickgroup)
                        if gc.preventedJoinByTicket == True:
                            gc.preventedJoinByTicket = False
                            if links == True:
                                gc.preventedJoinByTicket = False
                                self.client.updateGroup(gc)
                            link = self.client.reissueGroupTicket(kickgroup)
                            for sprt in self.stats['bots']['list']:
                                self.client.sendMessage(sprt, "%s %s" %(kickgroup, link))
                            for own in self.stats['owners']['list']:
                                self.client.sendMessage(own, "Room Target:\nline.me/R/ti/g/" + link)
                self.banned(kicker)

    def notif_invite_into_group(self, op):
        invites = op.param3.split("\x1e")
        inviter = op.param2
        group = op.param1
        if self.uid in invites:
            if self.access(inviter) == 0:
                self.client.acceptGroupInvitation(group)

    def notif_accept_group_invite(self, op):
        invited = op.param2
        group = op.param1
        if self.settings["strictmode"]:
            if invited in self.stats['bots']['list']:
                self.client.leaveGroup(group)
            elif invited in self.stats['banned']['list']:
                self.client.kickoutFromGroup(group, [invited])

    def notif_kick(self, op):
        self.count["countKick"] += 1

    def notif_invite(self, op):
        self.count["countInvite"] += 1

    def notif_cancel(self, op):
        self.count["countCancel"] += 1

    def receive_message(self, op):
        try:
            msg = op.message
            to = msg.to
            of = msg._from
            iz = msg.id
            text = msg.text
            if msg.contentType == 0:
                if None == msg.text:
                    return
                if text.lower().startswith(self.settings["rname"].lower() + " "):
                    rname = self.settings["rname"].lower() + " "
                else:
                    rname = self.settings["rname"].lower()
                if text.lower().startswith(self.settings["sname"].lower() + " "):
                    sname = self.settings["sname"].lower() + " "
                else:
                    sname = self.settings["sname"].lower()
                if msg.toType == 0:
                    if self.access(of) < 6:
                        if not rname in text.lower():
                            spl = text.split(" ")
                            if len(spl) == 2:
                                gid = msg.text.split()[0]
                                link = msg.text.split()[1]
                                self.client.acceptGroupInvitationByTicket(gid, link)
                    if self.access(of) < 3:
                        if "/ti/g/" in text:
                            regex = re.compile(r"(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?")
                            links = regex.findall(text)
                            tickets = []
                            gids = self.client.getGroupIdsJoined()
                            for link in links:
                                if link not in tickets:
                                    tickets.append(link)
                            for ticket in tickets:
                                try:
                                    group = self.client.findGroupByTicket(ticket)
                                except:
                                    continue
                                if group.id in gids:
                                    continue
                                self.client.acceptGroupInvitationByTicket(group.id, ticket)
                    if self.access(of) == 4:
                        if "/ti/g/" in text:
                            regex = re.compile(r"(?:line\:\/|line\.me\/R)\/ti\/g\/([a-zA-Z0-9_-]+)?")
                            links = regex.findall(text)
                            tickets = []
                            gids = self.client.getGroupIdsJoined()
                            for link in links:
                                if link not in tickets:
                                    tickets.append(link)
                            for ticket in tickets:
                                try:
                                    group = self.client.findGroupByTicket(ticket)
                                except:
                                    continue
                                if group.id in gids:
                                    continue
                                self.client.acceptGroupInvitationByTicket(group.id, ticket)
                                self.settings["strictmode"] = False
                txt = msg.text.lower()
                txt = " ".join(txt.split())
                mykey = []
                if (txt.startswith(rname) or txt.startswith(sname)):
                    mykey = self.mycmd(txt, rname, sname)
                else:
                    mykey = []
                if txt == "ping": self.client.sendMessage(to, "PING!!!")
                if txt == "rname" and self.access(of) < 4:
                    self.client.sendMessage(to, self.settings['rname'].title())
                if txt == "sname" and self.access(of) < 4:
                    self.client.sendMessage(to, self.settings['sname'].title())
                if txt == "speed" and self.access(of) < 6:
                    run = time.time()
                    self.client.getProfile() 
                    start = time.time() - run
                    self.client.sendMessage(to, "Speed: %.4f ms" %(start))
                for a in mykey:
                    txt = a
                    if self.access(of) == 0:
                        if txt == "help":
                            if self.settings["rname"] == "": keyrname = ""
                            else: keyrname = self.settings["rname"].title() + " "
                            cmds = "HELLTERHEAD CORP."
                            cmds += "\n[ Single Protect v1.0 ]"
                            cmds += "\n\nSquad Name: " + self.settings['sname'].capitalize()
                            cmds += "\n────────────────────"
                            cmds += "\n\n❏ PROTECTION"
                            cmds += "\n    1. " + keyrname + "strictmode /"
                            cmds += "\n    2. " + keyrname + "cban"
                            cmds += "\n    3. " + keyrname + "bye"
                            cmds += "\n    4. " + keyrname + "groups"
                            cmds += "\n\n❏ UTILITY"
                            cmds += "\n    5. " + keyrname + "uprname *"
                            cmds += "\n    6. " + keyrname + "upsname *"
                            cmds += "\n    7. " + keyrname + "upname *"
                            cmds += "\n    8. " + keyrname + "upbio *"
                            cmds += "\n    9. " + keyrname + "uppict ^"
                            cmds += "\n    10. " + keyrname + "abort"
                            cmds += "\n    11. " + keyrname + "check"
                            cmds += "\n    12. " + keyrname + "reboot"
                            cmds += "\n    13. " + keyrname + "kick ~"
                            cmds += "\n    14. " + keyrname + "invite ~"
                            cmds += "\n\n❏ PROMOTE/DEMOTE"
                            cmds += "\n    15. " + keyrname + "ban add ^"
                            cmds += "\n    16. " + keyrname + "ban del ^"
                            cmds += "\n    17. " + keyrname + "bot add ^"
                            cmds += "\n    18. " + keyrname + "bot del ^"
                            cmds += "\n    19. " + keyrname + "ajs add ^"
                            cmds += "\n    20. " + keyrname + "ajs del ^"
                            cmds += "\n    21. " + keyrname + "own add ^"
                            cmds += "\n    22. " + keyrname + "own del ^"
                            cmds += "\n    23. " + keyrname + "adm add ^"
                            cmds += "\n    23. " + keyrname + "adm del ^"
                            cmds += "\n    25. " + keyrname + "staff add ^"
                            cmds += "\n    26. " + keyrname + "staff del ^"
                            cmds += "\n\n❏ ACCESS"
                            cmds += "\n    27. " + keyrname + "banlist"
                            cmds += "\n    28. " + keyrname + "botlist"
                            cmds += "\n    29. " + keyrname + "ajslist"
                            cmds += "\n    30. " + keyrname + "ownlist"
                            cmds += "\n    31. " + keyrname + "admlist"
                            cmds += "\n    32. " + keyrname + "stafflist"
                            cmds += "\n\n────────────────────"
                            cmds += "\n[ ~ ] Reply"
                            cmds += "\n[ / ] Boolean"
                            cmds += "\n[ * ] Query"
                            cmds += "\n[ ^ ] Upload"
                            self.client.sendMessage(to, cmds)
                        elif txt == "check":
                            cstat = {"kick": "", "invite": ""}
                            try: self.client.inviteIntoGroup(to, [self.client.getProfile().mid]); cstat["invite"] = "⭕"
                            except: cstat["invite"] = "❌"
                            try: self.client.kickoutFromGroup(to, [self.client.getProfile().mid]); cstat["kick"] = "⭕"
                            except: cstat["kick"] = "❌"
                            msgs = "BOT CHECK\n"
                            msgs += "\n{}    Kick".format(cstat["kick"])
                            msgs += "\n{}    Invite".format(cstat["invite"])
                            msgs += "\n────────────────────"
                            msgs += "\nKick: {}".format(self.count["countKick"])
                            msgs += "\nInvite: {}".format(self.count["countInvite"])
                            msgs += "\nCancel: {}".format(self.count["countCancel"])
                            self.client.sendMessage(to, msgs)
                        elif txt == "groups":
                            if msg.toType == 2:
                                glist = self.client.getGroupIdsJoined()
                                glists = self.client.getGroups(glist)
                                no = 1
                                msgs = "GROUPLIST\n"
                                for ids in glists:
                                    msgs += "\n%i. %s" %(no, ids.name) + " (" + str(len(ids.members)) + ")"
                                    no = (no+1)
                                msgs += "\n\nTotal %i Groups" %len(glists)
                                self.client.sendMessage(to, "{}".format(str(msgs)))
                        elif txt == "abort":
                            self.stats["banned"]["add"] = False
                            self.stats["banned"]["del"] = False
                            self.stats["bots"]["add"] = False
                            self.stats["bots"]["del"] = False
                            self.stats["antijs"]["add"] = False
                            self.stats["antijs"]["del"] = False
                            self.stats["owners"]["add"] = False
                            self.stats["owners"]["del"] = False
                            self.stats["admins"]["add"] = False
                            self.stats["admins"]["del"] = False
                            self.stats["staffs"]["add"] = False
                            self.stats["staffs"]["del"] = False
                            self.settings["pictprofile"] = False
                            self.settings["pictprofile"] = False
                            self.client.sendMessage(to, "Command aborted.")
                        elif txt == "reboot":
                            self.client.sendMessage(to, "Restarting bot system...")
                            self.settings["restartpoint"] = to
                            time.sleep(1)
                            python3 = sys.executable
                            os.execl(python3, python3, *sys.argv)
                        elif txt == "bye":
                            self.client.leaveGroup(to)
                        elif txt == "cban":
                            amount = len(self.stats["banned"]["list"])
                            self.stats["banned"]["list"] = []
                            self.client.sendMessage(to, "Unbanned %s people." %amount)
                        elif txt == "kick":
                            if msg.relatedMessageId != None:
                                hlth = self.client.getRecentMessagesV2(to, 1001)
                                for i in hlth:
                                    if i.id in msg.relatedMessageId:
                                        self.client.kickoutFromGroup(to, [i._from])
                        elif txt == "invite":
                            if msg.relatedMessageId != None:
                                hlth = self.client.getRecentMessagesV2(to, 1001)
                                for i in hlth:
                                    if i.id in msg.relatedMessageId:
                                        self.client.findAndAddContactsByMid(i._from)
                                        self.client.inviteIntoGroup(to, [i._from])
                        elif txt.startswith("strictmode "):
                            spl = txt.replace("strictmode ", "")
                            if spl == "on":
                                if self.settings['strictmode']:
                                    self.client.sendMessage(to, "Strictmode already enabled.")
                                else:
                                    self.settings["strictmode"] = True
                                    self.client.sendMessage(to, "Strictmode enabled.")
                                self.client.leaveGroup(to)
                            elif spl == "off":
                                if self.settings['strictmode']:
                                    self.settings["strictmode"] = False
                                    self.client.sendMessage(to, "Strictmode disabled.")
                                else: self.client.sendMessage(to, "Strictmode already disabled.")
                        elif txt.startswith("ban "):
                            spl = txt.replace("ban ", "")
                            if spl == "add":
                                self.stats["banned"]["add"] = True
                                self.client.sendMessage(to, "Send contact...")
                            elif spl == "del":
                                self.stats["banned"]["del"] = True
                                self.client.sendMessage(to, "Send contact...")
                        elif txt.startswith("bot "):
                            spl = txt.replace("bot ", "")
                            if spl == "add":
                                self.stats["bots"]["add"] = True
                                self.client.sendMessage(to, "Send contact...")
                            elif spl == "del":
                                self.stats["bots"]["del"] = True
                                self.client.sendMessage(to, "Send contact...")
                        elif txt.startswith("ajs "):
                            spl = txt.replace("ajs ", "")
                            if spl == "add":
                                self.stats["antijs"]["add"] = True
                                self.client.sendMessage(to, "Send contact...")
                            elif spl == "del":
                                self.stats["antijs"]["del"] = True
                                self.client.sendMessage(to, "Send contact...")
                        elif txt.startswith("own "):
                            spl = txt.replace("own ", "")
                            if spl == "add":
                                self.stats["owners"]["add"] = True
                                self.client.sendMessage(to, "Send contact...")
                            elif spl == "del":
                                self.stats["owners"]["del"] = True
                                self.client.sendMessage(to, "Send contact...")
                        elif txt.startswith("adm "):
                            spl = txt.replace("adm ", "")
                            if spl == "add":
                                self.stats["admins"]["add"] = True
                                self.client.sendMessage(to, "Send contact...")
                            elif spl == "del":
                                self.stats["admins"]["del"] = True
                                self.client.sendMessage(to, "Send contact...")
                        elif txt.startswith("staff "):
                            spl = txt.replace("staff ", "")
                            if spl == "add":
                                self.stats["staffs"]["add"] = True
                                self.client.sendMessage(to, "Send contact...")
                            elif spl == "del":
                                self.stats["staffs"]["del"] = True
                                self.client.sendMessage(to, "Send contact...")
                        elif txt == "banlist":
                            if msg.toType == 2:
                                user = self.stats["banned"]["list"]
                                no = 1
                                msgs = "BANNED LIST\n"
                                for ids in user:
                                    users = self.client.getContact(ids)
                                    msgs += "\n%i. %s" %(no, users.displayName)
                                    no = (no+1)
                                msgs += "\n\nTotal %i Banned" %len(user)
                                self.client.sendMessage(to, "{}".format(str(msgs)))
                        elif txt == "botlist":
                            if msg.toType == 2:
                                user = self.stats["bots"]["list"]
                                no = 1
                                msgs = "BOT LIST\n"
                                for ids in user:
                                    users = self.client.getContact(ids)
                                    msgs += "\n%i. %s" %(no, users.displayName)
                                    no = (no+1)
                                msgs += "\n\nTotal %i Bots" %len(user)
                                self.client.sendMessage(to, "{}".format(str(msgs)))
                        elif txt == "ajslist":
                            if msg.toType == 2:
                                user = self.stats["antijs"]["list"]
                                no = 1
                                msgs = "ANTI JS LIST\n"
                                for ids in user:
                                    users = self.client.getContact(ids)
                                    msgs += "\n%i. %s" %(no, users.displayName)
                                    no = (no+1)
                                msgs += "\n\nTotal %i Antijs" %len(user)
                                self.client.sendMessage(to, "{}".format(str(msgs)))
                        elif txt == "ownlist":
                            if msg.toType == 2:
                                user = self.stats["owners"]["list"]
                                no = 1
                                msgs = "OWNER LIST\n"
                                for ids in user:
                                    users = self.client.getContact(ids)
                                    msgs += "\n%i. %s" %(no, users.displayName)
                                    no = (no+1)
                                msgs += "\n\nTotal %i Owners" %len(user)
                                self.client.sendMessage(to, "{}".format(str(msgs)))
                        elif txt == "admlist":
                            if msg.toType == 2:
                                user = self.stats["admins"]["list"]
                                no = 1
                                msgs = "ADMIN LIST\n"
                                for ids in user:
                                    users = self.client.getContact(ids)
                                    msgs += "\n%i. %s" %(no, users.displayName)
                                    no = (no+1)
                                msgs += "\n\nTotal %i Admins" %len(user)
                                self.client.sendMessage(to, "{}".format(str(msgs)))
                        elif txt == "stafflist":
                            if msg.toType == 2:
                                user = self.stats["staffs"]["list"]
                                no = 1
                                msgs = "STAFF LIST\n"
                                for ids in user:
                                    users = self.client.getContact(ids)
                                    msgs += "\n%i. %s" %(no, users.displayName)
                                    no = (no+1)
                                msgs += "\n\nTotal %i Staffs" %len(user)
                                self.client.sendMessage(to, "{}".format(str(msgs)))
                        elif txt.startswith("uprname "):
                            string = txt.split(" ")[1]
                            self.settings['rname'] = string
                            self.client.sendMessage(to, "Responsename update to {}".format(self.settings['rname']))
                        elif txt.startswith("upsname "):
                            string = txt.split(" ")[1]
                            self.settings['sname'] = string
                            self.client.sendMessage(to, "Squadname update to {}".format(self.settings['sname']))
                        elif txt.startswith("upbio "):
                            string = txt.split("upbio ")[1]
                            if len(string) <= 500:
                                bio = self.client.getProfile()
                                bio.statusMessage = string
                                self.client.updateProfile(bio)
                                self.client.sendMessage(to, "Bio updated to {}".format(string))
                            else: self.client.sendMessage(to, "Text is limit.")
                        elif txt.startswith("upname "):
                            string = txt.split("upname ")[1]
                            if len(string) <= 20:
                                name = self.client.getProfile()
                                name.displayName = string.title()
                                self.client.updateProfile(name)
                                self.client.sendMessage(to, "Name updated to {}".format(string.title()))
                            else: self.client.sendMessage(to, "Text is limit.")
                        elif txt == "uppict":
                            self.settings["pictprofile"] = True
                            self.client.sendMessage(to, "Send picture...")
            if msg.contentType == 1:
                if self.access(of) == 0:
                    if self.settings["pictprofile"] == True:
                        path = self.client.downloadObjectMsg(iz)
                        self.client.updateProfilePicture(path)
                        self.settings["pictprofile"] = False
                        self.client.sendMessage(to, "Picture profile updated.")
            if msg.contentType == 13:
                if self.access(of) == 0:
                    if self.stats["banned"]["add"] == True:
                        if msg.contentMetadata["mid"] not in self.client.profile.mid:
                            if msg.contentMetadata["mid"] in self.stats["banned"]["list"]:
                                self.client.sendMessage(to, "{} already in blacklist.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                self.stats["banned"]["add"] = False
                            else:
                                if msg.contentMetadata["mid"] not in (self.stats["owners"]["list"], self.stats["admins"]["list"], self.stats["staffs"]["list"], self.stats["bots"]["list"], self.stats["antijs"]["list"]):
                                    self.stats["banned"]["list"].append(msg.contentMetadata["mid"])
                                    self.client.sendMessage(to, "{} added in blacklist.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                    self.stats["banned"]["add"] = False
                                else: self.client.sendMessage(to, "User in whitelist.")
                                self.stats["banned"]["add"] = False
                    elif self.stats["banned"]["del"] == True:
                        if msg.contentMetadata["mid"] not in self.client.profile.mid:
                            if msg.contentMetadata["mid"] in self.stats["banned"]["list"]:
                                self.stats["banned"]["list"].remove(msg.contentMetadata["mid"])
                                self.client.sendMessage(to, "{} removed from blacklist.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                self.stats["banned"]["del"] = False
                            else: self.client.sendMessage(to, "User not in blacklist.")
                            self.stats["banned"]["del"] = False
                    elif self.stats["bots"]["add"] == True:
                        if msg.contentMetadata["mid"] not in self.client.profile.mid:
                            if msg.contentMetadata["mid"] in self.stats["bots"]["list"]:
                                self.client.sendMessage(to, "{} already in bots.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                self.stats["bots"]["add"] = False
                            else:
                                if msg.contentMetadata["mid"] not in self.stats["banned"]["list"]:
                                    self.stats["bots"]["list"].append(msg.contentMetadata["mid"])
                                    self.client.sendMessage(to, "{} added in bots.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                    self.stats["bots"]["add"] = False
                                else: self.client.sendMessage(to, "User in blacklist.")
                                self.stats["bots"]["add"] = False
                    elif self.stats["bots"]["del"] == True:
                        if msg.contentMetadata["mid"] not in self.client.profile.mid:
                            if msg.contentMetadata["mid"] in self.stats["bots"]["list"]:
                                self.stats["bots"]["list"].remove(msg.contentMetadata["mid"])
                                self.client.sendMessage(to, "{} removed from bots.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                self.stats["bots"]["del"] = False
                            else: self.client.sendMessage(to, "User not in bots.")
                            self.stats["bots"]["del"] = False
                    elif self.stats["antijs"]["add"] == True:
                        if msg.contentMetadata["mid"] not in self.client.profile.mid:
                            if msg.contentMetadata["mid"] in self.stats["antijs"]["list"]:
                                self.client.sendMessage(to, "{} already in antijs.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                self.stats["antijs"]["add"] = False
                            else:
                                if msg.contentMetadata["mid"] not in self.stats["banned"]["list"]:
                                    self.stats["antijs"]["list"].append(msg.contentMetadata["mid"])
                                    self.client.sendMessage(to, "{} added in antijs.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                    self.stats["antijs"]["add"] = False
                                else: self.client.sendMessage(to, "User in blacklist.")
                                self.stats["antijs"]["add"] = False
                    elif self.stats["antijs"]["del"] == True:
                        if msg.contentMetadata["mid"] not in self.client.profile.mid:
                            if msg.contentMetadata["mid"] in self.stats["antijs"]["list"]:
                                self.stats["antijs"]["list"].remove(msg.contentMetadata["mid"])
                                self.client.sendMessage(to, "{} removed from antijs.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                self.stats["antijs"]["del"] = False
                            else: self.client.sendMessage(to, "User not in antijs.")
                            self.stats["antijs"]["del"] = False
                    elif self.stats["owners"]["add"] == True:
                        if msg.contentMetadata["mid"] not in self.client.profile.mid:
                            if msg.contentMetadata["mid"] in self.stats["owners"]["list"]:
                                self.client.sendMessage(to, "{} already in owners.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                self.stats["owners"]["add"] = False
                            else:
                                if msg.contentMetadata["mid"] not in self.stats["banned"]["list"]:
                                    self.stats["owners"]["list"].append(msg.contentMetadata["mid"])
                                    self.client.sendMessage(to, "{} added in owners.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                    self.stats["owners"]["add"] = False
                                else: self.client.sendMessage(to, "User in blacklist.")
                                self.stats["owners"]["add"] = False
                    elif self.stats["owners"]["del"] == True:
                        if msg.contentMetadata["mid"] not in self.client.profile.mid:
                            if msg.contentMetadata["mid"] in self.stats["owners"]["list"]:
                                self.stats["owners"]["list"].remove(msg.contentMetadata["mid"])
                                self.client.sendMessage(to, "{} removed from owners.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                self.stats["owners"]["del"] = False
                            else: self.client.sendMessage(to, "User not in owners.")
                            self.stats["owners"]["del"] = False
                    elif self.stats["admins"]["add"] == True:
                        if msg.contentMetadata["mid"] not in self.client.profile.mid:
                            if msg.contentMetadata["mid"] in self.stats["admins"]["list"]:
                                self.client.sendMessage(to, "{} already in admins.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                self.stats["admins"]["add"] = False
                            else:
                                if msg.contentMetadata["mid"] not in self.stats["banned"]["list"]:
                                    self.stats["admins"]["list"].append(msg.contentMetadata["mid"])
                                    self.client.sendMessage(to, "{} added in admins.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                    self.stats["admins"]["add"] = False
                                else: self.client.sendMessage(to, "User in blacklist.")
                                self.stats["admins"]["add"] = False
                    elif self.stats["admins"]["del"] == True:
                        if msg.contentMetadata["mid"] not in self.client.profile.mid:
                            if msg.contentMetadata["mid"] in self.stats["admins"]["list"]:
                                self.stats["admins"]["list"].remove(msg.contentMetadata["mid"])
                                self.client.sendMessage(to, "{} removed from admins.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                self.stats["admins"]["del"] = False
                            else: self.client.sendMessage(to, "User not in admins.")
                            self.stats["admins"]["del"] = False
                    elif self.stats["staffs"]["add"] == True:
                        if msg.contentMetadata["mid"] not in self.client.profile.mid:
                            if msg.contentMetadata["mid"] in self.stats["staffs"]["list"]:
                                self.client.sendMessage(to, "{} already in staffs.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                self.stats["staffs"]["add"] = False
                            else:
                                if msg.contentMetadata["mid"] not in self.stats["banned"]["list"]:
                                    self.stats["staffs"]["list"].append(msg.contentMetadata["mid"])
                                    self.client.sendMessage(to, "{} added in staffs.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                    self.stats["staffs"]["add"] = False
                                else: self.client.sendMessage(to, "User in blacklist.")
                                self.stats["staffs"]["add"] = False
                    elif self.stats["staffs"]["del"] == True:
                        if msg.contentMetadata["mid"] not in self.client.profile.mid:
                            if msg.contentMetadata["mid"] in self.stats["staffs"]["list"]:
                                self.stats["staffs"]["list"].remove(msg.contentMetadata["mid"])
                                self.client.sendMessage(to, "{} removed from staffs.".format(self.client.getContact(msg.contentMetadata["mid"]).displayName))
                                self.stats["staffs"]["del"] = False
                            else: self.client.sendMessage(to, "User not in staffs.")
                            self.stats["staffs"]["del"] = False
        except Exception as e:
            e = traceback.format_exc()
            if "EOFError" in e: pass
            elif "ShouldSyncException" in e or "LOG_OUT" in e:
                python3 = sys.executable
                os.execl(python3, python3, *sys.argv)
            else: traceback.print_exc()
