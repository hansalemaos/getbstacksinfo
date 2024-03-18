import os
from list_all_files_recursively import get_folder_file_complete_path
from reggisearch import search_values
from tkkillablethreads import ExecuteAsThreadedTask
import subprocess
from nodepsutils import (
    get_short_path_name_cached,
    get_information_from_all_procs_with_connections,
    get_information_from_all_procs,
    kill_process,
    start_detached_process,
    invisibledict,
    ipreg,
    touch,
)
import time
from ctypes_window_info import get_window_infos
import ctypes
from ctypes import wintypes as w
import sys

windll = ctypes.LibraryLoader(ctypes.WinDLL)
user32 = windll.user32
user32.GetForegroundWindow.argtypes = ()
user32.GetForegroundWindow.restype = w.HWND
user32.ShowWindow.argtypes = w.HWND, w.BOOL
user32.ShowWindow.restype = w.BOOL


class WinFu:
    def __init__(self, fu=None, args=(), kwargs=None):
        if not kwargs:
            kwargs = {}
        self.fu = fu
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        newargs = args + self.args
        newkwargs = self.kwargs.copy()
        newkwargs.update(kwargs)
        return self.fu(*newargs, **newkwargs)


def window_HIDE(hwnd: int):
    user32.ShowWindow(hwnd, 0)


def window_NORMAL(hwnd: int):
    user32.ShowWindow(hwnd, 1)


def window_SHOWMINIMIZED(hwnd: int):
    user32.ShowWindow(hwnd, 2)


def window_MAXIMIZE(hwnd: int):
    user32.ShowWindow(hwnd, 3)


def window_SHOWNOACTIVATE(hwnd: int):
    user32.ShowWindow(hwnd, 4)


def window_SHOW(hwnd: int):
    user32.ShowWindow(hwnd, 5)


def window_MINIMIZE(hwnd: int):
    user32.ShowWindow(hwnd, 6)


def window_SHOWMINNOACTIVE(hwnd: int):
    user32.ShowWindow(hwnd, 7)


def window_SHOWNA(hwnd: int):
    user32.ShowWindow(hwnd, 8)


def window_RESTORE(hwnd: int):
    user32.ShowWindow(hwnd, 9)


def window_SHOWDEFAULT(hwnd: int):
    user32.ShowWindow(hwnd, 10)


def window_FORCEMINIMIZE(hwnd: int):
    user32.ShowWindow(hwnd, 11)


def resize_window(hwnd: int, position: tuple):
    user32.SetProcessDPIAware()
    user32.MoveWindow(hwnd, *position, True)


def kill_all_bluestacks_exe():
    killprocs = [
        """taskkill /IM "BlueStacksAppplayerWeb.exe" /F""",
        """taskkill /IM "BlueStacksHelper.exe" /F""",
        """taskkill /IM "BlueStacksUninstaller.exe" /F""",
        """taskkill /IM "BstkSVC.exe" /F""",
        """taskkill /IM "BstkVMMgr.exe" /F""",
        """taskkill /IM "HD-Adb.exe" /F""",
        """taskkill /IM "HD-CheckCpu.exe" /F""",
        """taskkill /IM "HD-ComRegistrar.exe" /F""",
        """taskkill /IM "HD-DataManager.exe" /F""",
        """taskkill /IM "HD-DiskCompaction.exe" /F""",
        """taskkill /IM "HD-DiskFormatCheck.exe" /F""",
        """taskkill /IM "HD-EnableHyperV.exe" /F""",
        """taskkill /IM "HD-ForceGPU.exe" /F""",
        """taskkill /IM "HD-GLCheck.exe" /F""",
        """taskkill /IM "HD-Hvutl.exe" /F""",
        """taskkill /IM "HD-LogCollector.exe" /F""",
        """taskkill /IM "HD-MultiInstanceManager.exe" /F""",
        """taskkill /IM "HD-Player.exe" /F""",
    ]

    for x in killprocs:
        try:
            subprocess.run(
                x,
                **invisibledict,
                timeout=10,
            )
        except Exception:
            pass


def change_root_fastboot_normal(xmldatapath):
    kill_all_bluestacks_exe()
    with open(xmldatapath, "r", encoding="utf-8") as f:
        xmldata = f.read()
    allnewxmls = xmldata.replace(
        """ format="VDI" type="Readonly"/>""", """ format="VDI" type="Normal"/>"""
    ).replace(
        """ format="VHD" type="Readonly"/>""", """ format="VHD" type="Normal"/>"""
    )

    with open(xmldatapath, "w", encoding="utf-8") as f:
        f.write(allnewxmls)


