# Some useful Bluestacks stuff

## pip install getbstacksinfo

### Tested against Windows 10 / Python 3.11 / Anaconda / BlueStacks

```PY
from getbstacksinfo import (
    start_bluestacks_instance_and_connect_to_adb,
    get_info_bluestacks,
    kill_all_bluestacks_exe,
)
from pprint import pprint

adb_path = r"C:\ProgramData\chocolatey\lib\adb\tools\platform-tools\adb.exe"

kill_any_bluestacks = False
if kill_any_bluestacks:
    kill_all_bluestacks_exe()

# start an instance and wait for it to connect
# Use with: https://github.com/hansalemaos/adbkonnekt
connect_adb = False
if connect_adb:
    instancetostart = "Rvc64_34"

    worked = start_bluestacks_instance_and_connect_to_adb(
        adb_path, instancetostart, sleeptime=5, timeout=120
    )
    print(worked)

(
    data,
    bstconfigpath,
    bstconfigpath_folder,
    bstconfigpath_folder_short,
    bstconfigpath_short,
    bluestacksinstances,
) = get_info_bluestacks()
pprint(bluestacksinstances)
# each bluestacks instance is a dict in bluestacksinstances
# if the instance has already started, there are more functions available
r""" 'Rvc64_39': {'adbport': '5945',
              'already_created': False,
              'already_created_files': 'C:\\ProgramData\\BlueStacks_nxt\\Engine\\Rvc64_39\\iscreated.txt', # a file to save some random data
              'bluestacksconfdata': ['bst.instance.Rvc64_39.abi_list="x86,x64,arm,arm64"', # data from bluestacks.conf
                                     'bst.instance.Rvc64_39.adb_port="5945"',
                                     'bst.instance.Rvc64_39.ads_display_time=""',
                                     ...
                                     'bst.instance.Rvc64_39.status.session_id="1"',
                                     'bst.instance.Rvc64_39.vulkan_supported="0"'],
              'bstk': files(folder='C:\\ProgramData\\BlueStacks_nxt\\Engine\\Rvc64_39', file='Rvc64_39.bstk', path='C:\\ProgramData\\BlueStacks_nxt\\Engine\\Rvc64_39\\Rvc64_39.bstk', ext='.bstk'),
              'bstk_prev': files(folder='C:\\ProgramData\\BlueStacks_nxt\\Engine\\Rvc64_39', file='Rvc64_39.bstk-prev', path='C:\\ProgramData\\BlueStacks_nxt\\Engine\\Rvc64_39\\Rvc64_39.bstk-prev', ext='.bstk-prev'),
              'connections': [['TCP',
                               '127.0.0.1:5945',
                               '0.0.0.0:0',
                               'LISTENING',
                               '15148'],
                              ['TCP',
                               '127.0.0.1:5945',
                               '127.0.0.1:52404',
                               'ESTABLISHED',
                               '15148'],
                              ['UDP', '0.0.0.0:53193', '*:*', '15148'],
                              ['UDP', '[::]:53193', '*:*', '15148']],
              'disable_root': {'exception': [], 'returnvalue': [], 'running': [False]}, # a callable class that disables root in bluestacks.conf
              'disableinternet': 'C:\\PROGRA~1\\BLUEST~2\\BSTKVM~1.EXE '
                                 'controlvm Rvc64_39 setlinkstate1 off', # command line to disable network (adb won't work anymore)
              'enable_root': {'exception': [], 'returnvalue': [], 'running': [False]},  # a callable class that enables root in bluestacks.conf
              'enableinternet': 'C:\\PROGRA~1\\BLUEST~2\\BSTKVM~1.EXE ' # command line to disable network
                                'controlvm Rvc64_39 setlinkstate1 on',
              'get_external_ip': {'exception': [], 'returnvalue': [], 'running': [False]}, # a callable class that gets the external ip
              'hdexecute': 'start /min "" C:\\PROGRA~1\\BLUEST~2\\HD-PLA~1.EXE '
                           '--instance Rvc64_39', # command line to start hdplayer detached
              'ismasterinstance': False, # if the instance is the master instance
              'keymap_dim': (571, 1016), # size of the keymap window
              'keymap_hwnd': 10555144, # handle of the keymap window
              'killcommand': {'exception': [], 'returnvalue': [], 'running': [False]}, # a callable class that kills the bluestacks instance
              'modify_xml_file_normal': None, # a callable class that modifies the hdds in the xml file to normal (only available if ismasterinstance is True)
              'modify_xml_file_read_only': None, # a callable class that modifies the hdds in the xml file to read only (only available if ismasterinstance is True)
              'procdata': {'Caption': 'HD-Player.exe',
                           'CommandLine': 'C:\\PROGRA~1\\BLUEST~2\\HD-PLA~1.EXE  '
                                          '--instance Rvc64_39',
                           'CreationDate': '20240318112659.149708-180',
                           'ExecutablePath': 'C:\\PROGRA~1\\BLUEST~2\\HD-Player.exe',
                           'KernelModeTime': '18340468750',
                           'ParentProcessId': '15816',
                           'ProcessId': '15148',
                           'ThreadCount': '147',
                           'UserModeTime': '9621562500',
                           'VirtualSize': '10083291136',
                           'WorkingSetSize': '97685504',
                           'connections': [['TCP',
                                            '127.0.0.1:5945',
                                            '0.0.0.0:0',
                                            'LISTENING',
                                            '15148'],
                                           ['TCP',
                                            '127.0.0.1:5945',
                                            '127.0.0.1:52404',
                                            'ESTABLISHED',
                                            '15148'],
                                           ['UDP',
                                            '0.0.0.0:53193',
                                            '*:*',
                                            '15148'],
                                           ['UDP',
                                            '[::]:53193',
                                            '*:*',
                                            '15148']]},
              'restart': {'exception': [], 'returnvalue': [], 'running': [False]}, # a callable class that restarts the bluestacks instance
              'startbat': 'C:\\ProgramData\\BlueStacks_nxt\\Engine\\Rvc64_39\\instancestart.bat', # path to a bat file that starts the bluestacks instance
              'startcommand': {'exception': [], 'returnvalue': [], 'running': [False]}, # a callable class that starts the bluestacks instance
              'vhdx': files(folder='C:\\ProgramData\\BlueStacks_nxt\\Engine\\Rvc64_39', file='Data.vhdx', path='C:\\ProgramData\\BlueStacks_nxt\\Engine\\Rvc64_39\\Data.vhdx', ext='.vhdx'),
              'window_functions': {'forceminimize': <getbstacksinfo.WinFu object at 0x000001FEB6D6AE90>, # some functions for the bluestacks window
                                   'hide': <getbstacksinfo.WinFu object at 0x000001FEB6D6A990>,
                                   'maximize': <getbstacksinfo.WinFu object at 0x000001FEB6D6AA90>,
                                   'minimize': <getbstacksinfo.WinFu object at 0x000001FEB6D6AC10>, 
                                   'normal': <getbstacksinfo.WinFu object at 0x000001FEB6D6A9D0>,
                                   'resize_window': <getbstacksinfo.WinFu object at 0x000001FEB6D6AF10>, # use position=(x, y, w, h)
                                   'restore': <getbstacksinfo.WinFu object at 0x000001FEB6D6AD90>,
                                   'show': <getbstacksinfo.WinFu object at 0x000001FEB6D6AB90>,
                                   'showdefault': <getbstacksinfo.WinFu object at 0x000001FEB6D6AE10>,
                                   'showminimized': <getbstacksinfo.WinFu object at 0x000001FEB6D6AA10>,
                                   'showminnoactive': <getbstacksinfo.WinFu object at 0x000001FEB6D6AC90>,
                                   'showna': <getbstacksinfo.WinFu object at 0x000001FEB6D6AD10>,
                                   'shownoactivate': <getbstacksinfo.WinFu object at 0x000001FEB6D6AB10>},
              'window_handles': [WindowInfo(pid=15148, title='Qt5154QWindowToolSaveBitsOwnDC', windowtext='BlueStacks Keymap Overlay', hwnd=10555144, length=26, tid=24768, status='visible', coords_client=(0, 571, 0, 1016), dim_client=(571, 1016), coords_win=(304, 875, 33, 1049), dim_win=(571, 1016), class_name='Qt5154QWindowToolSaveBitsOwnDC', path='C:\\PROGRA~1\\BLUEST~2\\HD-Player.exe'),
                                 ...
                                 WindowInfo(pid=15148, title='temp_d3d_window_4039785', windowtext='Temp Window', hwnd=3605532, length=12, tid=26584, status='invisible', coords_client=(0, 1, 0, 1), dim_client=(1, 1), coords_win=(0, 1, 0, 1), dim_win=(1, 1), class_name='temp_d3d_window_4039785', path='C:\\PROGRA~1\\BLUEST~2\\HD-Player.exe')],
              'window_hwnd': 4198756,
              'window_title': 'BlueStacks App Player 39',
              'workingfolder': 'C:\\PROGRA~3\\BLUEST~2\\Engine\\Rvc64_39'}}"""

```