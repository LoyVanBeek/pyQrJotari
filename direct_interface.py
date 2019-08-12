import zbar


class ZBarInterface(object):
    def __init__(self, device='/dev/video0', callback=None):
        self.callback = callback
        self.proc = zbar.Processor()
        # configure the Processor
        self.proc.parse_config('enable')
        self.device = device
        
    def start(self):
        self.proc.init(self.device)
        self.proc.set_data_handler(self.zbar_cb)
        self.proc.active = True
        # # enable the preview window
        # self.proc.visible = True

    # setup a callback
    def zbar_cb(self, proc, image, closure):
        # type: (zbar.Processor, zbar.Image, None) -> None
        # extract results

        for symbol in image.symbols:
            # do something useful with results
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
            out = symbol.data.replace("http://www.scoutingboxtel.nl/qr.asp?groep=", "")
            print out
            if self.callback:
                try:
                    self.callback(out, image=image)
                except Exception as e:
                    print e

    def force_stop(self):
        pass
    
    def wait_stop(self):
        try:
            # keep scanning until user provides key/mouse input
            self.proc.user_wait()
        except zbar.WindowClosed, e:
            pass
        
    def run(self):
        while self.process.poll() == None:
            try:
                out = self.process.stdout.readline()
                if "QR-Code:" in out:
                    out = out.strip("QR-Code:")
                    #For this year, the QR-codes encode an URL. We have some old codes as wel, so strip this all out:
                    out = out.replace("http://www.scoutingboxtel.nl/qr.asp?groep=", "")
                    print out
                    if self.callback:
                        try:
                            self.callback(out)
                        except Exception as e:
                            print e
            except Exception, e:
                print "Trying to read did not work: ", e
                self.wait_stop()
                break
        else:
            print "ZBar exited with exitcode {0}".format(self.process.returncode)
            self.wait_stop()

def dummy_callback(data):
    print "CB: ",data.capitalize()

def main2():
    zbar = ZBarInterface(callback=dummy_callback)
    zbar.start()
    
    '''
    while True:
        try:
            pass
        except KeyboardInterrupt:
            break
    zbar.stop()
    '''
    zbar.wait_stop()

if __name__ == "__main__":
    main2()