def change_root_fastboot_readonly(xmldatapath):
    kill_all_bluestacks_exe()
    with open(xmldatapath, "r", encoding="utf-8") as f:
        xmldata = f.read()
    allnewxmls = xmldata.replace(
        """ format="VDI" type="Normal"/>""", """ format="VDI" type="Readonly"/>"""
    ).replace(
        """ format="VHD" type="Normal"/>""", """ format="VHD" type="Readonly"/>"""
    )

    with open(xmldatapath, "w", encoding="utf-8") as f:
        f.write(allnewxmls)


def adb_get_external_ip(adbport):
    ADB_SHELL_GET_EXTERNAL_IP = """wget -qO- ifconfig.me/ip"""
    ADB_SHELL_GET_EXTERNAL_IP2 = "wget -O - -q icanhazip.com"

    allp = get_information_from_all_procs()
    allres = []
    for k, v in allp.items():
        cmdline = v["CommandLine"]
        s1 = "tcp:5037" in cmdline
        s2 = "adb.exe " in cmdline
        s3 = "fork-server server" in cmdline
        s4 = "adb " in cmdline
        s5 = "--reply-fd" in cmdline
        hitlist = len(
            [
                x
                for x in [
                    s1,
                    s2,
                    s3,
                    s4,
                    s5,
                ]
                if x
            ]
        )
        if hitlist > 1:
            allres.append([hitlist, v["ExecutablePath"]])
    allpathsorted = sorted(allres, key=lambda x: x[0], reverse=True)
    adbpath = allpathsorted[0][1]
    adbpath_short = get_short_path_name_cached(adbpath)
    wholecmd = (
        adbpath_short + f' -s 127.0.0.1:{adbport} shell "{ADB_SHELL_GET_EXTERNAL_IP}"'
    )
    resus = subprocess.run(wholecmd, capture_output=True, **invisibledict)
    if ipreg.search(resus.stdout.decode("utf-8", "backslashreplace")):
        return ipreg.findall(resus.stdout.strip().decode("utf-8", "backslashreplace"))[
            0
        ]
    else:
        wholecmd = (
            adbpath_short
            + f' -s 127.0.0.1:{adbport} shell "{ADB_SHELL_GET_EXTERNAL_IP2}"'
        )
        resus = subprocess.run(wholecmd, capture_output=True, **invisibledict)

        if ipreg.search(resus.stdout.decode("utf-8", "backslashreplace")):
            return ipreg.findall(
                resus.stdout.strip().decode("utf-8", "backslashreplace")
            )[0]


def restartstacks(vmm, machine, working_dir, command):
    allp = get_information_from_all_procs()
    machineinstance = ""
    machinepid = ""
    for k, v in allp.items():
        if v["Caption"] == "HD-Player.exe":
            cmdline = v["CommandLine"]
            instance = cmdline.split("--instance")[-1].strip("\" '")
            if instance == machine:
                machineinstance = instance
                machinepid = v["ProcessId"]
                break
    if machineinstance:
        subprocess.run(f"{vmm} controlvm {machine} poweroff", **invisibledict)
        kill_process(machinepid, sleep_between_exitcommands=0.1)
        time.sleep(1)
    allp = get_information_from_all_procs()
    while machinepid:
        for k, v in allp.items():
            if v["Caption"] == "HD-Player.exe":
                cmdline = v["CommandLine"]
                instance = cmdline.split("--instance")[-1].strip("\" '")
                if instance == machine:
                    machineinstance = instance
                    machinepid = v["ProcessId"]
                    break
        else:
            machinepid = ""
    return startstacks(command, working_dir)


def killstacks(vmm, machine):
    allp = get_information_from_all_procs()
    machineinstance = ""
    machinepid = ""
    for k, v in allp.items():
        if v["Caption"] == "HD-Player.exe":
            cmdline = v["CommandLine"]
            instance = cmdline.split("--instance")[-1].strip("\" '")
            if instance == machine:
                machineinstance = instance
                machinepid = v["ProcessId"]
                break
    if machineinstance:
        subprocess.run(f"{vmm} controlvm {machine} poweroff", **invisibledict)
        kill_process(machinepid, sleep_between_exitcommands=0.1)


def enable_root(bstconfigpath, machine):
    with open(bstconfigpath, "rb") as f:
        data = f.read()
    data = data.replace(
        """bst.instance.""" + machine.encode("utf-8") + '''.enable_root_access="0"''',
        """bst.instance.""" + machine.encode("utf-8") + '''.enable_root_access="1"''',
    )
    with open(bstconfigpath, "wb") as f:
        f.write(data)


