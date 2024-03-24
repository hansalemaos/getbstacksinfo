import regex as re
import subprocess
from pidconnectioninfos import (
    get_all_imagenames_and_pid,
    get_procs_with_open_file_pids_only,
    get_network_connections_from_process,
    invisibledict,
)
from regex4numbers import number_between
from list_all_files_recursively import get_folder_file_complete_path
import os 
from . import (
    get_bluestacks_programm_data_folder,
)

noregex = re.compile(r"^\d+$")
tcpregex = re.compile(R"\s+\b(?:TCP|UDP)\b\s+")
regex = number_between(start=0, end=65536, fullnumberreplacement="\\d")
regex2 = r"(?<=(?:\.\d{1,3}))(:?:" + regex + r"\b\s+)"
regexcompiled = re.compile(regex2)


def get_real_adb(adbexe="adb.exe"):
    adbexe = adbexe.lower()
    alladbs = [h for h in get_all_imagenames_and_pid() if h[0].lower() == adbexe]
    for adbpa, pidi in alladbs:
        prx = subprocess.run(
            f"""wmic process where (ProcessId={pidi}) get CommandLine""",
            shell=False,
            capture_output=True,
            **invisibledict,
        )
        if (
            b" --reply-fd " in prx.stdout
            or " tcp:5037 " in prx.stdout
            or " fork-server " in prx.stdout
        ):
            return (adbpa, pidi)

    return -1


def create_port_pid_lookup():
    px = subprocess.run("netstat -ano", capture_output=True, **invisibledict)
    stdo, stde = px.stdout.decode("utf-8", errors="backslashreplace"), px.stderr

    resus = [
        [
            hh.rstrip().rsplit(maxsplit=1)[-1],
            regexcompiled.findall(hh.rstrip().rsplit(maxsplit=1)[0]),
            h,
        ]
        for h in stdo.splitlines()
        if (hh := h.strip())
    ]
    resus = [
        [
            hh[0].strip(),
            [r.strip(": ") for r in hh[1]],
            hh[2],
            [ee.strip() for ee in tcpregex.findall(hh[2])],
        ]
        for hh in resus
        if noregex.match(hh[0])
    ]
    resus = [x for x in resus if x[1]]
    connectiondict_pid = {}
    connectiondict_hwnd = {}
    connectiondict_protocol = {}
    for ba in resus:
        try:
            if not ba[3]:
                continue
            connectiondict_pid.setdefault(int(ba[0]), set()).update(map(int, ba[1]))
            for v in map(int, ba[1]):
                connectiondict_hwnd.setdefault(v, set()).add(int(ba[0]))
            for v in map(int, ba[1]):
                connectiondict_protocol.setdefault(v, set()).add(ba[-1][-1])
        except Exception:
            pass
    return connectiondict_pid, connectiondict_hwnd, connectiondict_protocol


def get_all_bluestacks_online_instances(adbexe="adb.exe"):
    possible_adb_clients = {}
    (adbpa, rightadbproc) = get_real_adb(adbexe=adbexe)
    (
        connectiondict_pid,
        connectiondict_hwnd,
        connectiondict_protocol,
    ) = create_port_pid_lookup()
    for port in connectiondict_pid[rightadbproc]:
        pid = connectiondict_hwnd.get(port, [])
        for piddi in pid:
            if (piddi) == rightadbproc:
                if port:
                    possible_adb_clients[port] = piddi

    adbdataupdate = {}
    ports = list(possible_adb_clients)
    fatr = get_network_connections_from_process(ports=ports, always_ignore=(0, 4))
    openadbconnections = fatr[rightadbproc]["found_ports"]
    for key, item in fatr.items():
        try:
            if key == rightadbproc:
                continue
            if parseresu := openadbconnections.intersection(item["found_ports"]):
                adbportforinstance = sorted(parseresu)[0]
                pidofinstance = key
                instancedata = item["family_tree"]
                exefile = list(instancedata.keys())[0][0]
                cmdline = list(instancedata.keys())[0][1]
                instancename = cmdline.rsplit(maxsplit=1)[-1].strip("\"' ")
                adbdataupdate[instancename] = {
                    "port": adbportforinstance,
                    "cmdline": cmdline,
                    "exefile": exefile,
                    "pid": pidofinstance,
                    "running": True,
                    "connected": True,
                    "locking_pids":[]
                }
        except Exception:
            pass
    return adbdataupdate

def get_offline_and_online_bluestacks_instances(adbexe="adb.exe"):
    get_all_bluestacks_online_instances(adbexe=adbexe)
    updatedbluestacks = get_all_bluestacks_online_instances(adbexe=adbexe)

    (
        bstconfigpath_folder,
        bstconfigpath,
        bstconfigpath_folder_short,
        bstconfigpath_short,
        bstexe_folder,
        bsthdplayer,
        bstexe_folder_short,
        bsthdplayer_short,
        vboxmanager,
        vboxmanager_short,
    ) = get_bluestacks_programm_data_folder()
    accessedbluestacksimages=[]
    allbluestacksfiles = get_folder_file_complete_path(bstconfigpath_folder)
    allbluestacksfiles = [f for f in allbluestacksfiles if f.file.lower() == "data.vhdx"]
    for file in allbluestacksfiles:
        try:
            if (instancenameoffline := file.folder.split(os.sep)[-1]) in updatedbluestacks:
                continue
            resu=get_procs_with_open_file_pids_only(file.path)
            accessedbluestacksimages.append([instancenameoffline,file,resu])
            updatedbluestacks[instancenameoffline] = {
                "port": -1,
                "cmdline": f"{bsthdplayer_short} --instance {instancenameoffline}",
                "exefile": f"""startcommand = rf'start /min "" {bsthdplayer_short} --instance {instancenameoffline}""",
                "pid": -1,
                "running": False,
                "connected": False,
                "locking_pids": resu.copy(),
            }
        except Exception as e:
            print(e)

    return updatedbluestacks