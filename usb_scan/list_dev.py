from __future__ import print_function
import sys
import usb1

"""
iterate through usb devices that libusb can see
try to get information from selected device
    ex: TI ICDI device is 1cbe 00fd 
or if none specified, print all devices.
try to open device, if device cant be opened print "could not open.."
"""		
def list_test(vendID = 0, prodID = 0, printAll = False):
    context = usb1.USBContext()
    device_list = context.getDeviceList(skip_on_error=True)
    #1 if user supplied VID/PID tell libusb to search for device by vid/pid and try to open it
    if(vendID != 0):
        find_by_pid_vid_unit_test(context,vendID,prodID)
    for device in device_list:
	    thisPID = device.getProductID()
	    thisVID = device.getVendorID()
	    if( thisVID == vendID and thisPID == prodID):
		    print_dev(device)		
	    elif(printAll == True):
		    print_dev(device)			
	
def print_dev(device):
    #2 read device info
    device_info_unit_test(device)
    #3 try to open device and read additional info
    open_device_unit_test(device)
    #4 check what information we can get about the device
    device_interface_unit_test(device)
    #5 try to claim interfaces on the device
    claim_device_unit_test(device)



#1 test if libusb can find the device. libusb will search for the first instance of a device with PID, VID and attempt to open it
# libusb will return device open, or could not open device
def find_by_pid_vid_unit_test(context,thisVID, thisPID):
    dev = context.getByVendorIDAndProductID(thisVID, thisPID)
    if dev is None:		
        print ('\ncould not find by VID, PID')	
    else:
        print ('\ndevice found by VID PID')
        open_device_unit_test(dev)

#2 passive command to read device info				
def device_info_unit_test(device):	
    print (device.__str__())
    
#3 open device and get more info. if this fails, libusb can see the device but cant talk to it	
def open_device_unit_test(device):
    try:
	    serial = device.getSerialNumber()
	    print ('  serial:', serial)
	    print ('  MF:', device.getManufacturer())
	    print ('  product:', device.getProduct())				
    except:
	    print ('  Could not Open Device %x:%x' %(device.getVendorID(), device.getProductID()))

#4 test retrieving addition information of device
def device_interface_unit_test(device):
    nbInterface = 0
    for configuration in device.iterConfigurations():
	    nbInterface = configuration.getNumInterfaces()
	    print ('\n  nb interfaces:', nbInterface)
	    for interface in configuration:
		    for settings in interface:
			    print ('    interface:', settings.getNumber())
			    print ('      num endpoints:', settings.getNumEndpoints())
			    print ('      class.subclass.protocol: %x.%x.%x' %(settings.getClass(), settings.getSubClass(), settings.getProtocol()))						
			    for endpoint in settings:
				    print ('\tendpoint address: %x' %(endpoint.getAddress()))
				    print ('\tmax packet size: %x' %endpoint.getMaxPacketSize())
				    print ('\tpolling interval: %d' %endpoint.getInterval())
				    #found = True

#5 try to claim each interface on device, if device cant be opened, it cant be claimed					
def claim_device_unit_test(device):
    #print ('  number of configuration:'), device.getNumConfigurations()
    #print ('  len of configuration:'), device.__len__()
    #print ('  number of interfaces:'), device.__getitem__(0).getNumInterfaces()
    nbInterface = 0
    try:
	    nbInterface = device.__getitem__(0).getNumInterfaces()
    except:
	    pass
    print ('\nattempting to claim interfaces on device')
    for j in range(0,nbInterface):
	    try:
		    device.open().claimInterface(j)
		    print ('interface %d claimed' %j)
	    except:
		    print ('could not claim: ', j)
    print("")

def main():
    #try:
    if (len(sys.argv) == 3): 
	    print (sys.argv[1],sys.argv[2])
	    list_test(int(sys.argv[1],16),int(sys.argv[2],16))	
    else:
	    print ('all devices')
	    list_test(0,0,True)	

if __name__ == '__main__':
    main()

