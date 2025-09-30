from dataclasses import dataclass
import re
import os
from subprocess import Popen, PIPE
import shlex
import sys
from color import Color as clr


def path_replace(path, obj, val_source, search_for_keys: list[str], regex: str) -> str:
    for key in search_for_keys:
        rgx = re.compile(regex, 0)
        for item in rgx.findall(path):
            if item in [f"${key}", f"<{key}>"]:
                path = path.replace(item, val_source[key])
    return path
    


def run_command(command) -> int:
        args = shlex.split(command)
        subp = Popen(args, stdout=PIPE, stderr=PIPE)
        subp.communicate()
        return subp.returncode



@dataclass
class Device:
    label: str
    addr: str
    port: int
    user: str
    id_file: str
    mnt_from: str = None
    mnt_to: str = None
    name: str = None
    
    
    
    def __init__(self, 
        label=None, 
        addr=None, 
        port=None, 
        user=None, 
        id_file=None,
        mount=None,
        name=None,
    ):
        self.label = label
        self.addr = addr
        self.port = port
        self.user = None if len(user) <= 0 else user
        self.id_file = id_file
        
        sys_placeholder = r"(\$[\d\w]+)"
        config_placeholder = r"(\<[\d\w]+\>)"
        
        sys_search_for = ["USER", "HOME", "PWD"]
        config_search_for = ["label"]
        
        mnt_from = mount[0]
        mnt_to = mount[1]
        
        id_file = path_replace(id_file, self,
            os.environ,
            sys_search_for,
            sys_placeholder
        )
        
        id_file = path_replace(id_file, self,
            self.__dict__,
            config_search_for,
            config_placeholder
        )
        
        mnt_from = path_replace(mnt_from, self,
            os.environ,
            sys_search_for,
            sys_placeholder
        )
            
        mnt_to = path_replace(mnt_to, self,
            os.environ,
            sys_search_for,
            sys_placeholder
        )
        
        mnt_from = path_replace(mnt_from, self,
            self.__dict__,
            config_search_for,
            config_placeholder
        )
            
        mnt_to = path_replace(mnt_to, self,
            self.__dict__,
            config_search_for,
            config_placeholder
        )
        
        self.id_file = id_file
        self.mnt_from = mnt_from
        self.mnt_to = mnt_to
        self.name = name
    
    
    def mount_fs(self, return_bool: bool=False) -> [int|bool]:
        if os.path.isdir(self.mnt_to):
            print(f"Directory '{self.mnt_to}' exists.")
            return False
            
        if self.user is None:
            login = f"{self.addr}"
        else:
            login = f"{self.user}@{self.addr}"
            
        mk_command = f"""mkdir -p '{self.mnt_to}'"""
        sshfs_command = f"""sshfs -o allow_other,default_permissions """ \
                        f"""-o Port={self.port} """ \
                        f"""-o IdentityFile='{self.id_file}' """ \
                        f"""'{login}:{self.mnt_from}' """ \
                        f"""'{self.mnt_to}' """

        print(f"Mounting {self.addr}:{self.mnt_from} -> {self.mnt_to}")
        mk_rc = run_command(mk_command)
        sshfs_rc = run_command(sshfs_command)
        
        if sshfs_rc == 1:
            del_command = f"rm -rf '{self.mnt_to}'"
            run_command(del_command)

        if return_bool:
            return True if sshfs_rc == 0 else False
        else:
            return sshfs_rc

        
    def unmount_fs(self) -> None:
        print(f"Unmounting {self.addr}:{self.mnt_from} from {self.mnt_to}")
        unmount_command = f"umount '{self.mnt_to}'"
        run_command(unmount_command)
        del_command = f"rm -rf '{self.mnt_to}'"
        run_command(del_command)
        
    
    def is_accessible(self) -> int:
        if self.user is None:
            login = f"{self.addr}"
        else:
            login = f"{self.user}@{self.addr}"
            
        ssh_command = f"ssh -o ConnectTimeout=3 '{login}' " \
                      f"-p '{self.port}' -i '{self.id_file}' << ls "
        return_code = run_command(ssh_command)
        return return_code
