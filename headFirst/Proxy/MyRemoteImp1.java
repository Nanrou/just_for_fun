package headFirst.Proxy;

import java.rmi.*;
import java.rmi.server.*;

public class MyRemoteImp1 extends UnicastRemoteObject implements MyRemote {

    public MyRemoteImp1() throws RemoteException{ }

    public String sayHello() {
        return "Server says, 'Hey'";
    }

    public static void main(String[] args) {
        try {
            MyRemote service = new MyRemoteImp1();
            Naming.rebind("RemoteHello", service);
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