def disable_root(bstconfigpath, machine):
    with open(bstconfigpath, "rb") as f:
        data = f.read()
    data = data.replace(
        """bst.instance.""" + machine.encode("utf-8") + '''.enable_root_access="1"''',
        """bst.instance.""" + machine.encode("utf-8") + '''.enable_root_access="0"''',
    )
    with open(bstconfigpath, "wb") as f:
        f.write(data)


def startstacks(command, working_dir):
    return start_detached_process(
        command,
        working_dir,
        convert_exe_to_83=True,
        convert_all_to_83=False,
        accept_already_running=True,
        use_cached_shortpath=True,
        timeout_get_new_process_data=5,
        get_proc_information=True,
    )[-1]


def get_bluestacks_programm_data_folder():
    di = search_values(
        mainkeys=r"HKEY_LOCAL_MACHINE\SOFTWARE\BlueStacks_nxt", subkeys="UserDefinedDir"
    )
    bstconfigpath_folder = di[r"HKEY_LOCAL_MACHINE\SOFTWARE\BlueStacks_nxt"][
        "UserDefinedDir"
    ]
    bstconfigpath = os.path.normpath(
        os.path.join(bstconfigpath_folder, "bluestacks.conf")
    )

    di2 = search_values(
        mainkeys=r"HKEY_LOCAL_MACHINE\SOFTWARE\BlueStacks_nxt", subkeys="InstallDir"
    )
    bstexe_folder = di2[r"HKEY_LOCAL_MACHINE\SOFTWARE\BlueStacks_nxt"]["InstallDir"]
    bsthdplayer = os.path.normpath(os.path.join(bstexe_folder, "HD-Player.exe"))

    vboxmanager = os.path.normpath(os.path.join(bstexe_folder, "BstkVMMgr.exe"))

    return (
        bstconfigpath_folder,
        bstconfigpath,
        get_short_path_name_cached(bstconfigpath_folder),
        get_short_path_name_cached(bstconfigpath),
        bstexe_folder,
        bsthdplayer,
        get_short_path_name_cached(bstexe_folder),
        get_short_path_name_cached(bsthdplayer),
        vboxmanager,
        get_short_path_name_cached(vboxmanager),
    )


