NO_SERVICES = 0

try:
    import win32service
    import win32serviceutil
    RUNNING = win32service.SERVICE_RUNNING
    STARTING = win32service.SERVICE_START_PENDING
    STOPPING = win32service.SERVICE_STOP_PENDING
    STOPPED = win32service.SERVICE_STOPPED

except ImportError:
    NO_SERVICES = 1

import win32process
import win32gui
import sys

class ServiceControl:
    def __init__(self, instance_home, software_home):
        self.instance_home = instance_home
        self.software_home = software_home

    def _svc_name(self):
        # Zope-2.7.2 will lower INSTANCE_HOME in zopeservice.py,
        # so we do
        return "Zope_" + str(hash(self.instance_home.lower()))

    def _isService(self):
        if not hasattr(self, "_service"):
            self._testService()
        return self._service

    def _testService(self):
        self._service = 0
        if not NO_SERVICES:
            try:
                # see if a service is installed
                win32serviceutil.QueryServiceStatus(self._svc_name())
                self._service = 1
            except win32service.error, msg:
                # error 1060 means no service installed
                if msg[0] != 1060:
                    raise

    def isRunning(self):
        if self._isService():
            stat = win32serviceutil.QueryServiceStatus(self._svc_name())[1]
            if stat in [RUNNING, STARTING]:
                return 1
            return 0
        return 0

    def start(self):
        if self._isService():
            win32serviceutil.StartService(self._svc_name(), None)

    def stop(self):
        if self._isService():
            win32serviceutil.StopService(self._svc_name())
