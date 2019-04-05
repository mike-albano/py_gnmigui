import py_gnmicli
import json
import time
from Tkinter import *
from Tkinter import W

class Application:
  def __init__(self, master):
    self.master = master
    master.title('gNMI GUI')
    self.mode = self.CreateRadioMode(master)
    self.getcerts = self.CreateRadioCerts(master)
    self.apnameentry = self.CreateApEntry(master)
    self.targetentry = self.CreateTargetEntry(master)
    self.username = self.CreateUserEntry(master)
    self.password = self.CreatePasswordEntry(master)
    self.hostoverride = self.CreateHostOverrideEntry(master)
    self.xpathentry = self.CreateXpathEntry(master)
    self.CreateQuitButton(master)
    self.CreateProvisionedButton(master)
    self.CreateRadiusButton(master)
    self.CreateClientCountButton(master)
    self.CreateXpathButton(master)
    self.label = Label(root, text='Easy Buttons:')
    self.label.grid(row=11, column=0, sticky=W)

  def CreateRadioCerts(self, master):
    var = StringVar()
    button1 = Radiobutton(master, text='Use Internal Certs', variable=var,
                          value='InternalCert').grid(row=0, column=1)
    button2 = Radiobutton(master, text='Get Cert', variable=var,
                          value='DLCert').grid(row=0)
    var.set('InternalCert') # Default
    return var

  def CreateMessage(self, text, color):
    """Text box to hold results."""
    self.label = Label(root, text='Ctrl-/ to select all')
    self.label.grid(row=1, column=2)
    S = Scrollbar(root)
    T = Text(root, height=25, width=50, fg=color)
    S.grid(row=0, column=2)
    T.grid(row=0, column=2)
    S.config(command=T.yview)
    T.config(yscrollcommand=S.set)
    T.insert(END, text)

  def CreateTargetEntry(self, master):
    """Create text boxes for user input."""
    var = StringVar()
    self.label = Label(master, text='gNMI Target:')
    self.label.grid(row=1, columnspan=1, sticky=W)
    ap_name = Entry(master, width=20, textvariable=var)
    ap_name.grid(row=1, column=1)
    ap_name.delete(0, END)
    ap_name.focus_set()
    var.set('openconfig.mist.com:443')
    return var

  def CreateApEntry(self, master):
    """Create text boxes for user input."""
    var = StringVar()
    self.label = Label(master, text='AP Hostname:')
    self.label.grid(row=2, columnspan=1, sticky=W)
    ap_name = Entry(master, width=20, textvariable=var)
    ap_name.grid(row=2, column=1)
    ap_name.delete(0, END)
    return var

  def CreateUserEntry(self, master):
    """Create text boxes for user input."""
    var = StringVar()
    self.label = Label(master, text='Username:')
    self.label.grid(row=3, columnspan=1, sticky=W)
    username = Entry(master, width=10, textvariable=var)
    username.grid(row=3, column=1, sticky=W)
    username.delete(0, END)
    return var

  def CreatePasswordEntry(self, master):
    """Create text boxes for user input."""
    var = StringVar()
    self.label = Label(master, text='Password:')
    self.label.grid(row=4, columnspan=1, sticky=W)
    password = Entry(master, width=10, textvariable=var)
    password.grid(row=4, column=1, sticky=W)
    password.delete(0, END)
    return var

  def CreateHostOverrideEntry(self, master):
    """Create text boxes for user input."""
    var = StringVar()
    self.label = Label(master, text='[Optional] Host Override:')
    self.label.grid(row=5, columnspan=1, sticky=W)
    password = Entry(master, width=10, textvariable=var)
    password.grid(row=5, column=1, sticky=W)
    password.delete(0, END)
    return var

  def CreateXpathEntry(self, master):
    """Create text boxes for user input."""
    var = StringVar()
    self.label = Label(master, text='[Optional] xpath:')
    self.label.grid(row=6, columnspan=1, sticky=W)
    xpath = Entry(master, width=10, textvariable=var)
    xpath.grid(row=6, column=1, sticky=W)
    xpath.delete(0, END)
    return var

  def CreateProvisionedButton(self, master):
    """Creates button to get provisioned APs container."""
    self.PROVISIONEDAPS = Button(master, text='Provisioned APs',
                                 command=self.GetProvisioned)
    self.PROVISIONEDAPS["fg"] = "blue"
    self.PROVISIONEDAPS.grid(row=12, column=0, sticky=W)

  def CreateRadiusButton(self, master):
    """Creates button to get RADIUS counters."""
    self.RADIUSCOUNT = Button(master, text='RADIUS Counters',
                                 command=self.GetRadiusCounters)
    self.RADIUSCOUNT["fg"] = "blue"
    self.RADIUSCOUNT.grid(row=13, column=0, sticky=W)

  def CreateClientCountButton(self, master):
    """Creates button to get Client counts."""
    self.CLIENTCOUNT = Button(master, text='Client Counts',
                                 command=self.GetClientCounts)
    self.CLIENTCOUNT["fg"] = "blue"
    self.CLIENTCOUNT.grid(row=14, column=0, sticky=W)

  def CreateRadioMode(self, master):
    var = StringVar()
    button1 = Radiobutton(master, text='Get Once', variable=var,
                          value='GetOnce').grid(row=9)
    button2 = Radiobutton(master, text='Get Continuous', variable=var,
                          value='GetContinuous').grid(row=9, column=1)
    var.set('GetOnce') # Default
    return var

  def CreateXpathButton(self, master):
    """Creates button to parse full xpath."""
    self.XPATH = Button(master, text="Get Xpath", command=self.GetXpath)
    self.XPATH["fg"] = "red"
    self.XPATH.grid(row=6, column=1, sticky=E)

  def CreateQuitButton(self, master):
    """Creates button to exit program."""
    self.QUIT = Button(master, text="Quit", command=master.quit)
    self.QUIT["fg"] = "red"
    self.QUIT.grid(row=12, column=1)

  def GetProvisioned(self):
    """Gets provisioned-aps container."""
    if self.mode.get() == 'GetOnce':
      response = self.GnmiGet(self.targetentry.get(), '/provision-aps/')
      self.CreateMessage(json.dumps(json.loads(
        response.notification[0].update[0].val.json_ietf_val), indent=2),
                         'black')
    else:
      global xpath
      global targetentry
      xpath = '/provision-aps/'
      targetentry = self.targetentry.get()
      self.GnmiGetContinuous()

  def GetXpath(self):
    """Gets full xpath provided."""
    if self.mode.get() == 'GetOnce':
      response = self.GnmiGet(self.targetentry.get(), self.xpathentry.get())
      self.CreateMessage(json.dumps(json.loads(
        response.notification[0].update[0].val.json_ietf_val), indent=2),
                         'black')
    else:
      global xpath
      global targetentry
      xpath = self.xpathentry.get()
      targetentry = self.targetentry.get()
      self.GnmiGetContinuous()


  def GetRadiusCounters(self):
    """Gets RADIUS counters."""
    if self.apnameentry.get() == '':
      self.CreateMessage('Please specify a Hostname.', 'red')
    if self.mode.get() == 'GetOnce':
      response = self.GnmiGet(
        self.targetentry.get(),
        '/access-points/access-point[hostname=%s]/system/aaa/server-groups/' % self.apnameentry.get())
      self.CreateMessage(json.dumps(json.loads(
          response.notification[0].update[0].val.json_ietf_val)
                                    ['openconfig-access-points:server-group']
                                    [0]['servers']['server'][0]['radius']
                                    ['state']['counters'], indent=2), 'black')

    else:
      global xpath
      global targetentry
      xpath = (
        '/access-points/access-point[hostname=%s]/system/aaa/server-groups/'
        % self.apnameentry.get())
      targetentry = self.targetentry.get()
      self.GnmiGetContinuousRadius()

  def GetClientCounts(self):
      """Gets Client counts, per SSID."""
      if self.apnameentry.get() == '':
        self.CreateMessage('Please specify a Hostname.', 'red')
      if self.mode.get() == 'GetOnce':
        clients = {}
        response = self.GnmiGet(
          self.targetentry.get(),
          '/access-points/access-point[hostname=%s]/ssids/' % self.apnameentry.get())
        for ssid in json.loads(
          response.notification[0].update[0].val.json_ietf_val)['openconfig-access-points:ssid']:
          client_count = 0
          for client in ssid['bssids']['bssid']:
            client_count += client['state']['num-associated-clients']
          clients[ssid['name']] = client_count
          client_count = 0 # Reset count back to 0
        self.CreateMessage(json.dumps(clients, indent=2), 'black')
      else:
        global xpath
        global targetentry
        xpath = (
          '/access-points/access-point[hostname=%s]/ssids/'
          % self.apnameentry.get())
        targetentry = self.targetentry.get()
        self.GnmiGetContinuousClients()

  def GnmiGet(self, targetentry, xpath):
   if targetentry == '':
     self.CreateMessage('Please specify a gNMI Target:port.', 'red')
   else:
    if self.getcerts.get() == 'InternalCert':
      get_cert = False
      certs = {'root_cert': None, 'private_key': None, 'cert_chain': None}
    else:
      get_cert = True
    host_override = self.hostoverride.get() if self.hostoverride.get() != '' else False
    creds = py_gnmicli._build_creds(targetentry.split(':')[0],
                                    targetentry.split(':')[1],
                                    get_cert, certs, None)
    stub = py_gnmicli._create_stub(creds, targetentry.split(':')[0],
                        targetentry.split(':')[1], host_override)
    paths = py_gnmicli._parse_path(py_gnmicli._path_names(xpath))
    return py_gnmicli._get(stub, paths, self.username.get(), self.password.get())

  def GnmiGetContinuous(self):
    if targetentry == '':
      self.CreateMessage('Please specify a gNMI Target:port.', 'red')
    if self.getcerts.get() == 'InternalCert':
      get_cert = False
      certs = {'root_cert': None, 'private_key': None, 'cert_chain': None}
    else:
      get_cert = True
    host_override = self.hostoverride.get() if self.hostoverride.get() != '' else False
    creds = py_gnmicli._build_creds(targetentry.split(':')[0],
                                    targetentry.split(':')[1],
                                    get_cert, certs, None)
    stub = py_gnmicli._create_stub(creds, targetentry.split(':')[0],
                        targetentry.split(':')[1], host_override)
    paths = py_gnmicli._parse_path(py_gnmicli._path_names(xpath))
    response = py_gnmicli._get(stub, paths, self.username.get(),
                                 self.password.get())
    self.CreateMessage(json.dumps(json.loads(
        response.notification[0].update[0].val.json_ietf_val), indent=2),
                       'black')
    self.master.after(5000, self.GnmiGetContinuous)

  def GnmiGetContinuousRadius(self):
    """Prints only certain keys."""
    if targetentry == '':
      self.CreateMessage('Please specify a gNMI Target:port.', 'red')
    if self.getcerts.get() == 'InternalCert':
      get_cert = False
      certs = {'root_cert': None, 'private_key': None, 'cert_chain': None}
    else:
      get_cert = True
    host_override = self.hostoverride.get() if self.hostoverride.get() != '' else False
    creds = py_gnmicli._build_creds(targetentry.split(':')[0],
                                    targetentry.split(':')[1],
                                    get_cert, certs, None)
    stub = py_gnmicli._create_stub(creds, targetentry.split(':')[0],
                        targetentry.split(':')[1], host_override)
    paths = py_gnmicli._parse_path(py_gnmicli._path_names(xpath))
    response = py_gnmicli._get(stub, paths, self.username.get(),
                                 self.password.get())
    self.CreateMessage(json.dumps(json.loads(
        response.notification[0].update[0].val.json_ietf_val)
                                  ['openconfig-access-points:server-group']
                                  [0]['servers']['server'][0]['radius']
                                  ['state']['counters'], indent=2), 'black')
    self.master.after(5000, self.GnmiGetContinuousRadius)

  def GnmiGetContinuousClients(self):
    """Prints only certain keys."""
    if targetentry == '':
      self.CreateMessage('Please specify a gNMI Target:port.', 'red')
    if self.getcerts.get() == 'InternalCert':
      get_cert = False
      certs = {'root_cert': None, 'private_key': None, 'cert_chain': None}
    else:
      get_cert = True
    host_override = self.hostoverride.get() if self.hostoverride.get() != '' else False
    creds = py_gnmicli._build_creds(targetentry.split(':')[0],
                                    targetentry.split(':')[1],
                                    get_cert, certs, None)
    stub = py_gnmicli._create_stub(creds, targetentry.split(':')[0],
                        targetentry.split(':')[1], host_override)
    paths = py_gnmicli._parse_path(py_gnmicli._path_names(xpath))
    clients = {}
    response = py_gnmicli._get(stub, paths, self.username.get(),
                                 self.password.get())
    for ssid in json.loads(
      response.notification[0].update[0].val.json_ietf_val)['openconfig-access-points:ssid']:
      client_count = 0
      for client in ssid['bssids']['bssid']:
        client_count += client['state']['num-associated-clients']
      clients[ssid['name']] = client_count
      client_count = 0 # Reset count back to 0
    self.CreateMessage(json.dumps(clients, indent=2), 'black')
    self.master.after(5000, self.GnmiGetContinuousClients)


if __name__ == '__main__':
  root = Tk()
  app = Application(root)
  root.mainloop()
  root.destroy()