def get_info_bluestacks():
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
    with open(bstconfigpath_short, mode="r", encoding="utf-8") as f:
        configdata = f.read()
    configdatalines = configdata.splitlines()
    file_info_list = get_folder_file_complete_path([bstconfigpath_folder])
    vhdxfiles = {}
    bstkfiles = {}
    bstk_prev_files = {}
    already_created = {}
    hdexecute = {}
    startbatfiles = {}
    bluestacksconfdata = {}
    workingfolder = {}
    adbports = {}
    disableinternet = {}
    alldifferentkeys = set()
    enableinternet = {}
    already_created_files = {}
    ismasterinstance = {}
    modify_xml_file_normal = {}
    modify_xml_file_read_only = {}
    for file_info in file_info_list:
        lowerpath = file_info.file.lower()
        if lowerpath == "data.vhdx":
            newkey = file_info.folder.split(os.sep)[-1]
            workingfolder[newkey] = get_short_path_name_cached(file_info.folder)
            vhdxfiles[newkey] = file_info
            created_check = os.path.join(file_info.folder, "iscreated.txt")
            touch(created_check)
            already_created_files[newkey] = created_check
            with open(created_check, mode="r") as f:
                data = f.read()
            if data.strip():
                already_created[newkey] = True
            else:
                already_created[newkey] = False
            alldifferentkeys.add(newkey)
            startcommand = rf'start /min "" {bsthdplayer_short} --instance {newkey}'
            startbat = os.path.join(file_info.folder, "instancestart.bat")
            hdexecute[newkey] = startcommand
            disableinternet[
                newkey
            ] = f"{vboxmanager_short} controlvm {newkey} setlinkstate1 off"
            enableinternet[
                newkey
            ] = f"{vboxmanager_short} controlvm {newkey} setlinkstate1 on"
            with open(startbat, "w", encoding="utf-8") as f:
                f.write(startcommand)
            startbatfiles[newkey] = startbat
            for li in configdatalines:
                if f".{newkey}." in li:
                    bluestacksconfdata.setdefault(newkey, []).append(li)
                if f".{newkey}.adb_port=" in li:
                    adbports[newkey] = li.split("=")[-1].strip().strip('"')
        if lowerpath.endswith(".bstk"):
            newkey = file_info.folder.split(os.sep)[-1]

            bstkfiles[newkey] = file_info
            alldifferentkeys.add(newkey)
            with open(file_info.path, mode="r", encoding="utf-8") as f:
                data = f.read()

            if """ format="VDI" type=""" in data and """ format="VHD" type=""" in data:
                ismasterinstance[newkey] = True
                modify_xml_file_normal[newkey] = ExecuteAsThreadedTask(
                    fu=change_root_fastboot_normal,
                    args=(),
                    kwargs={
                        "xmldatapath": file_info.path,
                    },
                )
                modify_xml_file_read_only[newkey] = ExecuteAsThreadedTask(
                    fu=change_root_fastboot_readonly,
                    args=(),
                    kwargs={
                        "xmldatapath": file_info.path,
                    },
                )
            else:
                ismasterinstance[newkey] = False
                modify_xml_file_normal[newkey] = None
                modify_xml_file_read_only[newkey] = None
        if lowerpath.endswith(".bstk-prev"):
            newkey = file_info.folder.split(os.sep)[-1]

            bstk_prev_files[newkey] = file_info

            alldifferentkeys.add(newkey)
    results = {}
    for k in sorted(alldifferentkeys):
        results.setdefault(k, {})
        results[k]["vhdx"] = vhdxfiles.get(k, None)
        results[k]["bstk"] = bstkfiles.get(k, None)
        results[k]["bstk_prev"] = bstk_prev_files.get(k, None)
        results[k]["already_created"] = already_created.get(k, False)
        results[k]["hdexecute"] = hdexecute.get(k, None)
        results[k]["startbat"] = startbatfiles.get(k, None)
        results[k]["bluestacksconfdata"] = bluestacksconfdata.get(k, [])
        results[k]["workingfolder"] = workingfolder.get(k, None)
        results[k]["adbport"] = adbports.get(k, None)
        results[k]["disableinternet"] = disableinternet.get(k, None)
        results[k]["enableinternet"] = enableinternet.get(k, None)
        results[k]["already_created_files"] = already_created_files.get(k, None)
        results[k]["ismasterinstance"] = ismasterinstance.get(k, False)
        results[k]["modify_xml_file_normal"] = modify_xml_file_normal.get(k, None)
        results[k]["modify_xml_file_read_only"] = modify_xml_file_read_only.get(k, None)
        results[k]["killcommand"] = ExecuteAsThreadedTask(
            fu=killstacks, args=(), kwargs={"vmm": vboxmanager_short, "machine": k}
        )
        results[k]["startcommand"] = ExecuteAsThreadedTask(
            fu=startstacks,
            args=(),
            kwargs={
                "command": [bsthdplayer, "--instance", k],
                "working_dir": workingfolder.get(k, None),
            },
        )
        results[k]["enable_root"] = ExecuteAsThreadedTask(
            fu=enable_root,
            args=(),
            kwargs={"bstconfigpath": bstconfigpath, "machine": k},
        )
        results[k]["disable_root"] = ExecuteAsThreadedTask(
            fu=disable_root,
            args=(),
            kwargs={"bstconfigpath": bstconfigpath, "machine": k},
        )
        results[k]["restart"] = ExecuteAsThreadedTask(
            fu=restartstacks,
            args=(),
            kwargs={
                "vmm": vboxmanager_short,
                "machine": k,
                "command": [bsthdplayer, "--instance", k],
                "working_dir": workingfolder.get(k, None),
            },
        )
        results[k]["get_external_ip"] = ExecuteAsThreadedTask(
            fu=adb_get_external_ip,
            args=(),
            kwargs={"adbport": adbports.get(k, None)},
        )
        results[k]["connections"] = []
    allp = get_information_from_all_procs_with_connections()
    allwins = get_window_infos()
    for k, v in allp.items():
        if v["Caption"] == "HD-Player.exe":
            cmdline = v["CommandLine"]
            instance = cmdline.split("--instance")[-1].strip("\" '")
            results[instance]["procdata"] = v
            adbport = "127.0.0.1:" + results[instance]["adbport"]
            results[instance]["connections"].extend(v["connections"])
            for w in allwins:
                if str(w.pid) == v["ProcessId"]:
                    results[instance].setdefault("window_handles", []).append(w)
                    if w.title.endswith("WindowOwnDCIcon"):
                        results[instance]["window_title"] = w.windowtext
                        results[instance]["window_hwnd"] = w.hwnd
                        results[instance]["window_functions"] = {
                            "hide": WinFu(
                                fu=window_HIDE, args=(), kwargs={"hwnd": w.hwnd}
                            ),
                            "normal": WinFu(
                                fu=window_NORMAL, args=(), kwargs={"hwnd": w.hwnd}
                            ),
                            "showminimized": WinFu(
                                fu=window_SHOWMINIMIZED,
                                args=(),
                                kwargs={"hwnd": w.hwnd},
                            ),
                            "maximize": WinFu(
                                fu=window_MAXIMIZE, args=(), kwargs={"hwnd": w.hwnd}
                            ),
                            "shownoactivate": WinFu(
                                fu=window_SHOWNOACTIVATE,
                                args=(),
                                kwargs={"hwnd": w.hwnd},
                            ),
                            "show": WinFu(
                                fu=window_SHOW, args=(), kwargs={"hwnd": w.hwnd}
                            ),
                            "minimize": WinFu(
                                fu=window_MINIMIZE, args=(), kwargs={"hwnd": w.hwnd}
                            ),
                            "showminnoactive": WinFu(
                                fu=window_SHOWMINNOACTIVE,
                                args=(),
                                kwargs={"hwnd": w.hwnd},
                            ),
                            "showna": WinFu(
                                fu=window_SHOWNA, args=(), kwargs={"hwnd": w.hwnd}
                            ),
                            "restore": WinFu(
                                fu=window_RESTORE, args=(), kwargs={"hwnd": w.hwnd}
                            ),
                            "showdefault": WinFu(
                                fu=window_SHOWDEFAULT, args=(), kwargs={"hwnd": w.hwnd}
                            ),
                            "forceminimize": WinFu(
                                fu=window_FORCEMINIMIZE,
                                args=(),
                                kwargs={"hwnd": w.hwnd},
                            ),
                            "resize_window": WinFu(
                                fu=resize_window,
                                args=(w.hwnd,),
                                kwargs={},
                            ),
                        }
                    if w.title.endswith("WindowToolSaveBitsOwnDC"):
                        results[instance]["keymap_dim"] = w.dim_client
                        results[instance]["keymap_hwnd"] = w.hwnd
            for con in v["connections"]:
                if con[1] == adbport:
                    break
            else:
                foundport = False
                for qra in range(5):
                    if foundport:
                        break
                    adbport1 = "127.0.0.1:" + str(int(results[instance]["adbport"]) + 1)
                    adbport2 = "127.0.0.1:" + str(int(results[instance]["adbport"]) - 1)
                    for con in v["connections"]:
                        if con[1] == adbport1:
                            results[instance]["adbport"] = adbport1.split(":")[-1]
                            foundport = True
                            break

                        elif con[1] == adbport2:
                            results[instance]["adbport"] = adbport2.split(":")[-1]
                            foundport = True
                            break
    return (
        data,
        bstconfigpath,
        bstconfigpath_folder,
        bstconfigpath_folder_short,
        bstconfigpath_short,
        results,
    )


