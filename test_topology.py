#!/usr/bin/python

from mininet.topo import Topo

from mininet.cli import CLI
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

from mininet.node import RemoteController

# Traffic Control
from mininet.link import TCLink

REMOTE_CONTROLLER_IP = "172.21.22.1"


def simpleTest():
    # Create and test a simple network
    topo = SingleSwitchTopo(n=4)

    net = Mininet(topo=topo, controller=RemoteController, autoStaticArp=True)
    net.addController("c0", controller=RemoteController,
                      ip=REMOTE_CONTROLLER_IP, port=6633)

    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    net.pingAll()
    net.stop()


def perfTest():
    # Create network and run simple performance test
    topo = SingleSwitchTopo(n=4)

    net = Mininet(topo=topo, link=TCLink,
                  controller=RemoteController,
                  autoStaticArp=True)
    net.addController("c0",
                      controller=RemoteController,
                      ip=REMOTE_CONTROLLER_IP,
                      port=6633)

    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    # net.pingAll()
    print("Testing bandwidth between h1 and h4")
    h1, h4 = net.get('h1', 'h4')
    net.iperf((h1, h4), l4Type='UDP')
    net.stop()


class SingleSwitchTopo(Topo):
    # Single switch connected to n hosts
    def __init__(self, n=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        switch = self.addSwitch('s1', protocols='OpenFlow13')
        # Python's range(N) generates 0..N-1
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            # self.addLink(host, switch, bw=10, delay='5ms', loss=10)
            self.addLink(host, switch, bw=10)



class TwoSwitchTwoHost(Topo):
    def __init__(self):

        # Initialize topology
        Topo.__init__(self)

        # Add hosts and switches
        leftHost = self.addHost('h1')
        rightHost = self.addHost('h2')
        leftSwitch = self.addSwitch('s3',protocols='OpenFlow13')
        rightSwitch = self.addSwitch('s4',protocols='OpenFlow13')

        # Add links
        self.addLink(leftHost, leftSwitch)
        self.addLink(leftSwitch, rightSwitch)
        self.addLink(rightSwitch, rightHost)


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    # simpleTest()
    # perfTest()
    topo = TwoSwitchTwoHost()

    net = Mininet(topo=topo, link=TCLink,
                  controller=None,
                  autoStaticArp=True)
    net.addController("c0",
                      controller=RemoteController,
                      ip=REMOTE_CONTROLLER_IP,
                      port=6633)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    CLI(net)
    net.stop()