package headFirst.Proxy;

import java.rmi.*;
import headFirst.Proxy.Gumball.State;

public interface GumballMachineRemote extends Remote {
    public int getCount() throws RemoteException;
    public String getLocation() throws RemoteException;
    public State getState() throws RemoteException;
}