def start_bluestacks_instance_and_connect_to_adb(
    adb_path, instancetostart, sleeptime, timeout
):
    (
        data,
        bstconfigpath,
        bstconfigpath_folder,
        bstconfigpath_folder_short,
        bstconfigpath_short,
        bluestacksinstances,
    ) = get_info_bluestacks()
    bluestacksinstances[instancetostart]["startcommand"]()
    time.sleep(sleeptime)
    adbexeshort = get_short_path_name_cached(adb_path)
    timeoutfinal = time.time() + timeout
    isconnected = False
    while timeoutfinal > time.time():
        try:
            (
                data,
                bstconfigpath,
                bstconfigpath_folder,
                bstconfigpath_folder_short,
                bstconfigpath_short,
                bluestacksinstances,
            ) = get_info_bluestacks()
            if not bluestacksinstances[instancetostart]["connections"]:
                time.sleep(sleeptime)
                continue
            if "window_title" not in bluestacksinstances[instancetostart]:
                time.sleep(sleeptime)
                continue
            addr = "127.0.0.1:" + str(bluestacksinstances[instancetostart]["adbport"])
            resultproc = subprocess.run(
                [
                    adbexeshort,
                    "connect",
                    addr,
                ],
                capture_output=True,
                **invisibledict,
            )

            if b"already" in resultproc.stdout or b"already" in resultproc.stderr:
                isconnected = True
                break

        except Exception as e:
            sys.stderr.write(f"{e}")
            sys.stderr.flush()
            time.sleep(sleeptime)
            continue
    return isconnected
