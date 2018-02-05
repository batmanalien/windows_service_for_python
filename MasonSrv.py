import sys
import win32api
import win32event
import win32service
import servicemanager
import win32serviceutil


class MasonSrv(win32serviceutil.ServiceFramework):
    _svc_name_ = 'MasonSrv'
    _svc_display_name_ = 'Mason.ME Service'
    _svc_description_ = 'Enables you to say hello world...'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def log(self, msg):
        servicemanager.LogInfoMsg(str(msg))

    def sleep(self, sec):
        win32api.Sleep(sec * 1000, True)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.log('stopping')
        self.my_stop()
        self.log('stopped')
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):

        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.log('start')
            self.my_start()
            self.log('wait')
            win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
            self.log('done')
        except Exception as x:
            self.log('Exception : %s' % x)
            self.SvcStop()

    # to be overridden
    def my_start(self):
        self.runflag = True
        while self.runflag:
            self.sleep(5)
            self.log("Hello World! I'm alive ...")

    # to be overridden

    def my_stop(self):
        self.runflag = False
        self.log("I'm done")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MasonSrv)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MasonSrv)
