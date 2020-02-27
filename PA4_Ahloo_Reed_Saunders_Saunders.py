#!/usr/bin/python
# File: legacy_router-modify.py
# Austin Ah Loo, Mikie Reed, Mitchell Saunders, Nick Saunders
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Host, Node
from mininet.cli import CLI
from mininet.log import setLogLevel, info

# classes and functions structure based on 'linuxrouter.py' example

class NetworkRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( NetworkRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( NetworkRouter, self ).terminate()
        
class NetworkTopo( Topo ):
    "A NetworkRouter connecting one (or more) subnets"
    
    def build( self, **_opts ):
	
	defaultIP = '192.168.1.1/24'  # IP address for r0-eth1
	
	info( '*** Adding controller\n' )
	info( '*** Adding switches\n')
	# create and instantiate router with default subnet as defined
        router = self.addNode( 'r0', cls = NetworkRouter, ip = defaultIP )
        s1 = self.addSwitch( 's1' )
        info( '*** Add links\n')
        
        # establish link between router and switch
        self.addLink( s1, router )
        info( '*** Add hosts\n')
        # define two hosts on the same subnet as the router
        h1 = self.addHost( 'h1', ip='192.168.1.101/24', defaultRoute='via 192.168.1.1' )
        h2 = self.addHost( 'h2', ip='192.168.1.102/24', defaultRoute='via 192.168.1.1' )

	for h, s in [ (h1, s1), (h2, s1) ]:
            self.addLink( h, s )
           
    
def myNetwork():
  
    # Set up network
    "Test network router"
    topo = NetworkTopo()
    net = Mininet( topo=topo )  
    net.start()
    info( '*** Routing Table on Router:\n' )
    print net[ 'r0' ].cmd( 'route' )
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
