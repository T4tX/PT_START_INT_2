import paramiko
import db_init

commands_linux = {'Command History':'cat ~/.bash_history',
                  'Linux ver':'cat /etc/*-release',
                  'OS info':'uname -a',
                  'Arch':'uname -m'
                }

class linux_comp:
    def __init__(self,com_hist="",os_info='Default_linux',arch='x64', name="Linux", pretty_name="Linux OS", version="1.0", version_id="1.0", version_codename="Stable", id_like="linux", home_url="https://www.linux.org", support_url="https://www.linux.org/support", bug_report_url="https://www.linux.org/bugs"):
        self.com_hist = com_hist
        self.os_info = os_info
        self.arch = arch
        self.name = name
        self.pretty_name = pretty_name
        self.version = version
        self.version_id = version_id
        self.version_codename = version_codename
        self.id_like = id_like
        self.home_url = home_url
        self.support_url = support_url
        self.bug_report_url = bug_report_url
    def display_info(self):
        print("Command History:", self.com_hist)
        print("OS info:", self.os_info)
        print("Arch:", self.arch)
        print("Pretty Name:", self.pretty_name)
        print("Version:", self.version)
        print("Version ID:", self.version_id)
        print("Version Codename:", self.version_codename)
        print("ID Like:", self.id_like)
        print("Home URL:", self.home_url)
        print("Support URL:", self.support_url)
        print("Bug Report URL:", self.bug_report_url)
    def get_info(self): 
        info_dict = { "Command History": self.com_hist, "OS info": self.os_info, "Arch": self.arch, "Pretty Name": self.pretty_name, "Version": self.version, "Version ID": self.version_id, "Version Codename": self.version_codename, "ID Like": self.id_like, "Home URL": self.home_url, "Support URL": self.support_url, "Bug Report URL": self.bug_report_url, } 
        return info_dict
    def db_write(self):
        conn = db_init.connect_to_postgres()
        db_init.drop_table(conn)
        db_init.create_table(conn)
        db_init.read_data(conn)
        print(10)
        db_init.insert_data(conn,[str(self.com_hist), str(self.os_info), 
                                str(self.arch), str(self.name), 
                                str(self.pretty_name), str(self.version),
                                str(self.version_id), str(self.version_codename), 
                                str(self.id_like), str(self.home_url), 
                                str(self.support_url), str(self.bug_report_url)])
def list_to_dict(lst):

    result = {}
    for item in lst:
        key_value = item.split("=")
        key = key_value[0]
        value = "=".join(key_value[1:])
        result[key] = value
    return result

def parse_lin(hostname='192.168.86.93', username='osboxes', password='osboxes.org', PORT=22):
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username, password=password, port=PORT)

        with ssh:
            parsed_output = {}
            for name,command in commands_linux.items():
                stdin, stdout, stderr = ssh.exec_command(command)
                output = stdout.read().decode().split('\n')

                if name == 'Linux ver':
                    parsed_output.update(list_to_dict(output))
  

                else:

                    parsed_output.update({f'{name}':output[0]})
            output = linux_comp(com_hist=parsed_output["Command History"],os_info=parsed_output["OS info"],arch=parsed_output["Arch"],
                        name=parsed_output["NAME"],
                        pretty_name=parsed_output["PRETTY_NAME"],
                        version=parsed_output["VERSION"],
                        version_id=parsed_output["VERSION_ID"],
                        version_codename=parsed_output["VERSION_CODENAME"],
                        id_like=parsed_output["ID_LIKE"],
                        home_url=parsed_output["HOME_URL"],
                        support_url=parsed_output["SUPPORT_URL"],
                        bug_report_url=parsed_output["BUG_REPORT_URL"]
                    )
            output.display_info()
            output.db_write()
            return output

    except paramiko.AuthenticationException:
        print("Ошибка аутентификации. Проверьте учетные данные.")
    except paramiko.SSHException as e:
        print(f"Ошибка SSH: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        ssh.close()

if __name__ == '__main__':
    PORT = 22
    hostname = '192.168.86.93'
    username = 'osboxes'
    password = 'osboxes.org'
    print(parse_lin(username=username,password=password,hostname=hostname,PORT=PORT))